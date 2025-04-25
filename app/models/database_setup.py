from app.database.config import get_db_config
import mysql.connector
from mysql.connector import Error
import logging
import datetime
import json
import os
import socket


def setup_logging():
    """Configure logging for the database operations"""
    log_dir = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'logs')

    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Setup logging with rotation
    log_file = os.path.join(log_dir, 'database.log')
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
    logger.info("Starting database initialization")

    try:

        config = get_db_config()

        logger.info("Connecting to database")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        log_database_operation(
            connection=connection,
            operation_type="CONNECT",
            details="Database connection established",
            status="SUCCESS"
        )

        tables = {}

        tables['empresa'] = """
        CREATE TABLE IF NOT EXISTS empresa (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cnpj VARCHAR(18) NOT NULL,
        razao_social VARCHAR(255) NOT NULL,
        nome_fantasia VARCHAR(255),
        email VARCHAR(255) NOT NULL UNIQUE,  
        senha_hash VARCHAR(255) NOT NULL,   
        telefone VARCHAR(20),
        responsavel VARCHAR(100),
        cargo_responsavel VARCHAR(100),
        site_empresa VARCHAR(255),
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        ativo BOOLEAN DEFAULT TRUE,       
        UNIQUE (cnpj),                 
        INDEX (email)                      
        ) ENGINE=InnoDB;
        """

        tables['administrador'] = """
        CREATE TABLE IF NOT EXISTS administrador (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            senha_hash VARCHAR(255) NOT NULL,
            perfil VARCHAR(50) NOT NULL,
            tipo_admin VARCHAR(50) NOT NULL,
            UNIQUE (email)
        ) ENGINE=InnoDB;
        """

        tables['empresa_ramo'] = """
        CREATE TABLE IF NOT EXISTS empresa_ramo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            id_ramo INT NOT NULL,
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
            FOREIGN KEY (id_ramo) REFERENCES ramo(id) ON DELETE CASCADE,
            UNIQUE (id_empresa, id_ramo)
        ) ENGINE=InnoDB;
        """

        tables['ramo'] = """
        CREATE TABLE IF NOT EXISTS ramo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            id_tipo_rede_social INT,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT,
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
            FOREIGN KEY (id_tipo_rede_social) REFERENCES tipo_rede_social(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

        tables['tipo_rede_social'] = """
        CREATE TABLE IF NOT EXISTS tipo_rede_social (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            descricao VARCHAR(255),
            UNIQUE (nome)
        ) ENGINE=InnoDB;
        """

        tables['rede_social'] = """
        CREATE TABLE IF NOT EXISTS rede_social (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            id_tipo_rede_social INT NOT NULL,
            url VARCHAR(255) NOT NULL,
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
            FOREIGN KEY (id_tipo_rede_social) REFERENCES tipo_rede_social(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        tables['endereco'] = """
        CREATE TABLE IF NOT EXISTS endereco (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            logradouro VARCHAR(255) NOT NULL,
            bairro VARCHAR(100) NOT NULL,
            cep VARCHAR(10) NOT NULL,
            cidade VARCHAR(100) NOT NULL,
            uf VARCHAR(2) NOT NULL,
            complemento VARCHAR(255),
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        tables['contato'] = """
        CREATE TABLE IF NOT EXISTS contato (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            telefone_comercial VARCHAR(20),
            celular VARCHAR(20),
            whatsapp VARCHAR(20),
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        tables['selo'] = """
        CREATE TABLE IF NOT EXISTS selo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            data_emissao DATE NOT NULL,
            data_expiracao DATE NOT NULL,
            codigo_selo VARCHAR(50) NOT NULL,
            status VARCHAR(20) NOT NULL,
            documentacao TEXT,
            alerta_enviado BOOLEAN DEFAULT FALSE,
            dias_alerta_previo INT DEFAULT 30,
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
            UNIQUE (codigo_selo)
        ) ENGINE=InnoDB;
        """

        tables['alerta_expiracao_selo'] = """
        CREATE TABLE IF NOT EXISTS alerta_expiracao_selo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_selo INT NOT NULL,
            data_envio DATE NOT NULL,
            email_destino VARCHAR(255) NOT NULL,
            email_enviado BOOLEAN DEFAULT FALSE,
            conteudo_email TEXT,
            status VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_selo) REFERENCES selo(id) ON DELETE CASCADE
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

        tables['solicitacao_aprovacao'] = """
        CREATE TABLE IF NOT EXISTS solicitacao_aprovacao (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            tipo_dado VARCHAR(50) NOT NULL,
            id_registro INT NOT NULL,
            status VARCHAR(20) NOT NULL,
            ip VARCHAR(45),
            acao VARCHAR(20) NOT NULL,
            data_solicitacao DATETIME NOT NULL,
            data_resposta DATETIME,
            comentario_aprovador TEXT,
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        tables['log_acesso'] = """
        CREATE TABLE IF NOT EXISTS log_acesso (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_administrador INT,
            data_hora DATETIME NOT NULL,
            operacao VARCHAR(50) NOT NULL,
            tabela_afetada VARCHAR(50),
            id_registro_afetado INT,
            dados_anteriores JSON,
            dados_novos JSON,
            ip VARCHAR(45),
            user_agent VARCHAR(255),
            status VARCHAR(20) NOT NULL,
            mensagem TEXT,
            tempo_execucao INT,
            FOREIGN KEY (id_administrador) REFERENCES administrador(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

        tables['log_auditoria'] = """
        CREATE TABLE IF NOT EXISTS log_auditoria (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_administrador INT,
            data_hora DATETIME NOT NULL,
            tipo_evento ENUM('LOGIN', 'LOGOUT', 'TENTATIVA_LOGIN', 'ALTERACAO_PERMISSAO', 'EXCLUSAO', 'APROVACAO') NOT NULL,
            descricao TEXT NOT NULL,
            ip VARCHAR(45) NOT NULL,
            user_agent VARCHAR(255),
            status VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_administrador) REFERENCES administrador(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

        tables['log_erro'] = """
        CREATE TABLE IF NOT EXISTS log_erro (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data_hora DATETIME NOT NULL,
            nivel ENUM('INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
            origem VARCHAR(255) NOT NULL,
            mensagem TEXT NOT NULL,
            stack_trace TEXT,
            id_administrador INT,
            ip VARCHAR(45),
            FOREIGN KEY (id_administrador) REFERENCES administrador(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

        table_creation_order = [
            'tipo_rede_social', 'empresa', 'administrador', 'ramo',
            'empresa_ramo', 'rede_social', 'endereco', 'contato',
            'selo', 'alerta_expiracao_selo', 'notificacao',
            'solicitacao_aprovacao', 'log_acesso', 'log_auditoria', 'log_erro'
        ]

        for table_name in table_creation_order:
            logger.info(f"Creating table {table_name}...")
            cursor.execute(tables[table_name])

            log_database_operation(
                connection=connection,
                operation_type="CREATE_TABLE",
                details=f"Table {table_name} created or verified",
                status="SUCCESS",
                table=table_name
            )

        logger.info("All tables created successfully!")
        connection.commit()

    except Error as e:
        logger.error(f"Error creating tables: {e}")

        if connection and connection.is_connected():
            log_database_operation(
                connection=connection,
                operation_type="CREATE_TABLE",
                details=f"Error creating tables: {str(e)}",
                status="ERROR"
            )

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection closed")


def log_database_operation(connection, operation_type, details, status, table=None):

    try:

        if not connection or not connection.is_connected():
            logger = logging.getLogger('database_setup')
            logger.info(f"{operation_type}: {details} - Status: {status}")
            return

        cursor = connection.cursor()

        current_time = datetime.datetime.now()
        ip = socket.gethostbyname(socket.gethostname())

        if operation_type != "CREATE_TABLE" or (table and table != "log_acesso"):
            query = """
            INSERT INTO log_acesso 
            (data_hora, operacao, tabela_afetada, ip, status, mensagem) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (current_time, operation_type, table, ip, status, details)
            )
            connection.commit()

    except Error as e:

        logger = logging.getLogger('database_setup')
        logger.warning(f"Couldn't log to database: {e}")
        logger.info(f"{operation_type}: {details} - Status: {status}")

    finally:
        if cursor:
            cursor.close()


def create_database_if_not_exists():

    logger = setup_logging()
    logger.info("Checking if database exists")

    try:

        config = get_db_config()
        db_name = config.pop('database')

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        logger.info(f"Creating database {db_name} if not exists")
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        logger.info(f"Database {db_name} created or already exists")

        # Close connection
        cursor.close()
        connection.close()

    except Error as e:
        logger.error(f"Error creating database: {e}")
        raise


if __name__ == "__main__":
    setup_logging()
    create_database_if_not_exists()
    create_tables()
