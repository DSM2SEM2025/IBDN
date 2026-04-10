"""
Seed Usuarios Module
Popula o banco de dados com usuários de teste para o IBDN.
Este script é idempotente - pode ser executado múltiplas vezes sem duplicar dados.
"""
import logging
import uuid
import random
from datetime import datetime

from app.database.seed.seed_base import (
    setup_logging,
    record_exists,
    SeedContextManager,
    get_faker
)
from app.security.password import get_password_hash


# Definição dos perfis disponíveis
PERFIS_DISPONIVEIS = ["admin_master", "admin", "empresa"]

# Lista de usuários para seed (será mesclado com dados do Faker)
USUARIOS_BASE = [
    # Admin Master (1)
    {
        "nome": "Admin Master IBDN",
        "email": "admin.master@ibdn.com.br",
        "perfil": "admin_master",
        "ativo": True,
        "twofactor": True
    },
    # Admin (3)
    {
        "nome": "Administrador Geral",
        "email": "admin.geral@ibdn.com.br",
        "perfil": "admin",
        "ativo": True,
        "twofactor": False
    },
    {
        "nome": "Administrador de Operações",
        "email": "admin.operacoes@ibdn.com.br",
        "perfil": "admin",
        "ativo": True,
        "twofactor": True
    },
    {
        "nome": "Administrador de Suporte",
        "email": "admin.suporte@ibdn.com.br",
        "perfil": "admin",
        "ativo": False,
        "twofactor": False
    },
    # Empresa (usuários ativos)
    {
        "nome": "Empresa Ativa Teste 1",
        "email": "empresa.teste1@exemplo.com.br",
        "perfil": "empresa",
        "ativo": True,
        "twofactor": False
    },
    {
        "nome": "Empresa Ativa Teste 2",
        "email": "empresa.teste2@exemplo.com.br",
        "perfil": "empresa",
        "ativo": True,
        "twofactor": True
    },
    {
        "nome": "Empresa Ativa Teste 3",
        "email": "empresa.teste3@exemplo.com.br",
        "perfil": "empresa",
        "ativo": True,
        "twofactor": False
    },
    {
        "nome": "Empresa Ativa Teste 4",
        "email": "empresa.teste4@exemplo.com.br",
        "perfil": "empresa",
        "ativo": True,
        "twofactor": True
    },
    {
        "nome": "Empresa Ativa Teste 5",
        "email": "empresa.teste5@exemplo.com.br",
        "perfil": "empresa",
        "ativo": True,
        "twofactor": False
    },
    # Empresa (usuários inativos)
    {
        "nome": "Empresa Inativa Teste 1",
        "email": "empresa.inativa1@exemplo.com.br",
        "perfil": "empresa",
        "ativo": False,
        "twofactor": False
    },
    {
        "nome": "Empresa Inativa Teste 2",
        "email": "empresa.inativa2@exemplo.com.br",
        "perfil": "empresa",
        "ativo": False,
        "twofactor": True
    },
    {
        "nome": "Empresa Inativa Teste 3",
        "email": "empresa.inativa3@exemplo.com.br",
        "perfil": "empresa",
        "ativo": False,
        "twofactor": False
    },
]

# Quantidade adicional de usuários Faker a gerar
USUARIOS_FAKER_ADICIONAIS = 8

# Senha padrão para todos os usuários de teste
SENHA_PADRAO = "Teste@123"


def get_perfil_id(nome_perfil: str, cursor) -> str:
    """
    Obtém o ID de um perfil pelo nome.
    
    Args:
        nome_perfil: Nome do perfil
        cursor: Cursor do banco de dados
        
    Returns:
        ID do perfil ou None se não encontrado
    """
    cursor.execute(
        "SELECT id FROM ibdn_perfis WHERE nome = %s",
        (nome_perfil,)
    )
    resultado = cursor.fetchone()
    return resultado["id"] if resultado else None


def seed_usuarios_fixos(logger: logging.Logger) -> dict:
    """
    Popula usuários fixos definidos na lista USUARIOS_BASE.
    Idempotente: não cria usuários duplicados.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criados": 0, "existentes": 0, "erros": 0}
    faker = get_faker()
    
    with SeedContextManager(logger) as ctx:
        for usuario_data in USUARIOS_BASE:
            email = usuario_data["email"]
            
            # Verifica se usuário já existe
            if record_exists("ibdn_usuarios", "email", email, ctx.cursor):
                logger.info(f"Usuário '{email}' já existe, pulando...")
                stats["existentes"] += 1
                continue
            
            # Obtém ID do perfil
            perfil_id = get_perfil_id(usuario_data["perfil"], ctx.cursor)
            if not perfil_id:
                logger.warning(f"Perfil '{usuario_data['perfil']}' não encontrado para '{email}', pulando...")
                stats["erros"] += 1
                continue
            
            # Cria novo usuário
            usuario_id = str(uuid.uuid4())
            senha_hash = get_password_hash(SENHA_PADRAO)
            
            ctx.cursor.execute(
                """INSERT INTO ibdn_usuarios 
                   (id, nome, email, senha_hash, perfil_id, ativo, twofactor) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    usuario_id,
                    usuario_data["nome"],
                    email,
                    senha_hash,
                    perfil_id,
                    1 if usuario_data["ativo"] else 0,
                    1 if usuario_data["twofactor"] else 0
                )
            )
            
            logger.info(
                f"Usuário criado: {email} | Perfil: {usuario_data['perfil']} | "
                f"Ativo: {usuario_data['ativo']} | 2FA: {usuario_data['twofactor']}"
            )
            stats["criados"] += 1
        
        ctx.commit()
    
    return stats


def seed_usuarios_faker(logger: logging.Logger, quantidade: int = 8) -> dict:
    """
    Popula usuários aleatórios usando Faker.
    Idempotente: cria apenas usuários que não existem.
    
    Args:
        logger: Logger para mensagens
        quantidade: Quantidade de usuários a gerar
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criados": 0, "existentes": 0, "erros": 0}
    faker = get_faker()
    
    # Domains para gerar emails realistas
    domains = [
        "exemplo.com.br", "empresa.com.br", "corporacao.com.br",
        "negocios.com.br", "solucoes.com.br", "grupo.com.br"
    ]
    
    # Perfis com peso (empresa tem maior probabilidade)
    pesos_perfil = {"admin_master": 1, "admin": 3, "empresa": 10}
    
    with SeedContextManager(logger) as ctx:
        for i in range(quantidade):
            # Gera nome fake
            nome = faker.name()
            
            # Gera email fake único
            nome_parts = nome.lower().split()
            base_email = f"{nome_parts[0]}.{nome_parts[-1]}" if len(nome_parts) > 1 else nome_parts[0]
            domain = random.choice(domains)
            email = f"{base_email}{random.randint(1, 999)}@{domain}"
            
            # Verifica se email já existe
            if record_exists("ibdn_usuarios", "email", email, ctx.cursor):
                logger.debug(f"Email '{email}' já existe, gerando outro...")
                # Tenta outro email
                email = f"{base_email}_{random.randint(1000, 9999)}@{domain}"
                if record_exists("ibdn_usuarios", "email", email, ctx.cursor):
                    stats["existentes"] += 1
                    continue
            
            # Seleciona perfil aleatório com pesos
            perfil_nome = random.choices(
                list(pesos_perfil.keys()),
                weights=list(pesos_perfil.values())
            )[0]
            
            perfil_id = get_perfil_id(perfil_nome, ctx.cursor)
            if not perfil_id:
                logger.warning(f"Perfil '{perfil_nome}' não encontrado, pulando...")
                stats["erros"] += 1
                continue
            
            # Gera status aleatório
            ativo = random.choice([True, True, True, False])  # 75% ativos
            twofactor = random.choice([True, False, False, False])  # 25% com 2FA
            
            # Cria novo usuário
            usuario_id = str(uuid.uuid4())
            senha_hash = get_password_hash(SENHA_PADRAO)
            
            try:
                ctx.cursor.execute(
                    """INSERT INTO ibdn_usuarios 
                       (id, nome, email, senha_hash, perfil_id, ativo, twofactor) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        usuario_id,
                        nome,
                        email,
                        senha_hash,
                        perfil_id,
                        1 if ativo else 0,
                        1 if twofactor else 0
                    )
                )
                
                logger.info(
                    f"Usuário Faker criado: {email} | Perfil: {perfil_nome} | "
                    f"Ativo: {ativo} | 2FA: {twofactor}"
                )
                stats["criados"] += 1
                
            except Exception as e:
                logger.error(f"Erro ao criar usuário {email}: {e}")
                stats["erros"] += 1
        
        ctx.commit()
    
    return stats


def verificar_usuarios(logger: logging.Logger) -> dict:
    """
    Verifica a quantidade de usuários por perfil e status.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {}
    
    with SeedContextManager(logger) as ctx:
        # Total de usuários
        ctx.cursor.execute("SELECT COUNT(*) as total FROM ibdn_usuarios")
        stats["total"] = ctx.cursor.fetchone()["total"]
        
        # Por perfil
        ctx.cursor.execute("""
            SELECT p.nome as perfil, COUNT(u.id) as total 
            FROM ibdn_usuarios u 
            LEFT JOIN ibdn_perfis p ON u.perfil_id = p.id 
            GROUP BY p.nome
        """)
        stats["por_perfil"] = {row["perfil"]: row["total"] for row in ctx.cursor.fetchall()}
        
        # Por status ativo
        ctx.cursor.execute("""
            SELECT ativo, COUNT(*) as total 
            FROM ibdn_usuarios 
            GROUP BY ativo
        """)
        stats["por_ativo"] = {}
        for row in ctx.cursor.fetchall():
            key = "ativos" if row["ativo"] else "inativos"
            stats["por_ativo"][key] = row["total"]
        
        # Por twofactor
        ctx.cursor.execute("""
            SELECT twofactor, COUNT(*) as total 
            FROM ibdn_usuarios 
            GROUP BY twofactor
        """)
        stats["por_twofactor"] = {}
        for row in ctx.cursor.fetchall():
            key = "com_2fa" if row["twofactor"] else "sem_2fa"
            stats["por_twofactor"][key] = row["total"]
    
    return stats


def run_seed_usuarios(logger: logging.Logger = None) -> dict:
    """
    Executa o seed completo de usuários.
    
    Args:
        logger: Logger opcional
        
    Returns:
        Dicionário com estatísticas finais
    """
    logger = logger or setup_logging('seed_usuarios')
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO SEED DE USUARIOS")
        logger.info("=" * 60)
        
        # Step 1: Usuários fixos
        logger.info("\n--- Step 1: Criando Usuários Fixos ---")
        stats_fixos = seed_usuarios_fixos(logger)
        logger.info(
            f"Usuários Fixos: {stats_fixos['criados']} criados, "
            f"{stats_fixos['existentes']} existentes, {stats_fixos['erros']} erros"
        )
        
        # Step 2: Usuários Faker
        logger.info(f"\n--- Step 2: Criando {USUARIOS_FAKER_ADICIONAIS} Usuários Faker ---")
        stats_faker = seed_usuarios_faker(logger, USUARIOS_FAKER_ADICIONAIS)
        logger.info(
            f"Usuários Faker: {stats_faker['criados']} criados, "
            f"{stats_faker['existentes']} existentes, {stats_faker['erros']} erros"
        )
        
        # Step 3: Verificação
        logger.info("\n--- Step 3: Verificação ---")
        stats_verificacao = verificar_usuarios(logger)
        logger.info(f"Total de usuários no banco: {stats_verificacao['total']}")
        logger.info(f"Por perfil: {stats_verificacao['por_perfil']}")
        logger.info(f"Por status ativo: {stats_verificacao['por_ativo']}")
        logger.info(f"Por twofactor: {stats_verificacao['por_twofactor']}")
        
        logger.info("=" * 60)
        logger.info("SEED DE USUARIOS CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        
        return {
            "sucesso": True,
            "criados": stats_fixos["criados"] + stats_faker["criados"],
            "existentes": stats_fixos["existentes"] + stats_faker["existentes"],
            "total": stats_verificacao["total"]
        }
        
    except Exception as e:
        logger.error(f"ERRO DURANTE SEED: {e}")
        return {"sucesso": False, "erro": str(e)}


if __name__ == "__main__":
    logger = setup_logging('seed_usuarios')
    
    print("\n" + "=" * 60)
    print("SEED DE USUARIOS - IBDN")
    print("=" * 60 + "\n")
    
    # Executa o seed
    resultado = run_seed_usuarios(logger)
    
    if resultado.get("sucesso"):
        print("\n[RESULTADO]")
        print(f"Usuários criados: {resultado.get('criados', 0)}")
        print(f"Usuários existentes: {resultado.get('existentes', 0)}")
        print(f"Total no banco: {resultado.get('total', 0)}")
        print("\n[FASE 2 - USUARIOS CONCLUIDA COM SUCESSO]")
    else:
        print(f"\n[ERRO]: {resultado.get('erro', 'Erro desconhecido')}")
        exit(1)
