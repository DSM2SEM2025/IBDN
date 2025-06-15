import datetime
import json
import logging
import os
import socket

import mysql.connector
from mysql.connector import Error
# Supondo que esta função retorne o dict de config
from app.database.config import get_db_config


def setup_logging():
    """Configura o logging para as operações do banco de dados."""
    log_dir = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'database.log')
    # Remove handlers antigos para evitar duplicação de logs se a função for chamada múltiplas vezes
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
    logger.info("Iniciando a inicialização do banco de dados")
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
            FOREIGN KEY (usuario_id) REFERENCES ibdn_usuarios(id)
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
            bairro VARCHAR(100) NOT NULL,
            cep VARCHAR(10) NOT NULL,
            cidade VARCHAR(100) NOT NULL,
            uf VARCHAR(2) NOT NULL,
            complemento VARCHAR(255),
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        tables['tipo_selo'] = """
        CREATE TABLE IF NOT EXISTS tipo_selo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT NOT NULL,
            sigla VARCHAR(10) NOT NULL UNIQUE
        ) ENGINE=InnoDB;
        """

        tables['selo'] = """
        CREATE TABLE IF NOT EXISTS selo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_tipo_selo INT NOT NULL,
            data_emissao DATE NOT NULL,
            data_expiracao DATE NOT NULL,
            codigo_selo VARCHAR(50) NOT NULL UNIQUE,
            status VARCHAR(20) NOT NULL,
            documentacao TEXT,
            alerta_enviado BOOLEAN DEFAULT FALSE,
            dias_alerta_previo INT DEFAULT 30,
            FOREIGN KEY (id_tipo_selo) REFERENCES tipo_selo(id)
        ) ENGINE=InnoDB;
        """

        tables['empresa_selo'] = """
        CREATE TABLE IF NOT EXISTS empresa_selo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_empresa INT NOT NULL,
            id_selo INT NOT NULL,
            UNIQUE (id_empresa, id_selo),
            FOREIGN KEY (id_empresa) REFERENCES empresa(id) ON DELETE CASCADE,
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

        table_creation_order = [
            'ibdn_permissoes', 'ibdn_perfis', 'ramo', 'tipo_rede_social', 'tipo_selo',  # Nível 0
            'ibdn_usuarios', 'selo', 'ibdn_perfil_permissoes',  # Nível 1
            'empresa',  # Nível 2
            'endereco', 'empresa_selo', 'notificacao',  # Nível 3
            'alerta_expiracao_selo',  # Nível 4
            'log_acesso', 'log_auditoria', 'log_erro'  # Nível 5 (Logs)
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

def create_admin_master_user():
    """Cria o usuário administrador mestre padrão se não existir"""
    logger = setup_logging()
    logger.info("Verificando/Configurando usuário admin_master...")
    
    try:
        from app.repository.ibdn_permissions_repository import repo_create_ibdn_permissao
        from app.repository.ibdn_profiles_repository import (
            repo_create_ibdn_perfil,
            repo_get_ibdn_perfil_by_id_with_permissions,
            repo_add_permissao_to_perfil
        )
        from app.repository.ibdn_user_repository import (
            repo_get_ibdn_usuario_by_email,
            repo_create_ibdn_usuario
        )
        from app.security.password import get_password_hash
        from app.models.ibdn_user_model import IbdnUsuarioCreate  
        import os
        from uuid import uuid4

        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if not admin_email or not admin_password:
            error_msg = "Variáveis ADMIN_EMAIL e ADMIN_PASSWORD não configuradas. É obrigatório configurar estas variáveis."
            logger.error(error_msg)
            if os.getenv('ENVIRONMENT') == 'production':
                raise ValueError(error_msg)
            return

        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        
        try:
            # 1. Verificar/Criar permissão admin_master
            cursor.execute("SELECT id FROM ibdn_permissoes WHERE nome = 'admin_master'")
            permissao = cursor.fetchone()
            
            if not permissao:
                logger.info("Criando permissão admin_master...")
                permissao_id = str(uuid4())
                repo_create_ibdn_permissao({
                    'id': permissao_id,
                    'nome': 'admin_master'
                })
                logger.info(f"Permissão admin_master criada com ID: {permissao_id}")
            else:
                permissao_id = permissao['id']
                logger.info(f"Permissão admin_master já existe com ID: {permissao_id}")
            
            # 2. Verificar/Criar perfil admin_master
            cursor.execute("SELECT id FROM ibdn_perfis WHERE nome = 'admin_master'")
            perfil = cursor.fetchone()
            
            if not perfil:
                logger.info("Criando perfil admin_master...")
                perfil_id = str(uuid4())
                repo_create_ibdn_perfil({
                    'id': perfil_id,
                    'nome': 'admin_master'
                }, [permissao_id])
                logger.info(f"Perfil admin_master criado com ID: {perfil_id}")
            else:
                perfil_id = perfil['id']
                logger.info(f"Perfil admin_master já existe com ID: {perfil_id}")
                # Verificar se a permissão está associada ao perfil
                cursor.execute(
                    "SELECT 1 FROM ibdn_perfil_permissoes WHERE perfil_id = %s AND permissao_id = %s",
                    (perfil_id, permissao_id)
                )
                if not cursor.fetchone():
                    logger.info("Associando permissão admin_master ao perfil...")
                    repo_add_permissao_to_perfil(perfil_id, permissao_id)
                    logger.info("Permissão associada com sucesso.")
            
            # 3. Verificar/Criar usuário admin
            usuario = repo_get_ibdn_usuario_by_email(admin_email)
            if not usuario:
                logger.info(f"Criando usuário admin_master com email {admin_email}...")
                usuario_id = str(uuid4())
                
                usuario_data = IbdnUsuarioCreate(
                    id=usuario_id,
                    nome='Admin Master',
                    email=admin_email,
                    senha=admin_password,
                    perfil_id=perfil_id,
                    ativo=True,
                    twofactor=False
                )
                
                repo_create_ibdn_usuario(usuario_data)
                logger.info(f"Usuário admin_master criado com sucesso! ID: {usuario_id}")
            else:
                logger.info(f"Usuário admin_master já existe com email {admin_email}. Verificando configuração...")
                if usuario.get('perfil_id') != perfil_id:
                    logger.warning(f"Usuário admin existe mas não tem o perfil correto. Atualizando...")

                
        except Exception as e:
            logger.error(f"Erro durante a criação do admin_master: {str(e)}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
                
    except Exception as e:
        logger.error(f"Erro ao configurar admin_master: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        create_database_if_not_exists()
        create_tables()
        print("\nScript de inicialização do banco de dados concluído com sucesso.")
    except Exception as e:
        print(f"\nOcorreu um erro crítico durante a inicialização: {e}")