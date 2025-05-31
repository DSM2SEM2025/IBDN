import mysql.connector
from fastapi import HTTPException
from app.database.config import get_db_config
from typing import List
from app.models.model_ramo import RamoBase
from app.models.empresa_ramo_model import EmpresaRamoCreate, EmpresaRamoResponse

# Empresa_ramo

def associar_ramos(id_empresa:int, dados: EmpresaRamoCreate) -> List[EmpresaRamoResponse]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        associacoes = []

        for id_ramo in dados.ids_ramo:
            cursor.execute(
                "SELECT * FROM empresa_ramo WHERE id_empresa = %s AND id_ramo = %s", (id_empresa, id_ramo)
            )
            if cursor.fetchone():
                continue
        
            cursor.execute(
                "INSERT INTO empresa_ramo (id_empresa, id_ramo) VALUES (%s,%s)",(id_empresa, id_ramo)
            )
            conn.commit()

            associacoes.append(
                EmpresaRamoResponse(
                    id=cursor.lastrowid,
                    id_empresa=id_empresa,
                    id_ramo=id_ramo
                )
            )
        cursor.close()
        conn.close()

        if not associacoes:
            raise HTTPException(status_code=400, detail="Nenhuma associação foi criada. Todas já existiam")
        
        return associacoes
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Falha ao assossiar ramo: {err}")
    
def remover_associacao(id_empresa: int, id_ramo:int) -> None:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM empresa_ramo WHERE id_empresa = %s AND id_ramo = %s", (id_empresa, id_ramo)
        )
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Associação não encontrada")
        cursor.execute(
            "DELETE FROM empresa_ramo WHERE id_empresa = %s AND id_ramo = %s", (id_empresa,id_ramo)
        )

        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao remover associação: {err}")
    
def listar_ramos_por_empresas(id_empresa:int) -> List[RamoBase]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """SELECT r.id, r.nome, r.descricao FROM ramo r INNER JOIN empresa_ramo er ON r.id = er.id_ramo WHERE er.id_empresa = %s""", (id_empresa,)
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        
        ramos = [RamoBase(**row) for row in rows]

        return ramos
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao listar ramos pelas empresas: {err}")
    