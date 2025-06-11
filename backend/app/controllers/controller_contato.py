import mysql.connector
from fastapi import HTTPException
from app.database.config import get_db_config
from app.models.contato_model import EmpresaContato, EmpresaContatoUpdate

# EMPRESA_CONTATO
def get_empresa_contatos():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contato")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def update_empresa_contato(id: int, data: EmpresaContatoUpdate):
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contato SET telefone_comercial = %s, celular = %s, whatsapp = %s WHERE id = %s
    """, (data.telefone_comercial, data.celular, data.whatsapp, id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Contato atualizado com sucesso"}
