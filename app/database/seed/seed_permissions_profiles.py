"""
Seed Permissions and Profiles Module
Popula o banco de dados com permissões granulares e associações perfil-permissão.
Este script é idempotente - pode ser executado múltiplas vezes sem duplicar dados.
"""
import logging
import uuid

from app.database.seed.seed_base import (
    setup_logging,
    get_db_connection,
    record_exists,
    SeedContextManager
)


# Definição das permissões granulares
PERMISSOES = [
    # Permissões de Empresa
    {"nome": "criar_empresa", "descricao": "Permite criar novas empresas no sistema"},
    {"nome": "editar_empresa", "descricao": "Permite editar dados de empresas existentes"},
    {"nome": "visualizar_empresa", "descricao": "Permite visualizar dados de empresas"},
    {"nome": "excluir_empresa", "descricao": "Permite excluir empresas do sistema"},
    
    # Permissões de Selo
    {"nome": "solicitar_selo", "descricao": "Permite solicitar selos para empresas"},
    {"nome": "gerenciar_selos", "descricao": "Permite gerenciar (aprovar/rejeitar) selos"},
    {"nome": "visualizar_selos", "descricao": "Permite visualizar selos disponíveis"},
    
    # Permissões de Usuário
    {"nome": "gerenciar_usuarios", "descricao": "Permite criar, editar e desativar usuários"},
    {"nome": "editar_usuario_proprio", "descricao": "Permite editar próprios dados do usuário"},
    {"nome": "visualizar_usuarios", "descricao": "Permite listar usuários do sistema"},
    
    # Permissões de Relatórios
    {"nome": "visualizar_relatorios", "descricao": "Permite acessar relatórios e métricas"},
    {"nome": "exportar_relatorios", "descricao": "Permite exportar relatórios em diversos formatos"},
    
    # Permissões de Notificações
    {"nome": "configurar_notificacoes", "descricao": "Permite configurar preferências de notificações"},
    {"nome": "visualizar_notificacoes", "descricao": "Permite visualizar histórico de notificações"},
    
    # Permissões de Admin
    {"nome": "admin", "descricao": "Acesso administrativo completo"},
    {"nome": "admin_master", "descricao": "Acesso master administrativo"},
    {"nome": "empresa", "descricao": "Acesso padrão para empresas"},
    
    # Permissões de Ramos e Selos (cadastro)
    {"nome": "gerenciar_ramos", "descricao": "Permite gerenciar ramos de atividade"},
    {"nome": "gerenciar_selos_cadastro", "descricao": "Permite gerenciar tipos de selos"},
    
    # Permissões de Endereço
    {"nome": "gerenciar_enderecos", "descricao": "Permite gerenciar endereços de empresas"},
]

# Definição das associações perfil-permissão
# Cada perfil tem uma lista de permissões
PERFIL_PERMISSOES = {
    "admin_master": [
        "criar_empresa",
        "editar_empresa",
        "visualizar_empresa",
        "excluir_empresa",
        "solicitar_selo",
        "gerenciar_selos",
        "visualizar_selos",
        "gerenciar_usuarios",
        "editar_usuario_proprio",
        "visualizar_usuarios",
        "visualizar_relatorios",
        "exportar_relatorios",
        "configurar_notificacoes",
        "visualizar_notificacoes",
        "admin_master",
        "gerenciar_ramos",
        "gerenciar_selos_cadastro",
        "gerenciar_enderecos",
    ],
    "admin": [
        "criar_empresa",
        "editar_empresa",
        "visualizar_empresa",
        "solicitar_selo",
        "gerenciar_selos",
        "visualizar_selos",
        "gerenciar_usuarios",
        "editar_usuario_proprio",
        "visualizar_usuarios",
        "visualizar_relatorios",
        "exportar_relatorios",
        "configurar_notificacoes",
        "visualizar_notificacoes",
        "admin",
        "gerenciar_ramos",
        "gerenciar_selos_cadastro",
        "gerenciar_enderecos",
    ],
    "empresa": [
        "visualizar_empresa",
        "editar_empresa",
        "solicitar_selo",
        "visualizar_selos",
        "editar_usuario_proprio",
        "visualizar_notificacoes",
        "configurar_notificacoes",
        "gerenciar_enderecos",
        "empresa",
    ],
}


def seed_permissoes(logger: logging.Logger) -> dict:
    """
    Popula a tabela ibdn_permissoes com permissões granulares.
    Idempotente: não cria permissões duplicadas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens de criadas/existentes
    """
    stats = {"criadas": 0, "existentes": 0}
    
    with SeedContextManager(logger) as ctx:
        for permissao in PERMISSOES:
            nome = permissao["nome"]
            
            # Verifica se já existe
            if record_exists("ibdn_permissoes", "nome", nome, ctx.cursor):
                logger.info(f"Permissão '{nome}' já existe, pulando...")
                stats["existentes"] += 1
            else:
                # Cria nova permissão
                permissao_id = str(uuid.uuid4())
                ctx.cursor.execute(
                    "INSERT INTO ibdn_permissoes (id, nome) VALUES (%s, %s)",
                    (permissao_id, nome)
                )
                logger.info(f"Permissão '{nome}' criada com ID: {permissao_id}")
                stats["criadas"] += 1
        
        ctx.commit()
    
    return stats


def seed_perfis(logger: logging.Logger) -> dict:
    """
    Garante que os perfis padrão existam.
    Idempotente: não cria perfis duplicados.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criados": 0, "existentes": 0}
    
    nomes_perfis = list(PERFIL_PERMISSOES.keys())
    
    with SeedContextManager(logger) as ctx:
        for nome_perfil in nomes_perfis:
            if record_exists("ibdn_perfis", "nome", nome_perfil, ctx.cursor):
                logger.info(f"Perfil '{nome_perfil}' já existe, pulando...")
                stats["existentes"] += 1
            else:
                perfil_id = str(uuid.uuid4())
                ctx.cursor.execute(
                    "INSERT INTO ibdn_perfis (id, nome) VALUES (%s, %s)",
                    (perfil_id, nome_perfil)
                )
                logger.info(f"Perfil '{nome_perfil}' criado com ID: {perfil_id}")
                stats["criados"] += 1
        
        ctx.commit()
    
    return stats


def seed_associacoes(logger: logging.Logger) -> dict:
    """
    Popula a tabela ibdn_perfil_permissoes com associações completas.
    Idempotente: não cria associações duplicadas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criadas": 0, "existentes": 0}
    
    with SeedContextManager(logger) as ctx:
        for nome_perfil, permissoes in PERFIL_PERMISSOES.items():
            # Obtém ID do perfil
            ctx.cursor.execute(
                "SELECT id FROM ibdn_perfis WHERE nome = %s",
                (nome_perfil,)
            )
            resultado_perfil = ctx.cursor.fetchone()
            
            if not resultado_perfil:
                logger.warning(f"Perfil '{nome_perfil}' não encontrado, pulando...")
                continue
            
            perfil_id = resultado_perfil["id"]
            
            for nome_permissao in permissoes:
                # Obtém ID da permissão
                ctx.cursor.execute(
                    "SELECT id FROM ibdn_permissoes WHERE nome = %s",
                    (nome_permissao,)
                )
                resultado_permissao = ctx.cursor.fetchone()
                
                if not resultado_permissao:
                    logger.warning(f"Permissão '{nome_permissao}' não encontrada, pulando...")
                    continue
                
                permissao_id = resultado_permissao["id"]
                
                # Verifica se associação já existe
                ctx.cursor.execute(
                    """SELECT 1 FROM ibdn_perfil_permissoes 
                       WHERE perfil_id = %s AND permissao_id = %s""",
                    (perfil_id, permissao_id)
                )
                
                if ctx.cursor.fetchone():
                    logger.debug(
                        f"Associação '{nome_perfil}' -> '{nome_permissao}' já existe"
                    )
                    stats["existentes"] += 1
                else:
                    # Cria nova associação
                    ctx.cursor.execute(
                        """INSERT INTO ibdn_perfil_permissoes 
                           (perfil_id, permissao_id) VALUES (%s, %s)""",
                        (perfil_id, permissao_id)
                    )
                    logger.info(
                        f"Associação criada: '{nome_perfil}' -> '{nome_permissao}'"
                    )
                    stats["criadas"] += 1
        
        ctx.commit()
    
    return stats


def run_seed_permissions_profiles(logger: logging.Logger = None) -> bool:
    """
    Executa o seed completo de permissões e perfis.
    
    Args:
        logger: Logger opcional
        
    Returns:
        True se sucesso, False caso contrário
    """
    logger = logger or setup_logging('seed_permissions_profiles')
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO SEED DE PERMISSÕES E PERFIS")
        logger.info("=" * 60)
        
        # Step 1: Garante que perfis existam
        logger.info("\n--- Step 1: Verificando/Criando Perfis ---")
        stats_perfis = seed_perfis(logger)
        logger.info(f"Perfis: {stats_perfis['criados']} criados, {stats_perfis['existentes']} existentes")
        
        # Step 2: Popula permissões
        logger.info("\n--- Step 2: Populando Permissões Granulares ---")
        stats_permissoes = seed_permissoes(logger)
        logger.info(f"Permissões: {stats_permissoes['criadas']} criadas, {stats_permissoes['existentes']} existentes")
        
        # Step 3: Associa permissões aos perfis
        logger.info("\n--- Step 3: Associando Permissões aos Perfis ---")
        stats_associacoes = seed_associacoes(logger)
        logger.info(f"Associações: {stats_associacoes['criadas']} criadas, {stats_associacoes['existentes']} existentes")
        
        logger.info("=" * 60)
        logger.info("SEED DE PERMISSÕES E PERFIS CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"ERRO DURANTE SEED: {e}")
        return False


def verificar_estrutura(logger: logging.Logger = None) -> bool:
    """
    Verifica se a estrutura de permissões e perfis está correta.
    
    Args:
        logger: Logger opcional
        
    Returns:
        True se estrutura OK, False caso contrário
    """
    logger = logger or setup_logging('seed_permissions_profiles')
    
    try:
        with SeedContextManager(logger) as ctx:
            # Conta permissões
            ctx.cursor.execute("SELECT COUNT(*) as total FROM ibdn_permissoes")
            total_permissoes = ctx.cursor.fetchone()["total"]
            
            # Conta perfis
            ctx.cursor.execute("SELECT COUNT(*) as total FROM ibdn_perfis")
            total_perfis = ctx.cursor.fetchone()["total"]
            
            # Conta associações
            ctx.cursor.execute("SELECT COUNT(*) as total FROM ibdn_perfil_permissoes")
            total_associacoes = ctx.cursor.fetchone()["total"]
            
            logger.info("=" * 60)
            logger.info("VERIFICAÇÃO DA ESTRUTURA")
            logger.info("=" * 60)
            logger.info(f"Total de Permissões: {total_permissoes}")
            logger.info(f"Total de Perfis: {total_perfis}")
            logger.info(f"Total de Associações: {total_associacoes}")
            logger.info("=" * 60)
            
            # Lista permissões por perfil
            logger.info("\n--- Permissões por Perfil ---")
            for nome_perfil in PERFIL_PERMISSOES.keys():
                ctx.cursor.execute(
                    """SELECT COUNT(*) as total 
                       FROM ibdn_perfil_permissoes pp
                       JOIN ibdn_perfis p ON p.id = pp.perfil_id
                       WHERE p.nome = %s""",
                    (nome_perfil,)
                )
                total = ctx.cursor.fetchone()["total"]
                logger.info(f"  {nome_perfil}: {total} permissões")
            
            return True
            
    except Exception as e:
        logger.error(f"ERRO NA VERIFICAÇÃO: {e}")
        return False


if __name__ == "__main__":
    logger = setup_logging('seed_permissions_profiles')
    
    print("\n" + "=" * 60)
    print("SEED DE PERMISSOES E PERFIS - IBDN")
    print("=" * 60 + "\n")
    
    # Executa o seed
    sucesso = run_seed_permissions_profiles(logger)
    
    if sucesso:
        # Verifica a estrutura created
        print("\n")
        verificar_estrutura(logger)
        print("\n[FASE 1 CONCLUIDA COM SUCESSO]")
    else:
        print("\n[ERRO DURANTE A EXECUCAO DO SEED]")
        exit(1)
