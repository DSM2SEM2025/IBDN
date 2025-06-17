from mysql.connector import Error
from fastapi import HTTPException
from typing import List, Optional, Dict
from app.database.config import get_cursor
from app.models.model_endereco import EmpresaEnderecoCreate, EmpresaEnderecoUpdate

def get_enderecos_by_empresa(empresa_id: int) -> List[Dict]:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM endereco WHERE id_empresa = %s", (empresa_id,))
            return cursor.fetchall()
    except Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar endereços: {err}")

def update_endereco(empresa_id: int, endereco: EmpresaEnderecoUpdate) -> bool:
    try:
        with get_cursor() as cursor:
            update_fields = endereco.model_dump(exclude_unset=True)
            if not update_fields:
                return True

            set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
            
            sql = f"UPDATE endereco SET {set_clause} WHERE id_empresa = %s"
            
            params = list(update_fields.values()) + [empresa_id]

            cursor.execute(sql, tuple(params))
            return cursor.rowcount > 0
    except Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar endereço: {err}")


def create_endereco(empresa_id: int, endereco: EmpresaEnderecoCreate) -> Dict:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT id FROM endereco WHERE id_empresa = %s", (empresa_id,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Esta empresa já possui um endereço cadastrado. Para alterá-lo, use a rota de atualização (PUT).")

            sql = """
            INSERT INTO endereco (id_empresa, logradouro, numero, bairro, cep, cidade, uf, complemento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                empresa_id, endereco.logradouro, endereco.numero, endereco.bairro,
                endereco.cep, endereco.cidade, endereco.uf, endereco.complemento
            ))
            novo_id = cursor.lastrowid
            return {"id": novo_id, **endereco.model_dump()}
    except HTTPException as http_exc:
        raise http_exc
    except Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao criar endereço: {err}")
    
def repo_delete_endereco(empresa_id: int) -> bool:
    try:
        with get_cursor() as cursor:
            sql = "DELETE FROM endereco WHERE id_empresa = %s"
            cursor.execute(sql, (empresa_id,))
            return cursor.rowcount > 0
    except Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar endereço: {err}")