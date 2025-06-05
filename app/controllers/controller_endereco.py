import mysql.connector
from fastapi import HTTPException
from app.database.config import get_db_config
from app.models.model_endereco import EmpresaEndereco, EmpresaEnderecoUpdate

def get_empresa_enderecos_by_empresa_id(empresa_id: int):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM endereco WHERE id_empresa = %s", (empresa_id,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum endereço encontrado para esta empresa")
        return rows
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar endereços: {err}")

def update_empresa_endereco(empresa_id: int, endereco_id: int, data: dict):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Verifica se o endereço pertence à empresa
        cursor.execute("SELECT id FROM endereco WHERE id = %s AND id_empresa = %s", (endereco_id, empresa_id))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Endereço não encontrado para esta empresa")

        # Atualiza o endereço
        cursor.execute("""
            UPDATE endereco SET 
                logradouro = %s,
                bairro = %s,
                cep = %s,
                cidade = %s,
                uf = %s,
                complemento = %s
            WHERE id = %s AND id_empresa = %s
        """, (
            data.get('logradouro'),
            data.get('bairro'),
            data.get('cep'),
            data.get('cidade'),
            data.get('uf'),
            data.get('complemento'),
            endereco_id,
            empresa_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"mensagem": "Endereço atualizado com sucesso"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar endereço: {err}")
    