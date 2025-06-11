import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
from app.database.connection import get_db_connection
from typing import Optional


def login_usuario(email: str):
    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        print(f"Login attempt for email: {email}")

        query = "SELECT * FROM ibdn_usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()

        cursor.close()
        connection.close()

        if usuario:
            return usuario
        else:
            return None
    except Error as err:
        raise HTTPException(
            status_code=500, detail=f"Erro ao acessar banco: {err}")
