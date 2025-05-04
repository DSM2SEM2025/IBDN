import os
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', '3306'))
    }
    if not all([config['user'], config['password'], config['database']]):
        raise ValueError(
            "Variáveis de ambiente do banco de dados não configuradas corretamente")
    return config
