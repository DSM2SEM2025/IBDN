import os
from dotenv import load_dotenv
from contextlib import contextmanager
from fastapi import HTTPException
from mysql.connector import Error
import mysql.connector 

load_dotenv()

def get_db_config():
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT'))
    }
    if not all([config['user'], config['password'], config['database']]):
        raise ValueError(
            "Variáveis de ambiente do banco de dados não configuradas corretamente")
    return config

def get_db_connection():
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        return connection 
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao conectar ao banco de dados: {str(e)}"
        )
    
@contextmanager
def get_cursor():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()