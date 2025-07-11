import logging
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from app.database.config import get_db_config
from app.security.password import get_password_hash
from uuid import uuid4

load_dotenv(override=True)


def setup_logging():
    
    log_dir = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'database.log')
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('database_setup')


def create_tables():
    logger = setup_logging()
    logger.info("Iniciando a criação das tabelas do banco de dados")
    connection = None
    try:
        config = get_db_config()
        logger.info("Conectando ao banco de dados...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        tables = {}

        tables['ibdn_permissoes'] = """
            CREATE TABLE IF NOT EXISTS ibdn_permissoes (
                id CHAR(40) PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE
            ) ENGINE=InnoDB;
        """
        tables['ibdn_perfis'] = """
            CREATE TABLE IF NOT EXISTS ibdn_perfis (
                id CHAR(40) PRIMARY KEY,
                nome VARCHAR(50) NOT NULL UNIQUE
            ) ENGINE=InnoDB;
        """
        tables['ibdn_perfil_permissoes'] = """
            CREATE TABLE IF NOT EXISTS ibdn_perfil_permissoes (
                perfil_id CHAR(40),
                permissao_id CHAR(40),
                PRIMARY KEY (perfil_id, permissao_id),
                FOREIGN KEY (perfil_id) REFERENCES ibdn_perfis(id) ON DELETE CASCADE,
                FOREIGN KEY (permissao_id) REFERENCES ibdn_permissoes(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """
        tables['ibdn_usuarios'] = """
            CREATE TABLE IF NOT EXISTS ibdn_usuarios (
                id CHAR(40) PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                senha_hash VARCHAR(255) NOT NULL,
                perfil_id CHAR(40) NULL,
                ativo TINYINT(1) DEFAULT 1,
                twofactor TINYINT(1) DEFAULT 0,
                FOREIGN KEY (perfil_id) REFERENCES ibdn_perfis(id) ON DELETE SET NULL
            ) ENGINE=InnoDB;
        """

        tables['empresa'] = """
        CREATE TABLE IF NOT EXISTS empresa (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cnpj VARCHAR(18) NOT NULL UNIQUE,
            razao_social VARCHAR(255) NOT NULL,
            nome_fantasia VARCHAR(255),
            usuario_id CHAR(40) NOT NULL UNIQUE,
            telefone VARCHAR(20),
            responsavel VARCHAR(100),
            cargo_responsavel VARCHAR(100),
            site VARCHAR(255),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (usuario_id) REFERENCES ibdn_usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        tables['empresa_ramo'] = """
        CREATE TABLE IF NOT EXISTS empresa_ramo (
            id_empresa INT NOT NULL,
            id_ramo INT NOT NULL,
            PRIMARY KEY (id_empresa, id_ramo),
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
            FOREIGN KEY (id_ramo) REFERENCES ramo(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
        tables['empresa_selo'] = """
            CREATE TABLE IF NOT EXISTS empresa_selo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_empresa INT NOT NULL,
                id_selo INT NOT NULL,
                status VARCHAR(20),
                data_emissao DATE,
                data_expiracao DATE,
                codigo_selo VARCHAR(50) UNIQUE,
                documentacao TEXT,
                alerta_enviado BOOLEAN,
                dias_alerta_previo INT,
                plano_solicitado_anos INT,
                FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
                FOREIGN KEY (id_selo) REFERENCES selo(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """
        tables['selo'] = """
            CREATE TABLE IF NOT EXISTS selo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE,
                sigla VARCHAR(3) NOT NULL UNIQUE,
                descricao TEXT
            ) ENGINE=InnoDB;
        """
        tables['ramo'] = """
            CREATE TABLE IF NOT EXISTS ramo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE,
                descricao TEXT
            ) ENGINE=InnoDB;
        """

        tables['endereco'] = """
            CREATE TABLE IF NOT EXISTS endereco (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_empresa INT NOT NULL,
                logradouro VARCHAR(255) NOT NULL,
                numero VARCHAR(20) NOT NULL,
                bairro VARCHAR(100) NOT NULL,
                cep VARCHAR(10) NOT NULL,
                cidade VARCHAR(100) NOT NULL,
                uf VARCHAR(2) NOT NULL,
                complemento VARCHAR(255),
                FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """



        tables['notificacao'] = """
            CREATE TABLE IF NOT EXISTS notificacao (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_empresa INT NOT NULL,
                mensagem TEXT NOT NULL,
                data_envio DATETIME NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                lida BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """

        table_creation_order = [
            'ibdn_permissoes', 'ibdn_perfis', 'ramo', 'selo',
            'ibdn_perfil_permissoes', 'ibdn_usuarios', 
            'empresa', 
            'endereco', 'empresa_ramo', 'notificacao', 'empresa_selo'
        ]

        logger.info("Iniciando a criação das tabelas na ordem correta...")
        for table_name in table_creation_order:
            if table_name in tables:
                logger.info(f"Criando/Verificando tabela: {table_name}...")
                cursor.execute(tables[table_name])
            else:
                logger.warning(
                    f"Definição para a tabela '{table_name}' não encontrada. Pulando.")

        logger.info("Todas as tabelas foram criadas/verificadas com sucesso!")
        connection.commit()

    except Error as e:
        logger.error(f"ERRO AO CRIAR TABELAS: {e}")
        if connection:
            connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("Conexão com MySQL foi fechada.")


def create_database_if_not_exists():
    logger = setup_logging()
    logger.info("Verificando se o banco de dados existe...")
    connection = None
    try:
        config = get_db_config()
        db_name = config.pop('database')

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        logger.info(f"Criando banco de dados '{db_name}' se não existir...")
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        logger.info(f"Banco de dados '{db_name}' pronto para uso.")

    except Error as e:
        logger.error(f"ERRO AO CRIAR BANCO DE DADOS: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


def create_initial_data():
    logger = setup_logging()
    logger.info("Verificando/Configurando dados iniciais...")

    connection = None
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        perfis_padrao = ["admin", "empresa", "admin_master"]
        for nome_perfil in perfis_padrao:
            cursor.execute(
                "SELECT id FROM ibdn_perfis WHERE nome = %s", (nome_perfil,))
            if not cursor.fetchone():
                logger.info(f"Criando perfil '{nome_perfil}'...")
                cursor.execute(
                    "INSERT INTO ibdn_perfis (id, nome) VALUES (%s, %s)", (str(uuid4()), nome_perfil))

        
        permissoes_padrao = ["admin", "empresa", "admin_master"]
        for nome_permissao in permissoes_padrao:
            cursor.execute(
                "SELECT id FROM ibdn_permissoes WHERE nome = %s", (nome_permissao,))
            if not cursor.fetchone():
                logger.info(f"Criando permissão '{nome_permissao}'...")
                cursor.execute("INSERT INTO ibdn_permissoes (id, nome) VALUES (%s, %s)", (str(
                    uuid4()), nome_permissao))

        connection.commit()

        perfis_e_permissoes = {
            "admin_master": ["admin_master"],
            "admin": ["admin"],
            "empresa": ["empresa"]
        }

        for nome_perfil, permissoes_perfil in perfis_e_permissoes.items():
            cursor.execute(
                "SELECT id FROM ibdn_perfis WHERE nome = %s", (nome_perfil,))
            perfil_id = cursor.fetchone()['id']

            for nome_permissao in permissoes_perfil:
                cursor.execute(
                    "SELECT id FROM ibdn_permissoes WHERE nome = %s", (nome_permissao,))
                permissao_id = cursor.fetchone()['id']

                cursor.execute(
                    "SELECT 1 FROM ibdn_perfil_permissoes WHERE perfil_id = %s AND permissao_id = %s", (perfil_id, permissao_id))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)", (perfil_id, permissao_id))
                    logger.info(
                        f"Permissão '{nome_permissao}' associada ao perfil '{nome_perfil}'.")

        connection.commit()
        
        logger.info("Verificando/Configurando ramos iniciais...")
        ramos_iniciais = [
            {"nome": "Hotelaria e Turismo", "descricao": 'Hotéis, pousadas e resorts que buscam a certificação "Hotel Eco Responsável (HER)", focada em redução de consumo de água, energia e gestão de resíduos. Exemplo: Cocriação de alternativas para minimizar impactos ambientais em estabelecimentos hoteleiros 1.'},
            {"nome": "Logística e Transporte", "descricao": 'Empresas de gestão de frotas e transporte que neutralizam emissões de carbono, como a Maestro Frotas, certificada como "Neutra em Carbono" pelo IBDN 1.'},
            {"nome": "Agronegócio e Eventos Rurais", "descricao": "Eventos agropecuários (ex.: Rodeio Crioulo Internacional de Imbé) e propriedades rurais que compensam emissões de GEE por meio de reflorestamento ou outras ações sustentáveis 1."},
            {"nome": "Alimentos e Bebidas", "descricao": "Marcas como Café Pilão, que mantêm parcerias de longo prazo com o IBDN para ações socioambientais, incluindo redução de impacto em embalagens e cadeia produtiva 1."},
            {"nome": "Energia e Sustentabilidade", "descricao": 'Empresas que adotam energias renováveis (solar, eólica) e buscam selos como "Energia Renovável" ou "Neutro em Carbono" para validar suas práticas 1.'},
            {"nome": "Educação e Conscientização Ambiental", "descricao": "Escolas, universidades e projetos educacionais que participam de programas do IBDN, como distribuição de cartilhas e palestras sobre sustentabilidade (ex.: Jornada do Rio Tietê com alunos de Itapevi) 11."},
            {"nome": "Construção Civil e Imobiliário", "descricao": "Construtoras e empreendimentos que implementam eficiência energética, gestão de resíduos e outras práticas para obter certificações ambientais 1."},
            {"nome": "Marketing e Comunicação", "descricao": 'Agências e empresas de comunicação que adquirem selos como "Empresa Parceira da Natureza" para reforçar sua imagem sustentável perante clientes 1.'},
            {"nome": "Setor Público e Políticas Ambientais", "descricao": "Governos e entidades públicas que colaboram com o IBDN em projetos de revitalização (ex.: participação em eventos como a Jornada do Rio Tietê) 11."},
            {"nome": "Tecnologia e Serviços", "descricao": "Empresas de TI e consultoria que alinham operações aos ODS da ONU, utilizando certificações do IBDN como diferencial competitivo 1."}
        ]

        for ramo in ramos_iniciais:
            cursor.execute("SELECT id FROM ramo WHERE nome = %s", (ramo['nome'],))
            if not cursor.fetchone():
                logger.info(f"Criando ramo '{ramo['nome']}'...")
                cursor.execute(
                    "INSERT INTO ramo (nome, descricao) VALUES (%s, %s)",
                    (ramo['nome'], ramo['descricao'])
                )
        connection.commit()
        logger.info("Ramos iniciais configurados.")

        logger.info("Verificando/Configurando selos iniciais...")
        selos_iniciais = [
            {"nome": "Empresa Parceira da Natureza", "sigla": "EPN", "descricao": "Certifica empresas comprometidas com práticas sustentáveis, alinhadas aos ODS da ONU e critérios ESG. Inclui gestão de resíduos e educação ambiental 1."},
            {"nome": "Neutro de Carbono", "sigla": "NC", "descricao": "Atesta a neutralização de emissões de GEE (Gases de Efeito Estufa) por meio de compensação, como reflorestamento ou projetos de energia limpa 1."},
            {"nome": "Produto ECO Sustentável", "sigla": "PES", "descricao": "Certifica produtos com ciclo de vida sustentável, desde matérias-primas até descarte, seguindo normas como ISO 14024 1."},
            {"nome": "Hotel ECO Responsável", "sigla": "HER", "descricao": "Selo exclusivo para meios de hospedagem que reduzem impactos ambientais (água, energia e resíduos) 1."},
            {"nome": "Energia Renovável", "sigla": "ER", "descricao": "Reconhece empresas que utilizam fontes renováveis (solar, eólica, biomassa) em suas operações 1."},
            {"nome": "Carbono Cidadão", "sigla": "CC", "descricao": "Certificação individual para pessoas ou pequenos negócios que neutralizam suas emissões de carbono 1."}
        ]
        
        for selo in selos_iniciais:
            cursor.execute("SELECT id FROM selo WHERE sigla = %s", (selo['sigla'],))
            if not cursor.fetchone():
                logger.info(f"Criando selo '{selo['nome']}' ({selo['sigla']})...")
                cursor.execute(
                    "INSERT INTO selo (nome, sigla, descricao) VALUES (%s, %s, %s)",
                    (selo['nome'], selo['sigla'], selo['descricao'])
                )
        connection.commit()
        logger.info("Selos iniciais configurados.")
        # <<< FIM DA NOVA SEÇÃO >>>

        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not admin_email or not admin_password:
            logger.warning(
                "Variáveis ADMIN_EMAIL e ADMIN_PASSWORD não configuradas. Admin master não será criado.")
            return

        cursor.execute(
            "SELECT id FROM ibdn_usuarios WHERE email = %s", (admin_email,))
        if not cursor.fetchone():
            logger.info(
                f"Criando usuário admin_master com email {admin_email}...")
            usuario_id = str(uuid4())
            senha_hash = get_password_hash(admin_password)

            cursor.execute(
                "SELECT id FROM ibdn_perfis WHERE nome = 'admin_master'")
            perfil_master_id = cursor.fetchone()['id']

            query = "INSERT INTO ibdn_usuarios (id, nome, email, senha_hash, perfil_id, ativo) VALUES (%s, %s, %s, %s, %s, 1)"
            cursor.execute(query, (usuario_id, 'Admin Master',
                                   admin_email, senha_hash, perfil_master_id))
            logger.info(
                f"Usuário admin_master criado com sucesso! ID: {usuario_id}")
            connection.commit()
        else:
            logger.info(
                f"Usuário admin_master com email {admin_email} já existe.")

    except Error as e:
        logger.error(f"Erro durante a configuração dos dados iniciais: {e}")
        if connection:
            connection.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    try:
        create_database_if_not_exists()
        create_tables()
        create_initial_data()
        print("\nScript de inicialização do banco de dados concluído com sucesso.")
    except Exception as e:
        print(f"\nOcorreu um erro crítico durante a inicialização: {e}")