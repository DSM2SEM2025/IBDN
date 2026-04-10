"""
Seed Base Module
Fornece funções helper para os scripts de seed do banco de dados IBDN.
"""
import logging
import os
import random
from datetime import datetime, timedelta

import mysql.connector
from faker import Faker
from dotenv import load_dotenv

load_dotenv()

# Initialize Faker with pt_BR locale
fake = Faker('pt_BR')


def setup_logging(name: str = 'seed') -> logging.Logger:
    """
    Configura logging para scripts de seed.
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'logs'
    )
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'seed.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(name)


def get_db_config() -> dict:
    """
    Obtém configuração do banco de dados a partir de variáveis de ambiente.
    
    Returns:
        Dicionário com configurações do banco
    """
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))
    }


def get_db_connection() -> mysql.connector.MySQLConnection:
    """
    Cria conexão com o banco de dados.
    
    Returns:
        Objeto de conexão MySQL
        
    Raises:
        mysql.connector.Error: Se falhar ao conectar
    """
    config = get_db_config()
    return mysql.connector.connect(**config)


class SeedContextManager:
    """
    Context manager para operações de seed com rollback automático.
    """
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or setup_logging()
        self.connection = None
        self.cursor = None
        
    def __enter__(self):
        try:
            self.connection = get_db_connection()
            self.cursor = self.connection.cursor(dictionary=True)
            self.logger.info("Conexão com banco de dados estabelecida")
            return self
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao conectar ao banco: {e}")
            raise
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"Erro durante execução: {exc_val}")
            if self.connection:
                self.connection.rollback()
                self.logger.info("Rollback executado")
        
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Conexão encerrada")
            
    def commit(self):
        if self.connection:
            self.connection.commit()
            
    def rollback(self):
        if self.connection:
            self.connection.rollback()


def gerar_cnpj() -> str:
    """
    Gera um CNPJ válido com dígitos verificadores corretos.
    
    Returns:
        CNPJ formatado (XX.XXX.XXX/XXXX-XX)
    """
    # Gera os 8 primeiros dígitos (raiz)
    raiz = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    
    # Gera os 4 dígitos do estabelecimento
    estabelecimento = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
    # Concatena para cálculo dos dígitos verificadores
    cnpj_base = raiz + estabelecimento
    
    # Cálculo do primeiro dígito verificador
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_1 = sum(int(c) * p for c, p in zip(cnpj_base[:12], pesos_1))
    resto_1 = soma_1 % 11
    dv1 = 0 if resto_1 < 2 else 11 - resto_1
    
    # Cálculo do segundo dígito verificador
    cnpj_com_dv1 = cnpj_base + str(dv1)
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2 = sum(int(c) * p for c, p in zip(cnpj_com_dv1, pesos_2))
    resto_2 = soma_2 % 11
    dv2 = 0 if resto_2 < 2 else 11 - resto_2
    
    cnpj_final = f"{raiz[:2]}.{raiz[2:5]}.{raiz[5:8]}/{estabelecimento}-{dv1}{dv2}"
    
    return cnpj_final


def get_faker() -> Faker:
    """
    Retorna instância do Faker com locale pt_BR.
    
    Returns:
        Instância de Faker
    """
    return fake


def record_exists(table: str, column: str, value: any, cursor) -> bool:
    """
    Verifica se um registro existe na tabela.
    
    Args:
        table: Nome da tabela
        column: Nome da coluna para verificação
        value: Valor a verificar
        cursor: Cursor do banco de dados
        
    Returns:
        True se existe, False caso contrário
    """
    cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = %s LIMIT 1", (value,))
    return cursor.fetchone() is not None


def get_or_create_id(table: str, column: str, value: any, id_column: str = 'id', 
                     create_if_not_exists: bool = True, cursor = None) -> str:
    """
    Obtém ID de um registro existente ou cria novo se não existir.
    
    Args:
        table: Nome da tabela
        column: Coluna para busca
        value: Valor para busca
        id_column: Nome da coluna ID
        create_if_not_exists: Se True, cria registro se não existir
        cursor: Cursor do banco
        
    Returns:
        ID do registro (existente ou novo)
    """
    import uuid
    
    cursor.execute(f"SELECT {id_column} FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()
    
    if result:
        return result[id_column]
    
    if create_if_not_exists:
        new_id = str(uuid.uuid4())
        cursor.execute(f"INSERT INTO {table} ({id_column}, {column}) VALUES (%s, %s)", 
                      (new_id, value))
        return new_id
    
    return None


def execute_seed_safe(table_name: str, seed_func, logger: logging.Logger = None) -> bool:
    """
    Executa função de seed de forma segura com tratamento de erros.
    
    Args:
        table_name: Nome da tabela sendo populada
        seed_func: Função de seed a executar
        logger: Logger para mensagens
        
    Returns:
        True se sucesso, False se erro
    """
    logger = logger or setup_logging()
    
    try:
        logger.info(f"Iniciando seed para {table_name}...")
        result = seed_func()
        logger.info(f"Seed para {table_name} concluído com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro durante seed de {table_name}: {e}")
        return False