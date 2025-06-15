import logging
import os
import mysql.connector
from mysql.connector import Error
from app.database.config import get_db_config
from app.security.password import get_password_hash
from uuid import uuid4


def setup_logging():
    """Configura o logging para as operações do banco de dados."""
    log_dir = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'database.log')
    # Limpa handlers existentes para evitar duplicação de logs
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
    """Conecta ao banco de dados e cria todas as tabelas na ordem correta."""
    logger = setup_logging()
    logger.info("Iniciando a criação das tabelas do banco de dados")
    connection = None
    cursor = None
    try:
        config = get_db_config()
        logger.info("Conectando ao banco de dados...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")

        tables = {}

        # --- DEFINIÇÃO DE TABELAS ---
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
            site_empresa VARCHAR(255),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (usuario_id) REFERENCES ibdn_usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
        tables['ramo'] = "CREATE TABLE IF NOT EXISTS ramo (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100) NOT NULL UNIQUE, descricao TEXT) ENGINE=InnoDB;"
        
        # --- NOVA TABELA DE ASSOCIAÇÃO ---
        tables['empresa_ramo'] = """
        CREATE TABLE IF NOT EXISTS empresa_ramo (
            id_empresa INT NOT NULL,
            id_ramo INT NOT NULL,
            PRIMARY KEY (id_empresa, id_ramo),
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
            FOREIGN KEY (id_ramo) REFERENCES ramo(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
        
        tables['tipo_rede_social'] = "CREATE TABLE IF NOT EXISTS tipo_rede_social (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(50) NOT NULL UNIQUE) ENGINE=InnoDB;"
        tables['endereco'] = "CREATE TABLE IF NOT EXISTS endereco (id INT AUTO_INCREMENT PRIMARY KEY, id_empresa INT NOT NULL, logradouro VARCHAR(255) NOT NULL, bairro VARCHAR(100) NOT NULL, cep VARCHAR(10) NOT NULL, cidade VARCHAR(100) NOT NULL, uf VARCHAR(2) NOT NULL, complemento VARCHAR(255), FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE) ENGINE=InnoDB;"
        tables['tipo_selo'] = "CREATE TABLE IF NOT EXISTS tipo_selo (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(100) NOT NULL, descricao TEXT NOT NULL, sigla VARCHAR(10) NOT NULL UNIQUE) ENGINE=InnoDB;"
        tables['selo'] = "CREATE TABLE IF NOT EXISTS selo (id INT AUTO_INCREMENT PRIMARY KEY, id_tipo_selo INT NOT NULL, data_emissao DATE NOT NULL, data_expiracao DATE NOT NULL, codigo_selo VARCHAR(50) NOT NULL UNIQUE, status VARCHAR(20) NOT NULL, documentacao TEXT, alerta_enviado BOOLEAN DEFAULT FALSE, dias_alerta_previo INT DEFAULT 30, FOREIGN KEY (id_tipo_selo) REFERENCES tipo_selo(id)) ENGINE=InnoDB;"
        tables['empresa_selo'] = "CREATE TABLE IF NOT EXISTS empresa_selo (id INT AUTO_INCREMENT PRIMARY KEY, id_empresa INT NOT NULL, id_selo INT NOT NULL, UNIQUE (id_empresa, id_selo), FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE, FOREIGN KEY (id_selo) REFERENCES selo(id) ON DELETE CASCADE) ENGINE=InnoDB;"
        tables['alerta_expiracao_selo'] = "CREATE TABLE IF NOT EXISTS alerta_expiracao_selo (id INT AUTO_INCREMENT PRIMARY KEY, id_selo INT NOT NULL, data_envio DATE NOT NULL, email_destino VARCHAR(255) NOT NULL, email_enviado BOOLEAN DEFAULT FALSE, conteudo_email TEXT, status VARCHAR(20) NOT NULL, FOREIGN KEY (id_selo) REFERENCES selo(id) ON DELETE CASCADE) ENGINE=InnoDB;"
        tables['notificacao'] = "CREATE TABLE IF NOT EXISTS notificacao (id INT AUTO_INCREMENT PRIMARY KEY, id_empresa INT NOT NULL, mensagem TEXT NOT NULL, data_envio DATETIME NOT NULL, tipo VARCHAR(50) NOT NULL, lida BOOLEAN DEFAULT FALSE, FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE) ENGINE=InnoDB;"
        tables['log_acesso'] = "CREATE TABLE IF NOT EXISTS log_acesso (id INT AUTO_INCREMENT PRIMARY KEY, id_usuario CHAR(40), data_hora DATETIME NOT NULL, operacao VARCHAR(50) NOT NULL, tabela_afetada VARCHAR(50), id_registro_afetado VARCHAR(255), dados_anteriores JSON, dados_novos JSON, ip VARCHAR(45), user_agent VARCHAR(255), status VARCHAR(20) NOT NULL, mensagem TEXT, tempo_execucao INT, FOREIGN KEY (id_usuario) REFERENCES ibdn_usuarios(id) ON DELETE SET NULL) ENGINE=InnoDB;"
        tables['log_auditoria'] = "CREATE TABLE IF NOT EXISTS log_auditoria (id INT AUTO_INCREMENT PRIMARY KEY, id_usuario CHAR(40), data_hora DATETIME NOT NULL, tipo_evento ENUM('LOGIN', 'LOGOUT', 'TENTATIVA_LOGIN', 'ALTERACAO_PERMISSAO', 'EXCLUSAO', 'APROVACAO') NOT NULL, descricao TEXT NOT NULL, ip VARCHAR(45) NOT NULL, user_agent VARCHAR(255), status VARCHAR(20) NOT NULL, FOREIGN KEY (id_usuario) REFERENCES ibdn_usuarios(id) ON DELETE SET NULL) ENGINE=InnoDB;"
        tables['log_erro'] = "CREATE TABLE IF NOT EXISTS log_erro (id INT AUTO_INCREMENT PRIMARY KEY, data_hora DATETIME NOT NULL, nivel ENUM('INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL, origem VARCHAR(255) NOT NULL, mensagem TEXT NOT NULL, stack_trace TEXT, id_usuario CHAR(40), ip VARCHAR(45), FOREIGN KEY (id_usuario) REFERENCES ibdn_usuarios(id) ON DELETE SET NULL) ENGINE=InnoDB;"

        # --- ORDEM DE CRIAÇÃO DAS TABELAS (ATUALIZADA) ---
        table_creation_order = [
            'ibdn_permissoes', 'ibdn_perfis', 'ramo', 'tipo_rede_social', 'tipo_selo',
            'ibdn_usuarios', 'selo', 'ibdn_perfil_permissoes',
            'empresa',
            'endereco', 'empresa_selo', 'empresa_ramo', 'notificacao',
            'alerta_expiracao_selo',
            'log_acesso', 'log_auditoria', 'log_erro'
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
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("Conexão com MySQL foi fechada.")


def create_database_if_not_exists():
    """Cria o banco de dados se ele ainda não existir."""
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
    """Cria os dados iniciais essenciais para o sistema, como perfis e o admin master."""
    logger = setup_logging()
    logger.info("Verificando/Configurando dados iniciais...")

    connection = None
    cursor = None
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)

        # 1. Criar Perfis Padrão (Admin, Empresa, Admin Master)
        perfis_a_criar = {
            "admin": str(uuid4()),
            "empresa": str(uuid4()),
            "admin_master": str(uuid4())
        }
        for nome_perfil, perfil_id in perfis_a_criar.items():
            cursor.execute(
                "SELECT id FROM ibdn_perfis WHERE nome = %s", (nome_perfil,))
            if not cursor.fetchone():
                logger.info(f"Criando perfil '{nome_perfil}'...")
                cursor.execute(
                    "INSERT INTO ibdn_perfis (id, nome) VALUES (%s, %s)", (perfil_id, nome_perfil))

        connection.commit()  # Commit após criar perfis

        # 2. Criar Permissões Essenciais
        permissoes_a_criar = {
            "admin": str(uuid4()),
            "admin_master": str(uuid4()),
            "empresa": str(uuid4())
        }
        for nome_permissao, permissao_id in permissoes_a_criar.items():
            cursor.execute(
                "SELECT id FROM ibdn_permissoes WHERE nome = %s", (nome_permissao,))
            if not cursor.fetchone():
                logger.info(f"Criando permissão '{nome_permissao}'...")
                cursor.execute(
                    "INSERT INTO ibdn_permissoes (id, nome) VALUES (%s, %s)", (permissao_id, nome_permissao))

        connection.commit()  # Commit após criar permissões

        # 3. Associar Permissão 'admin_master' ao Perfil 'admin_master'
        cursor.execute(
            "SELECT id FROM ibdn_perfis WHERE nome = 'admin_master'")
        perfil_master_result = cursor.fetchone()
        
        cursor.execute(
            "SELECT id FROM ibdn_permissoes WHERE nome = 'admin_master'")
        permissao_master_result = cursor.fetchone()

        if perfil_master_result and permissao_master_result:
            perfil_master_id = perfil_master_result['id']
            permissao_master_id = permissao_master_result['id']

            cursor.execute("SELECT 1 FROM ibdn_perfil_permissoes WHERE perfil_id = %s AND permissao_id = %s",
                           (perfil_master_id, permissao_master_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)",
                               (perfil_master_id, permissao_master_id))
                logger.info(
                    "Permissão 'admin_master' associada ao perfil 'admin_master'.")
                connection.commit()

        # 4. Criar Usuário Admin Master
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com') # Adicionado valor padrão
        admin_password = os.getenv('ADMIN_PASSWORD', 'strongpassword123') # Adicionado valor padrão

        if not admin_email or not admin_password:
            logger.warning(
                "Variáveis ADMIN_EMAIL e ADMIN_PASSWORD não configuradas. Admin master não será criado.")
            return

        cursor.execute(
            "SELECT id FROM ibdn_usuarios WHERE email = %s", (admin_email,))
        if not cursor.fetchone():
            cursor.execute(
                "SELECT id FROM ibdn_perfis WHERE nome = 'admin_master'"
            )
            perfil_master_result = cursor.fetchone()
            if perfil_master_result:
                perfil_master_id = perfil_master_result['id']
                logger.info(
                    f"Criando usuário admin_master com email {admin_email}...")
                usuario_id = str(uuid4())
                senha_hash = get_password_hash(admin_password)

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
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    try:
        # Funções para simular dependências (remover em ambiente real)
        def get_db_config():
            return {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'ibdn_db_test'
            }
        
        def get_password_hash(password):
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest()

        # Sobrescrevendo as funções importadas para o teste
        globals()['get_db_config'] = get_db_config
        globals()['get_password_hash'] = get_password_hash

        create_database_if_not_exists()
        create_tables()
        create_initial_data()
        print("\nScript de inicialização do banco de dados concluído com sucesso.")
    except Exception as e:
        print(f"\nOcorreu um erro crítico durante a inicialização: {e}")