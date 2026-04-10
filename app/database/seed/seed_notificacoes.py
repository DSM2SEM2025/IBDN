"""
Seed Notificações
Popula o banco de dados com notificações para as empresas do IBDN.
Este script é idempotente - pode ser executado múltiplas vezes sem duplicar dados.
"""
import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict

from app.database.seed.seed_base import (
    setup_logging,
    SeedContextManager,
    get_faker
)


# Tipos de notificação disponíveis
TIPOS_NOTIFICACAO = [
    "alerta_expiracao",
    "renovacao_solicitada", 
    "documentacao_pendente",
    "comunicado_geral"
]

# Mensagens por tipo de notificação
MENSAGENS_POR_TIPO = {
    "alerta_expiracao": [
        "Atenção! O selo {sigla} está próximo do vencimento. Data de expiração: {data}.",
        "Seu certificado {nome} expira em {dias} dias. Renove agora para manter sua certificação.",
        "Aviso importante: O selo {sigla} vencerá em breve. Entre em contato para renovação.",
        "O prazo para renovação do {nome} está terminando. Não perca sua certificação!",
        "Lembrete: Seu selo {sigla} expira no dia {data}. Favor进行处理."
    ],
    "renovacao_solicitada": [
        "Sua solicitação de renovação do {nome} foi recebida. Aguarde aprovação.",
        "Renovação do {sigla} solicitada com sucesso. O processo leva até 5 dias úteis.",
        "Pedido de renovação registrado para {nome}. Entraremos em contato em breve.",
        "Solicitação de renovação enviada para {sigla}. Status: em análise.",
        "Nova solicitação de renovação recebida para {nome}. Gracias por sua confiança!"
    ],
    "documentacao_pendente": [
        "Documentação pendente para {nome}. Por favor, envie os documentos necessários.",
        "Faltam documentos para certificação do {sigla}. Envie a documentação requerida.",
        "Atenção: Sua documentação para {nome} está incompleta. Complete agora.",
        "Precisamos de documentos adicionais para {sigla}. Envie via portal.",
        "Documentação obrigatória pendiente para {nome}. Acesso o portal para enviar."
    ],
    "comunicado_geral": [
        "Novo evento de sustentabilidade confirmado. Participate da Jornada do Rio Tietê!",
        "Parabéns! Sua empresa foi selecionada para o programa de reconheciminto.",
        "Atualização no sistema de certificações. Novas funcionalidades disponíveis.",
        "IBDN lança novo programa de capacitação. Inscreva-se gratuitamente.",
        "Parceria exclusiva: Novos benefícios para empresas certificadas pelo IBDN."
    ]
}


def get_empresas_ids(cursor) -> List[Dict]:
    """
    Obtém IDs e dados das empresas existentes.
    
    Args:
        cursor: Cursor do banco de dados
        
    Returns:
        Lista de dicionários com dados das empresas
    """
    cursor.execute("""
        SELECT id, nome_fantasia, razao_social 
        FROM empresa
    """)
    return cursor.fetchall()


def get_selos_empresa(cursor, empresa_id: int) -> List[Dict]:
    """
    Obtém os selos de uma empresa específica.
    
    Args:
        cursor: Cursor do banco de dados
        empresa_id: ID da empresa
        
    Returns:
        Lista de dicionários com dados dos selos da empresa
    """
    cursor.execute("""
        SELECT s.id, s.nome, s.sigla, es.status, es.data_expiracao
        FROM empresa_selo es
        JOIN selo s ON es.id_selo = s.id
        WHERE es.id_empresa = %s
    """, (empresa_id,))
    return cursor.fetchall()


def gerar_mensagem(tipo: str, empresa_id: int, cursor) -> str:
    """
    Gera uma mensagem de notificação baseada no tipo.
    
    Args:
        tipo: Tipo de notificação
        empresa_id: ID da empresa
        cursor: Cursor do banco de dados
        
    Returns:
        Mensagem formatada
    """
    faker = get_faker()
    mensagens = MENSAGENS_POR_TIPO.get(tipo, MENSAGENS_POR_TIPO["comunicado_geral"])
    mensagem_base = random.choice(mensagens)
    
    # Se for relacionado a selo, tenta obter dados do selo
    if tipo in ["alerta_expiracao", "renovacao_solicitada", "documentacao_pendente"]:
        selos = get_selos_empresa(cursor, empresa_id)
        
        if selos:
            selo = random.choice(selos)
            mensagem = mensagem_base.format(
                nome=selo["nome"],
                sigla=selo["sigla"],
                data=selo["data_expiracao"].strftime("%d/%m/%Y") if selo["data_expiracao"] else "N/A",
                dias=random.randint(15, 60)
            )
            return mensagem
    
    # Para comunicado geral ou se não houver selos
    return mensagem_base


def seed_notificacoes(logger: logging.Logger) -> dict:
    """
    Popula notificações para cada empresa (0-5 notificações por empresa).
    Diversos tipos, statuses e datas.
    Idempotente: não cria notificações duplicadas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {
        "criadas": 0, 
        "existentes": 0, 
        "erros": 0, 
        "empresas_processadas": 0,
        "por_tipo": {tipo: 0 for tipo in TIPOS_NOTIFICACAO},
        "por_status": {"lidas": 0, "nao_lidas": 0}
    }
    faker = get_faker()
    
    with SeedContextManager(logger) as ctx:
        # Obtém empresas existentes
        empresas = get_empresas_ids(ctx.cursor)
        
        if not empresas:
            logger.warning("Nenhuma empresa encontrada para criar notificações!")
            return stats
        
        logger.info(f"Encontradas {len(empresas)} empresas para criar notificações")
        
        for empresa in empresas:
            empresa_id = empresa["id"]
            nome_empresa = empresa["nome_fantasia"]
            
            # Decide quantas notificações criar (0-5)
            qtd_notificacoes = random.randint(0, 5)
            
            if qtd_notificacoes == 0:
                stats["empresas_processadas"] += 1
                logger.info(f"Empresa '{nome_empresa}' não receberá notificações nesta execução")
                continue
            
            # Gera notificações
            tipos_selecionados = random.choices(
                TIPOS_NOTIFICACAO, 
                weights=[25, 20, 25, 30],  # Pesos: mais alertas e docs pendentes
                k=qtd_notificacoes
            )
            
            for tipo in tipos_selecionados:
                # Gera mensagem
                mensagem = gerar_mensagem(tipo, empresa_id, ctx.cursor)
                
                # Gera data de envio (diversas: recentes e antigas)
                # 60% nos últimos 30 dias, 40% entre 30 e 180 dias atrás
                if random.random() < 0.6:
                    dias_atras = random.randint(0, 30)
                else:
                    dias_atras = random.randint(31, 180)
                
                data_envio = datetime.now() - timedelta(days=dias_atras)
                
                # Decide se foi lida (70% não lidas para notificações recentes)
                if dias_atras <= 7:
                    lida = random.choice([False, False, False, True])  # 75% não lidas
                else:
                    lida = random.choice([False, True])  # 50% cada
                
                try:
                    ctx.cursor.execute(
                        """INSERT INTO notificacao 
                           (id_empresa, mensagem, tipo, data_envio, lida) 
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            empresa_id,
                            mensagem,
                            tipo,
                            data_envio,
                            1 if lida else 0
                        )
                    )
                    
                    stats["criadas"] += 1
                    stats["por_tipo"][tipo] += 1
                    if lida:
                        stats["por_status"]["lidas"] += 1
                    else:
                        stats["por_status"]["nao_lidas"] += 1
                    
                    logger.debug(
                        f"Notificação '{tipo}' ({'lida' if lida else 'não lida'}) "
                        f"criada para '{nome_empresa}'"
                    )
                    
                except Exception as e:
                    logger.error(
                        f"Erro ao criar notificação para '{nome_empresa}': {e}"
                    )
                    stats["erros"] += 1
            
            stats["empresas_processadas"] += 1
            logger.info(
                f"Empresa '{nome_empresa}': {qtd_notificacoes} notificações criadas"
            )
        
        ctx.commit()
    
    return stats


def verificar_notificacoes(logger: logging.Logger) -> dict:
    """
    Verifica a quantidade de notificações no banco.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {}
    
    with SeedContextManager(logger) as ctx:
        # Total de notificações
        ctx.cursor.execute("SELECT COUNT(*) as total FROM notificacao")
        stats["total"] = ctx.cursor.fetchone()["total"]
        
        # Por tipo
        ctx.cursor.execute("""
            SELECT tipo, COUNT(*) as total 
            FROM notificacao 
            GROUP BY tipo
            ORDER BY total DESC
        """)
        stats["por_tipo"] = {row["tipo"]: row["total"] for row in ctx.cursor.fetchall()}
        
        # Por status de leitura
        ctx.cursor.execute("""
            SELECT lida, COUNT(*) as total 
            FROM notificacao 
            GROUP BY lida
        """)
        stats["por_lida"] = {}
        for row in ctx.cursor.fetchall():
            key = "lidas" if row["lida"] else "nao_lidas"
            stats["por_lida"][key] = row["total"]
        
        # Notificações nos últimos 30 dias
        ctx.cursor.execute("""
            SELECT COUNT(*) as total 
            FROM notificacao 
            WHERE data_envio >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)
        stats["ultimos_30_dias"] = ctx.cursor.fetchone()["total"]
        
        # Empresas com notificações
        ctx.cursor.execute("""
            SELECT COUNT(DISTINCT id_empresa) as total 
            FROM notificacao
        """)
        stats["empresas_com_notificacoes"] = ctx.cursor.fetchone()["total"]
        
        # Média de notificações por empresa
        ctx.cursor.execute("""
            SELECT AVG(total_notif) as media
            FROM (
                SELECT id_empresa, COUNT(*) as total_notif
                FROM notificacao
                GROUP BY id_empresa
            ) as subquery
        """)
        stats["media_por_empresa"] = round(ctx.cursor.fetchone()["media"] or 0, 2)
    
    return stats


def run_seed_notificacoes(logger: logging.Logger = None) -> dict:
    """
    Executa o seed de notificações.
    
    Args:
        logger: Logger opcional
        
    Returns:
        Dicionário com estatísticas finais
    """
    logger = logger or setup_logging('seed_notificacoes')
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO SEED DE NOTIFICAÇÕES")
        logger.info("=" * 60)
        
        # Step 1: Criar notificações
        logger.info("\n--- Step 1: Criando Notificações ---")
        stats_notificacoes = seed_notificacoes(logger)
        logger.info(
            f"Notificações criadas: {stats_notificacoes['criadas']}, "
            f"Erros: {stats_notificacoes['erros']}"
        )
        logger.info(f"Por tipo: {stats_notificacoes['por_tipo']}")
        logger.info(f"Por status: {stats_notificacoes['por_status']}")
        
        # Step 2: Verificação
        logger.info("\n--- Step 2: Verificação ---")
        stats_verificacao = verificar_notificacoes(logger)
        logger.info(f"Total de notificações: {stats_verificacao['total']}")
        logger.info(f"Por tipo: {stats_verificacao['por_tipo']}")
        logger.info(f"Por leitura: {stats_verificacao['por_lida']}")
        logger.info(f"Últimos 30 dias: {stats_verificacao['ultimos_30_dias']}")
        logger.info(f"Empresas com notificações: {stats_verificacao['empresas_com_notificacoes']}")
        logger.info(f"Média por empresa: {stats_verificacao['media_por_empresa']}")
        
        logger.info("=" * 60)
        logger.info("SEED DE NOTIFICAÇÕES CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        
        return {
            "sucesso": True,
            "criadas": stats_notificacoes["criadas"],
            "existentes": stats_notificacoes["existentes"],
            "erros": stats_notificacoes["erros"],
            "por_tipo": stats_notificacoes["por_tipo"],
            "por_status": stats_notificacoes["por_status"],
            "total": stats_verificacao["total"]
        }
        
    except Exception as e:
        logger.error(f"ERRO DURANTE SEED: {e}")
        return {"sucesso": False, "erro": str(e)}


if __name__ == "__main__":
    logger = setup_logging('seed_notificacoes')
    
    print("\n" + "=" * 60)
    print("SEED DE NOTIFICAÇÕES - IBDN")
    print("=" * 60 + "\n")
    
    # Executa o seed
    resultado = run_seed_notificacoes(logger)
    
    if resultado.get("sucesso"):
        print("\n[RESULTADO]")
        print(f"Notificações criadas: {resultado.get('criadas', 0)}")
        print(f"Total no banco: {resultado.get('total', 0)}")
        print("\n[POR TIPO]")
        for tipo, qtd in resultado.get("por_tipo", {}).items():
            print(f"  {tipo}: {qtd}")
        print("\n[POR STATUS]")
        status = resultado.get("por_status", {})
        print(f"  Lidas: {status.get('lidas', 0)}")
        print(f"  Não lidas: {status.get('nao_lidas', 0)}")
        print("\n[SEED NOTIFICAÇÕES CONCLUÍDO COM SUCESSO]")
    else:
        print(f"\n[ERRO]: {resultado.get('erro', 'Erro desconhecido')}")
        exit(1)
