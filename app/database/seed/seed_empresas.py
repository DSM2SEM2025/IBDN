"""
Seed Empresas Module
Popula o banco de dados com empresas de teste para o IBDN.
Este script é idempotente - pode ser executado múltiplas vezes sem duplicar dados.
"""
import logging
import random
from datetime import datetime, timedelta
from decimal import Decimal

from app.database.seed.seed_base import (
    setup_logging,
    record_exists,
    SeedContextManager,
    get_faker,
    gerar_cnpj
)


# Lista de empresas fixas para seed
EMPRESAS_BASE = [
    # Empresas ativas
    {
        "razao_social": "Instituto Brasileiro de Desenvolvimento e Natureza Ltda",
        "nome_fantasia": "IBDN",
        "telefone": "(11) 99999-0001",
        "responsavel": "Carlos Silva",
        "cargo_responsavel": "Diretor Geral",
        "site": "https://www.ibdn.com.br",
        "ativo": True
    },
    {
        "razao_social": "Hotelaria Verde Resort & Spa Ltda",
        "nome_fantasia": "Verde Resort",
        "telefone": "(21) 99999-0002",
        "responsavel": "Ana Paula Oliveira",
        "cargo_responsavel": "Gerente Geral",
        "site": "https://www.verderesort.com.br",
        "ativo": True
    },
    {
        "razao_social": "Logística Sustentável Maestro Frotas Ltda",
        "nome_fantasia": "Maestro Frotas",
        "telefone": "(31) 99999-0003",
        "responsavel": "Roberto Martins",
        "cargo_responsavel": "Diretor de Operações",
        "site": "https://www.maestrofrotas.com.br",
        "ativo": True
    },
    {
        "razao_social": "Café Pilão Indústria e Comércio Ltda",
        "nome_fantasia": "Café Pilão",
        "telefone": "(41) 99999-0004",
        "responsavel": "João Pedro Santos",
        "cargo_responsavel": "CEO",
        "site": "https://www.cafepilao.com.br",
        "ativo": True
    },
    {
        "razao_social": "Solar Energy Solutions Ltda",
        "nome_fantasia": "Solar Energy",
        "telefone": "(51) 99999-0005",
        "responsavel": "Marcos Ferreira",
        "cargo_responsavel": "Diretor Técnico",
        "site": "https://www.solarenergy.com.br",
        "ativo": True
    },
    {
        "razao_social": "Escola Verde Educação Ambiental Ltda",
        "nome_fantasia": "Escola Verde",
        "telefone": "(61) 99999-0006",
        "responsavel": "Patricia Lima",
        "cargo_responsavel": "Diretora Educacional",
        "site": "https://www.escolaverde.edu.br",
        "ativo": True
    },
    {
        "razao_social": "Construtora Eco Eficiente Ltda",
        "nome_fantasia": "Eco Eficiente",
        "telefone": "(71) 99999-0007",
        "responsavel": "Ricardo Almeida",
        "cargo_responsavel": "Engenheiro Responsável",
        "site": "https://www.ecoeficiente.com.br",
        "ativo": True
    },
    # Empresas inativas
    {
        "razao_social": "Marketing Verde Comunicação Ltda",
        "nome_fantasia": "Verde Comunicação",
        "telefone": "(81) 99999-0008",
        "responsavel": "Juliana Costa",
        "cargo_responsavel": "Diretora de Criação",
        "site": "https://www.verdecomunicacao.com.br",
        "ativo": False
    },
    {
        "razao_social": "Tech Sustentável Solutions Ltda",
        "nome_fantasia": "Tech Sus",
        "telefone": "(85) 99999-0009",
        "responsavel": "Fernando Souza",
        "cargo_responsavel": "CEO",
        "site": "https://www.techsus.com.br",
        "ativo": False
    },
    {
        "razao_social": "Agronegócios Campo Verde Ltda",
        "nome_fantasia": "Campo Verde",
        "telefone": "(91) 99999-0010",
        "responsavel": "Antonio Carlos",
        "cargo_responsavel": "Proprietário",
        "site": "https://www.campoverde.com.br",
        "ativo": False
    },
]

# Quantidade adicional de empresas Faker a gerar
EMPRESAS_FAKER_ADICIONAIS = 5

# Ramos de atividade para associar (serão buscados do banco)
RAMOS_DISPONIVEIS = [
    "Hotelaria e Turismo",
    "Logística e Transporte",
    "Agronegócios e Eventos Rurais",
    "Alimentos e Bebidas",
    "Energia e Sustentabilidade",
    "Educação e Conscientização Ambiental",
    "Construção Civil e Imobiliário",
    "Marketing e Comunicação",
    "Setor Público e Políticas Ambientais",
    "Tecnologia e Serviços"
]


def get_usuarios_empresa_ids(cursor) -> list:
    """
    Obtém IDs dos usuários com perfil 'empresa'.
    
    Args:
        cursor: Cursor do banco de dados
        
    Returns:
        Lista de IDs de usuários empresa
    """
    cursor.execute("""
        SELECT u.id 
        FROM ibdn_usuarios u
        JOIN ibdn_perfis p ON u.perfil_id = p.id
        WHERE p.nome = 'empresa'
    """)
    return [row["id"] for row in cursor.fetchall()]


def get_ramo_id(nome_ramo: str, cursor) -> int:
    """
    Obtém o ID de um ramo pelo nome.
    
    Args:
        nome_ramo: Nome do ramo
        cursor: Cursor do banco de dados
        
    Returns:
        ID do ramo ou None se não encontrado
    """
    cursor.execute("SELECT id FROM ramo WHERE nome = %s", (nome_ramo,))
    resultado = cursor.fetchone()
    return resultado["id"] if resultado else None


def gerar_cnpj_unico(cursor) -> str:
    """
    Gera um CNPJ único que não existe no banco.
    
    Args:
        cursor: Cursor do banco de dados
        
    Returns:
        CNPJ válido e único
    """
    max_tentativas = 50
    for _ in range(max_tentativas):
        cnpj = gerar_cnpj()
        if not record_exists("empresa", "cnpj", cnpj, cursor):
            return cnpj
    raise ValueError("Não foi possível gerar um CNPJ único após muitas tentativas")


def seed_empresas_fixas(logger: logging.Logger) -> dict:
    """
    Popula empresas fixas definidas na lista EMPRESAS_BASE.
    Idempotente: não cria empresas duplicadas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criadas": 0, "existentes": 0, "erros": 0}
    faker = get_faker()
    
    with SeedContextManager(logger) as ctx:
        # Obtém IDs dos usuários empresa
        usuarios_empresa = get_usuarios_empresa_ids(ctx.cursor)
        
        if not usuarios_empresa:
            logger.warning("Nenhum usuário com perfil 'empresa' encontrado!")
            logger.warning("Criando usuários empresa temporários para associação...")
            
            # Cria usuários empresa temporários se não existirem
            from app.security.password import get_password_hash
            import uuid
            
            for i, empresa_data in enumerate(EMPRESAS_BASE[:5]):  # Usa 5 empresas
                # Obtém perfil empresa
                ctx.cursor.execute(
                    "SELECT id FROM ibdn_perfis WHERE nome = 'empresa'"
                )
                perfil_result = ctx.cursor.fetchone()
                if not perfil_result:
                    logger.error("Perfil 'empresa' não encontrado!")
                    continue
                
                perfil_id = perfil_result["id"]
                
                # Cria usuário
                usuario_id = str(uuid.uuid4())
                senha_hash = get_password_hash("Teste@123")
                
                ctx.cursor.execute(
                    """INSERT INTO ibdn_usuarios 
                       (id, nome, email, senha_hash, perfil_id, ativo) 
                       VALUES (%s, %s, %s, %s, %s, 1)""",
                    (
                        usuario_id,
                        f"Usuário {empresa_data['nome_fantasia']}",
                        f"user_{i+1}@temp.com",
                        senha_hash,
                        perfil_id
                    )
                )
                usuarios_empresa.append(usuario_id)
                logger.info(f"Usuário temporário criado para {empresa_data['nome_fantasia']}")
            
            ctx.commit()
        
        logger.info(f"Encontrados {len(usuarios_empresa)} usuários empresa")
        
        for i, empresa_data in enumerate(EMPRESAS_BASE):
            # Usa nome_fantasia como identificador único para verificar duplicata
            nome_fantasia = empresa_data["nome_fantasia"]
            
            # Verifica se empresa já existe (pelo nome fantasia ou CNPJ)
            ctx.cursor.execute(
                "SELECT id FROM empresa WHERE nome_fantasia = %s OR razao_social = %s",
                (nome_fantasia, empresa_data["razao_social"])
            )
            
            if ctx.cursor.fetchone():
                logger.info(f"Empresa '{nome_fantasia}' já existe, pulando...")
                stats["existentes"] += 1
                continue
            
            # Gera CNPJ único
            cnpj = gerar_cnpj_unico(ctx.cursor)
            
            # Associa a um usuário empresa (distribui circularmente)
            usuario_id = usuarios_empresa[i % len(usuarios_empresa)] if usuarios_empresa else None
            
            if not usuario_id:
                logger.warning(f"Nenhum usuário disponível para empresa '{nome_fantasia}', pulando...")
                stats["erros"] += 1
                continue
            
            # Gera data de cadastro aleatória (entre 1 e 365 dias atrás)
            dias_atras = random.randint(1, 365)
            data_cadastro = datetime.now() - timedelta(days=dias_atras)
            
            ctx.cursor.execute(
                """INSERT INTO empresa 
                   (cnpj, razao_social, nome_fantasia, usuario_id, telefone, 
                    responsavel, cargo_responsavel, site, data_cadastro, ativo) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    cnpj,
                    empresa_data["razao_social"],
                    nome_fantasia,
                    usuario_id,
                    empresa_data["telefone"],
                    empresa_data["responsavel"],
                    empresa_data["cargo_responsavel"],
                    empresa_data["site"],
                    data_cadastro,
                    1 if empresa_data["ativo"] else 0
                )
            )
            
            empresa_id = ctx.cursor.lastrowid
            
            logger.info(
                f"Empresa criada: {nome_fantasia} | CNPJ: {cnpj} | "
                f"Ativo: {empresa_data['ativo']} | Usuário: {usuario_id[:8]}..."
            )
            stats["criadas"] += 1
        
        ctx.commit()
    
    return stats


def seed_empresas_faker(logger: logging.Logger, quantidade: int = 5) -> dict:
    """
    Popula empresas aleatórias usando Faker.
    Idempotente: cria apenas empresas que não existem.
    
    Args:
        logger: Logger para mensagens
        quantidade: Quantidade de empresas a gerar
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criadas": 0, "existentes": 0, "erros": 0}
    faker = get_faker()
    
    # Prefixos para razão social
    prefixos = [
        "Grupo", "Corporação", "Industria", "Comércio", "Serviços",
        "Solutions", "Technologies", "Group", "Holdings"
    ]
    
    # Sufixos para razão social
    suffixes = [
        "Ltda", "Eireli", "ME", "MEI", "S.A.", "SS"
    ]
    
    with SeedContextManager(logger) as ctx:
        # Obtém IDs dos usuários empresa
        usuarios_empresa = get_usuarios_empresa_ids(ctx.cursor)
        
        if not usuarios_empresa:
            logger.warning("Nenhum usuário com perfil 'empresa' encontrado!")
            stats["erros"] += quantidade
            return stats
        
        for i in range(quantidade):
            # Gera dados aleatórios
            nome_fantasia = faker.company()
            prefixo = random.choice(prefixos)
            razao_social = f"{prefixo} {faker.last_name()} {random.choice(suffixes)}"
            
            # Verifica se empresa já existe
            ctx.cursor.execute(
                "SELECT id FROM empresa WHERE nome_fantasia = %s",
                (nome_fantasia,)
            )
            
            if ctx.cursor.fetchone():
                stats["existentes"] += 1
                continue
            
            # Gera CNPJ único
            cnpj = gerar_cnpj_unico(ctx.cursor)
            
            # Seleciona usuário aleatório
            usuario_id = random.choice(usuarios_empresa)
            
            # Gera telefone
            telefone = faker.phone_number()
            
            # Gera responsável
            responsavel = faker.name()
            cargo = random.choice([
                "Gerente", "Diretor", "Coordenador", "Supervisor",
                "Administrador", "CEO", "Proprietário"
            ])
            
            # Gera site
            palavras = nome_fantasia.lower().split()
            site = f"https://www.{''.join(palavras[:2])}.com.br"
            
            # Gera data de cadastro aleatória
            dias_atras = random.randint(1, 730)  # Até 2 anos atrás
            data_cadastro = datetime.now() - timedelta(days=dias_atras)
            
            # Status ativo (75% ativas)
            ativo = random.choice([True, True, True, False])
            
            try:
                ctx.cursor.execute(
                    """INSERT INTO empresa 
                       (cnpj, razao_social, nome_fantasia, usuario_id, telefone, 
                        responsavel, cargo_responsavel, site, data_cadastro, ativo) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        cnpj,
                        razao_social,
                        nome_fantasia,
                        usuario_id,
                        telefone,
                        responsavel,
                        cargo,
                        site,
                        data_cadastro,
                        1 if ativo else 0
                    )
                )
                
                logger.info(
                    f"Empresa Faker criada: {nome_fantasia} | CNPJ: {cnpj} | "
                    f"Ativo: {ativo}"
                )
                stats["criadas"] += 1
                
            except Exception as e:
                logger.error(f"Erro ao criar empresa {nome_fantasia}: {e}")
                stats["erros"] += 1
        
        ctx.commit()
    
    return stats


def verificar_empresas(logger: logging.Logger) -> dict:
    """
    Verifica a quantidade de empresas por status e outras estatísticas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {}
    
    with SeedContextManager(logger) as ctx:
        # Total de empresas
        ctx.cursor.execute("SELECT COUNT(*) as total FROM empresa")
        stats["total"] = ctx.cursor.fetchone()["total"]
        
        # Por status ativo
        ctx.cursor.execute("""
            SELECT ativo, COUNT(*) as total 
            FROM empresa 
            GROUP BY ativo
        """)
        stats["por_ativo"] = {}
        for row in ctx.cursor.fetchall():
            key = "ativas" if row["ativo"] else "inativas"
            stats["por_ativo"][key] = row["total"]
        
        # Empresas com e sem responsável
        ctx.cursor.execute("""
            SELECT 
                CASE WHEN responsavel IS NOT NULL AND responsavel != '' THEN 'com_responsavel' 
                ELSE 'sem_responsavel' END as status,
                COUNT(*) as total 
            FROM empresa 
            GROUP BY status
        """)
        stats["por_responsavel"] = {}
        for row in ctx.cursor.fetchall():
            stats["por_responsavel"][row["status"]] = row["total"]
        
        # Empresas por usuário
        ctx.cursor.execute("""
            SELECT usuario_id, COUNT(*) as total 
            FROM empresa 
            GROUP BY usuario_id 
            ORDER BY total DESC 
            LIMIT 5
        """)
        stats["por_usuario_top5"] = [
            {"usuario_id": row["usuario_id"][:8] + "...", "total": row["total"]}
            for row in ctx.cursor.fetchall()
        ]
    
    return stats


def run_seed_empresas(logger: logging.Logger = None) -> dict:
    """
    Executa o seed completo de empresas.
    
    Args:
        logger: Logger opcional
        
    Returns:
        Dicionário com estatísticas finais
    """
    logger = logger or setup_logging('seed_empresas')
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO SEED DE EMPRESAS")
        logger.info("=" * 60)
        
        # Step 1: Empresas fixas
        logger.info("\n--- Step 1: Criando Empresas Fixas ---")
        stats_fixas = seed_empresas_fixas(logger)
        logger.info(
            f"Empresas Fixas: {stats_fixas['criadas']} criadas, "
            f"{stats_fixas['existentes']} existentes, {stats_fixas['erros']} erros"
        )
        
        # Step 2: Empresas Faker
        logger.info(f"\n--- Step 2: Criando {EMPRESAS_FAKER_ADICIONAIS} Empresas Faker ---")
        stats_faker = seed_empresas_faker(logger, EMPRESAS_FAKER_ADICIONAIS)
        logger.info(
            f"Empresas Faker: {stats_faker['criadas']} criadas, "
            f"{stats_faker['existentes']} existentes, {stats_faker['erros']} erros"
        )
        
        # Step 3: Verificação
        logger.info("\n--- Step 3: Verificação ---")
        stats_verificacao = verificar_empresas(logger)
        logger.info(f"Total de empresas no banco: {stats_verificacao['total']}")
        logger.info(f"Por status ativo: {stats_verificacao['por_ativo']}")
        logger.info(f"Por responsável: {stats_verificacao['por_responsavel']}")
        logger.info(f"Top 5 usuários com mais empresas: {stats_verificacao['por_usuario_top5']}")
        
        logger.info("=" * 60)
        logger.info("SEED DE EMPRESAS CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        
        return {
            "sucesso": True,
            "criadas": stats_fixas["criadas"] + stats_faker["criadas"],
            "existentes": stats_fixas["existentes"] + stats_faker["existentes"],
            "total": stats_verificacao["total"]
        }
        
    except Exception as e:
        logger.error(f"ERRO DURANTE SEED: {e}")
        return {"sucesso": False, "erro": str(e)}


if __name__ == "__main__":
    logger = setup_logging('seed_empresas')
    
    print("\n" + "=" * 60)
    print("SEED DE EMPRESAS - IBDN")
    print("=" * 60 + "\n")
    
    # Executa o seed
    resultado = run_seed_empresas(logger)
    
    if resultado.get("sucesso"):
        print("\n[RESULTADO]")
        print(f"Empresas criadas: {resultado.get('criadas', 0)}")
        print(f"Empresas existentes: {resultado.get('existentes', 0)}")
        print(f"Total no banco: {resultado.get('total', 0)}")
        print("\n[FASE 2 - EMPRESAS CONCLUIDA COM SUCESSO]")
    else:
        print(f"\n[ERRO]: {resultado.get('erro', 'Erro desconhecido')}")
        exit(1)
