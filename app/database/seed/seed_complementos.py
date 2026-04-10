"""
Seed Módulos Complementares
Popula o banco de dados com endereços, associações empresa_ramo e empresa_selo para o IBDN.
Este script é idempotente - pode ser executado múltiplas vezes sem duplicar dados.
"""
import logging
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict

from app.database.seed.seed_base import (
    setup_logging,
    SeedContextManager,
    get_faker
)


# Dados brasileiros para endereços
BRASIL_ESTADOS = [
    {"uf": "AC", "nome": "Acre", "cidades": ["Rio Branco", "Cruzeiro do Sul", "Sena Madureira"]},
    {"uf": "AL", "nome": "Alagoas", "cidades": ["Maceió", "Arapiraca", " Palmeira dos Índias"]},
    {"uf": "AP", "nome": "Amapá", "cidades": ["Macapá", "Santana", "Laranjal do Jari"]},
    {"uf": "AM", "nome": "Amazonas", "cidades": ["Manaus", "Parintins", "Itacoatiara"]},
    {"uf": "BA", "nome": "Bahia", "cidades": ["Salvador", "Feira de Santana", "Vitória da Conquista"]},
    {"uf": "CE", "nome": "Ceará", "cidades": ["Fortaleza", "Caucaia", "Juazeiro do Norte"]},
    {"uf": "DF", "nome": "Distrito Federal", "cidades": ["Brasília", "Taguatinga", "Asa Sul"]},
    {"uf": "ES", "nome": "Espírito Santo", "cidades": ["Vitória", "Vila Velha", "Cachoeiro de Itapemirim"]},
    {"uf": "GO", "nome": "Goiás", "cidades": ["Goiânia", "Anápolis", "Rio Verde"]},
    {"uf": "MA", "nome": "Maranhão", "cidades": ["São Luís", "Imperatriz", "São José de Ribamar"]},
    {"uf": "MT", "nome": "Mato Grosso", "cidades": ["Cuiabá", "Várzea Grande", "Rondonópolis"]},
    {"uf": "MS", "nome": "Mato Grosso do Sul", "cidades": ["Campo Grande", "Dourados", "Três Lagoas"]},
    {"uf": "MG", "nome": "Minas Gerais", "cidades": ["Belo Horizonte", "Uberlândia", "Contagem"]},
    {"uf": "PA", "nome": "Pará", "cidades": ["Belém", "Ananindeua", "Santarém"]},
    {"uf": "PB", "nome": "Paraíba", "cidades": ["João Pessoa", "Campina Grande", "Santa Rita"]},
    {"uf": "PR", "nome": "Paraná", "cidades": ["Curitiba", "Londrina", "Maringá"]},
    {"uf": "PE", "nome": "Pernambuco", "cidades": ["Recife", "Caruaru", "Petrolina"]},
    {"uf": "PI", "nome": "Piauí", "cidades": ["Teresina", "Parnaíba", "Floriano"]},
    {"uf": "RJ", "nome": "Rio de Janeiro", "cidades": ["Rio de Janeiro", "Niterói", "São Gonçalo"]},
    {"uf": "RN", "nome": "Rio Grande do Norte", "cidades": ["Natal", "Mossoró", "Parnamirim"]},
    {"uf": "RS", "nome": "Rio Grande do Sul", "cidades": ["Porto Alegre", "Caxias do Sul", "Pelotas"]},
    {"uf": "RO", "nome": "Rondônia", "cidades": ["Porto Velho", "Ji-Paraná", "Ariquemes"]},
    {"uf": "RR", "nome": "Roraima", "cidades": ["Boa Vista", "Rorainópolis", "Caracaraí"]},
    {"uf": "SC", "nome": "Santa Catarina", "cidades": ["Florianópolis", "Joinville", "Blumenau"]},
    {"uf": "SP", "nome": "São Paulo", "cidades": ["São Paulo", "Campinas", "Santos"]},
    {"uf": "SE", "nome": "Sergipe", "cidades": ["Aracaju", "Nossa Senhora do Socorro", "Lagarto"]},
    {"uf": "TO", "nome": "Tocantins", "cidades": ["Palmas", "Araguaína", "Gurupi"]}
]

# Tipos de logradouro brasileiros
TIPOS_LOGRADOURO = [
    "Rua", "Avenida", "Praça", "Estrada", "Rodovia", "Alameda", 
    "Travessa", "Boulevard", "Via", "Passagem"
]

# Tipos de complemento brasileiros
TIPOS_COMPLEMENTO = [
    "Sala", "Andar", "Bloco", "Anexo", "Ala", "Casa", "Apartamento",
    "Galpão", "Warehouse", "Pavilhão", None
]


def gerar_cep_valido() -> str:
    """Gera um CEP brasileiro válido no formato XXXXX-XXX."""
    return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"


def gerar_codigo_selo() -> str:
    """Gera um código único para selo (formato: EPN-XXXX-XXXXX)."""
    letras = ''.join(random.choices(string.ascii_uppercase, k=4))
    numeros = ''.join(random.choices(string.digits, k=5))
    return f"{letras}-{numeros}"


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


def get_ramos_ids(cursor) -> List[Dict]:
    """
    Obtém IDs dos ramos existentes.
    
    Args:
        cursor: Cursor do banco de dados
        
    Returns:
        Lista de dicionários com dados dos ramos
    """
    cursor.execute("SELECT id, nome FROM ramo")
    return cursor.fetchall()


def get_selos_ids(cursor) -> List[Dict]:
    """
    Obtém IDs dos selos existentes.
    
    Args:
        cursor: Cursor do banco de dados
        
    Returns:
        Lista de dicionários com dados dos selos
    """
    cursor.execute("SELECT id, nome, sigla FROM selo")
    return cursor.fetchall()


def seed_enderecos(logger: logging.Logger) -> dict:
    """
    Popula endereços para cada empresa (1-3 endereços por empresa).
    Idempotente: não cria endereços duplicados.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criados": 0, "existentes": 0, "erros": 0, "empresas_processadas": 0}
    faker = get_faker()
    
    with SeedContextManager(logger) as ctx:
        # Obtém empresas existentes
        empresas = get_empresas_ids(ctx.cursor)
        
        if not empresas:
            logger.warning("Nenhuma empresa encontrada para criar endereços!")
            return stats
        
        logger.info(f"Encontradas {len(empresas)} empresas para criar endereços")
        
        for empresa in empresas:
            empresa_id = empresa["id"]
            nome_empresa = empresa["nome_fantasia"]
            
            # Verifica quantos endereços a empresa já tem
            ctx.cursor.execute(
                "SELECT COUNT(*) as total FROM endereco WHERE id_empresa = %s",
                (empresa_id,)
            )
            enderecos_existentes = ctx.cursor.fetchone()["total"]
            
            # Decide quantos endereços criar (1-3, subtraindo os existentes)
            max_enderecos = random.randint(1, 3)
            enderecos_a_criar = max(0, max_enderecos - enderecos_existentes)
            
            if enderecos_a_criar == 0:
                stats["existentes"] += enderecos_existentes
                stats["empresas_processadas"] += 1
                logger.info(f"Empresa '{nome_empresa}' já tem {enderecos_existentes} endereços, pulando...")
                continue
            
            for _ in range(enderecos_a_criar):
                # Gera dados de endereço brasileiro
                tipo_logradouro = random.choice(TIPOS_LOGRADOURO)
                nome_logradouro = faker.street_name()
                logradouro = f"{tipo_logradouro} {nome_logradouro}"
                
                numero = faker.building_number()
                bairro = faker.bairro()
                cep = gerar_cep_valido()
                
                # Seleciona estado e cidade
                estado = random.choice(BRASIL_ESTADOS)
                uf = estado["uf"]
                cidade = random.choice(estado["cidades"])
                
                # Gera complemento (70% de chance)
                complemento = None
                if random.random() < 0.7:
                    tipo_comp = random.choice(TIPOS_COMPLEMENTO)
                    if tipo_comp:
                        complemento = f"{tipo_comp} {random.randint(1, 50)}"
                
                try:
                    ctx.cursor.execute(
                        """INSERT INTO endereco 
                           (id_empresa, logradouro, numero, bairro, cep, cidade, uf, complemento) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            empresa_id,
                            logradouro,
                            numero,
                            bairro,
                            cep,
                            cidade,
                            uf,
                            complemento
                        )
                    )
                    stats["criados"] += 1
                    
                except Exception as e:
                    logger.error(f"Erro ao criar endereço para '{nome_empresa}': {e}")
                    stats["erros"] += 1
            
            stats["empresas_processadas"] += 1
            logger.info(
                f"Empresa '{nome_empresa}': {enderecos_a_criar} endereços criados "
                f"(total: {enderecos_existentes + enderecos_a_criar})"
            )
        
        ctx.commit()
    
    return stats


def seed_empresa_ramo(logger: logging.Logger) -> dict:
    """
    Popula associações entre empresas e ramos (1-3 ramos por empresa).
    Idempotente: não cria associações duplicadas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {"criadas": 0, "existentes": 0, "erros": 0, "empresas_processadas": 0}
    
    with SeedContextManager(logger) as ctx:
        # Obtém empresas e ramos
        empresas = get_empresas_ids(ctx.cursor)
        ramos = get_ramos_ids(ctx.cursor)
        
        if not empresas:
            logger.warning("Nenhuma empresa encontrada para associar ramos!")
            return stats
        
        if not ramos:
            logger.warning("Nenhum ramo encontrado para associar!")
            return stats
        
        logger.info(f"Encontradas {len(empresas)} empresas e {len(ramos)} ramos")
        
        for empresa in empresas:
            empresa_id = empresa["id"]
            nome_empresa = empresa["nome_fantasia"]
            
            # Verifica quantos ramos a empresa já tem
            ctx.cursor.execute(
                "SELECT COUNT(*) as total FROM empresa_ramo WHERE id_empresa = %s",
                (empresa_id,)
            )
            ramos_existentes = ctx.cursor.fetchone()["total"]
            
            # Decide quantos ramos associar (1-3)
            max_ramos = random.randint(1, 3)
            ramos_a_associar = max(0, max_ramos - ramos_existentes)
            
            if ramos_a_associar == 0:
                stats["existentes"] += ramos_existentes
                stats["empresas_processadas"] += 1
                logger.info(f"Empresa '{nome_empresa}' já tem {ramos_existentes} ramos, pulando...")
                continue
            
            # Seleciona ramos aleatórios disponíveis
            ramos_disponiveis = random.sample(ramos, min(ramos_a_associar, len(ramos)))
            
            for ramo in ramos_disponiveis:
                id_ramo = ramo["id"]
                nome_ramo = ramo["nome"]
                
                # Verifica se já existe a associação
                ctx.cursor.execute(
                    """SELECT 1 FROM empresa_ramo 
                       WHERE id_empresa = %s AND id_ramo = %s""",
                    (empresa_id, id_ramo)
                )
                
                if ctx.cursor.fetchone():
                    stats["existentes"] += 1
                    continue
                
                try:
                    ctx.cursor.execute(
                        """INSERT INTO empresa_ramo (id_empresa, id_ramo) 
                           VALUES (%s, %s)""",
                        (empresa_id, id_ramo)
                    )
                    stats["criadas"] += 1
                    logger.info(
                        f"Associação criada: empresa '{nome_empresa}' <-> ramo '{nome_ramo}'"
                    )
                    
                except Exception as e:
                    logger.error(
                        f"Erro ao associar ramo '{nome_ramo}' à empresa '{nome_empresa}': {e}"
                    )
                    stats["erros"] += 1
            
            stats["empresas_processadas"] += 1
        
        ctx.commit()
    
    return stats


def seed_empresa_selo(logger: logging.Logger) -> dict:
    """
    Popula certificações de selos para empresas.
    Diversos statuses: ativos, expirados, pendentes.
    Idempotente: não cria certificações duplicadas.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {
        "ativos": 0, 
        "expirados": 0, 
        "pendentes": 0, 
        "erros": 0, 
        "empresas_processadas": 0
    }
    
    with SeedContextManager(logger) as ctx:
        # Obtém empresas e selos
        empresas = get_empresas_ids(ctx.cursor)
        selos = get_selos_ids(ctx.cursor)
        
        if not empresas:
            logger.warning("Nenhuma empresa encontrada para associar selos!")
            return stats
        
        if not selos:
            logger.warning("Nenhum selo encontrado para associar!")
            return stats
        
        logger.info(f"Encontradas {len(empresas)} empresas e {len(selos)} selos")
        
        for empresa in empresas:
            empresa_id = empresa["id"]
            nome_empresa = empresa["nome_fantasia"]
            
            # Decide quantos selos associar (1-3)
            qtd_selos = random.randint(1, 3)
            
            # Seleciona selos aleatórios
            selos_selecionados = random.sample(selos, min(qtd_selos, len(selos)))
            
            for i, selo in enumerate(selos_selecionados):
                id_selo = selo["id"]
                nome_selo = selo["nome"]
                sigla_selo = selo["sigla"]
                
                # Verifica se já existe a certificação para esta empresa+selo
                ctx.cursor.execute(
                    """SELECT id FROM empresa_selo 
                       WHERE id_empresa = %s AND id_selo = %s""",
                    (empresa_id, id_selo)
                )
                
                if ctx.cursor.fetchone():
                    stats["existentes"] = stats.get("existentes", 0) + 1
                    continue
                
                # Decide o status (40% ativo, 30% expirado, 30% pendente)
                rand_status = random.random()
                if rand_status < 0.4:
                    status = "ativo"
                    data_emissao = datetime.now() - timedelta(days=random.randint(30, 180))
                    # Ativo: data_expiracao entre 30 dias no futuro e 1 ano
                    data_expiracao = data_emissao + timedelta(days=random.randint(30, 365))
                    codigo_selo = gerar_codigo_selo()
                    dias_alerta_previo = random.choice([15, 30, 45, 60])
                    plano_anos = random.choice([1, 2])
                    
                elif rand_status < 0.7:
                    status = "expirado"
                    # Expirado: data_expiracao no passado (30 a 365 dias atrás)
                    data_expiracao = datetime.now() - timedelta(days=random.randint(30, 365))
                    data_emissao = data_expiracao - timedelta(days=random.randint(180, 365))
                    codigo_selo = gerar_codigo_selo()
                    dias_alerta_previo = None
                    plano_anos = random.choice([1, 2])
                    
                else:
                    status = "pendente"
                    data_emissao = None
                    data_expiracao = None
                    codigo_selo = None
                    dias_alerta_previo = None
                    plano_anos = random.choice([1, 2])
                
                try:
                    ctx.cursor.execute(
                        """INSERT INTO empresa_selo 
                           (id_empresa, id_selo, status, data_emissao, data_expiracao, 
                            codigo_selo, dias_alerta_previo, plano_solicitado_anos) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            empresa_id,
                            id_selo,
                            status,
                            data_emissao.date() if data_emissao else None,
                            data_expiracao.date() if data_expiracao else None,
                            codigo_selo,
                            dias_alerta_previo,
                            plano_anos
                        )
                    )
                    
                    if status == "ativo":
                        stats["ativos"] += 1
                    elif status == "expirado":
                        stats["expirados"] += 1
                    else:
                        stats["pendentes"] += 1
                    
                    logger.info(
                        f"Selo '{sigla_selo}' ({status}) criado para empresa '{nome_empresa}'"
                    )
                    
                except Exception as e:
                    logger.error(
                        f"Erro ao associar selo '{nome_selo}' à empresa '{nome_empresa}': {e}"
                    )
                    stats["erros"] += 1
            
            stats["empresas_processadas"] += 1
            logger.info(f"Empresa '{nome_empresa}': {qtd_selos} selos processados")
        
        ctx.commit()
    
    return stats


def verificar_complementos(logger: logging.Logger) -> dict:
    """
    Verifica a quantidade de registros nas tabelas complementares.
    
    Args:
        logger: Logger para mensagens
        
    Returns:
        Dicionário com contagens
    """
    stats = {}
    
    with SeedContextManager(logger) as ctx:
        # Endereços
        ctx.cursor.execute("SELECT COUNT(*) as total FROM endereco")
        stats["enderecos_total"] = ctx.cursor.fetchone()["total"]
        
        # Empresas por quantidade de endereços
        ctx.cursor.execute("""
            SELECT 
                CASE 
                    WHEN total_enderecos = 1 THEN '1_endereco'
                    WHEN total_enderecos = 2 THEN '2_enderecos'
                    WHEN total_enderecos >= 3 THEN '3+_enderecos'
                    ELSE 'sem_endereco'
                END as faixa,
                COUNT(*) as total
            FROM (
                SELECT id_empresa, COUNT(*) as total_enderecos
                FROM endereco
                GROUP BY id_empresa
            ) as subquery
            GROUP BY faixa
        """)
        stats["enderecos_por_faixa"] = {row["faixa"]: row["total"] for row in ctx.cursor.fetchall()}
        
        # Empresa-Ramo
        ctx.cursor.execute("SELECT COUNT(*) as total FROM empresa_selo")
        stats["empresa_ramo_total"] = ctx.cursor.fetchone()["total"]
        
        # Empresa-Selo por status
        ctx.cursor.execute("""
            SELECT status, COUNT(*) as total 
            FROM empresa_selo 
            GROUP BY status
        """)
        stats["selos_por_status"] = {row["status"]: row["total"] for row in ctx.cursor.fetchall()}
        
        # Empresas com selos ativos
        ctx.cursor.execute("""
            SELECT COUNT(DISTINCT id_empresa) as total 
            FROM empresa_selo 
            WHERE status = 'ativo'
        """)
        stats["empresas_com_selos_ativos"] = ctx.cursor.fetchone()["total"]
    
    return stats


def run_seed_complementos(logger: logging.Logger = None) -> dict:
    """
    Executa o seed completo dos módulos complementares.
    
    Args:
        logger: Logger opcional
        
    Returns:
        Dicionário com estatísticas finais
    """
    logger = logger or setup_logging('seed_complementos')
    
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO SEED DE MÓDULOS COMPLEMENTARES")
        logger.info("=" * 60)
        
        # Step 1: Endereços
        logger.info("\n--- Step 1: Criando Endereços ---")
        stats_enderecos = seed_enderecos(logger)
        logger.info(
            f"Endereços: {stats_enderecos['criados']} criados, "
            f"{stats_enderecos['existentes']} existentes, {stats_enderecos['erros']} erros"
        )
        
        # Step 2: Empresa-Ramo
        logger.info("\n--- Step 2: Associando Empresas a Ramos ---")
        stats_empresa_ramo = seed_empresa_ramo(logger)
        logger.info(
            f"Associações: {stats_empresa_ramo['criadas']} criadas, "
            f"{stats_empresa_ramo['existentes']} existentes, {stats_empresa_ramo['erros']} erros"
        )
        
        # Step 3: Empresa-Selo
        logger.info("\n--- Step 3: Associando Selos às Empresas ---")
        stats_empresa_selo = seed_empresa_selo(logger)
        logger.info(
            f"Selos Ativos: {stats_empresa_selo['ativos']}, "
            f"Selos Expirados: {stats_empresa_selo['expirados']}, "
            f"Selos Pendentes: {stats_empresa_selo['pendentes']}, "
            f"Erros: {stats_empresa_selo['erros']}"
        )
        
        # Step 4: Verificação
        logger.info("\n--- Step 4: Verificação ---")
        stats_verificacao = verificar_complementos(logger)
        logger.info(f"Total de endereços: {stats_verificacao['enderecos_total']}")
        logger.info(f"Endereços por faixa: {stats_verificacao['enderecos_por_faixa']}")
        logger.info(f"Total de associações empresa_ramo: {stats_verificacao['empresa_ramo_total']}")
        logger.info(f"Selos por status: {stats_verificacao['selos_por_status']}")
        logger.info(f"Empresas com selos ativos: {stats_verificacao['empresas_com_selos_ativos']}")
        
        logger.info("=" * 60)
        logger.info("SEED DE MÓDULOS COMPLEMENTARES CONCLUÍDO COM SUCESSO!")
        logger.info("=" * 60)
        
        return {
            "sucesso": True,
            "enderecos": {
                "criados": stats_enderecos["criados"],
                "existentes": stats_enderecos["existentes"],
                "total": stats_verificacao["enderecos_total"]
            },
            "empresa_ramo": {
                "criadas": stats_empresa_ramo["criadas"],
                "existentes": stats_empresa_ramo["existentes"],
                "total": stats_verificacao["empresa_ramo_total"]
            },
            "empresa_selo": {
                "ativos": stats_empresa_selo["ativos"],
                "expirados": stats_empresa_selo["expirados"],
                "pendentes": stats_empresa_selo["pendentes"],
                "total": sum([
                    stats_empresa_selo["ativos"],
                    stats_empresa_selo["expirados"],
                    stats_empresa_selo["pendentes"]
                ])
            }
        }
        
    except Exception as e:
        logger.error(f"ERRO DURANTE SEED: {e}")
        return {"sucesso": False, "erro": str(e)}


if __name__ == "__main__":
    logger = setup_logging('seed_complementos')
    
    print("\n" + "=" * 60)
    print("SEED DE MÓDULOS COMPLEMENTARES - IBDN")
    print("=" * 60 + "\n")
    
    # Executa o seed
    resultado = run_seed_complementos(logger)
    
    if resultado.get("sucesso"):
        print("\n[RESULTADO]")
        print(f"Endereços criados: {resultado.get('enderecos', {}).get('criados', 0)}")
        print(f"Associações empresa_ramo criadas: {resultado.get('empresa_ramo', {}).get('criadas', 0)}")
        print(f"Selos ativos: {resultado.get('empresa_selo', {}).get('ativos', 0)}")
        print(f"Selos expirados: {resultado.get('empresa_selo', {}).get('expirados', 0)}")
        print(f"Selos pendentes: {resultado.get('empresa_selo', {}).get('pendentes', 0)}")
        print("\n[FASE 3 - MÓDULOS COMPLEMENTARES CONCLUÍDA COM SUCESSO]")
    else:
        print(f"\n[ERRO]: {resultado.get('erro', 'Erro desconhecido')}")
        exit(1)
