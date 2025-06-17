import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.model_ramo import RamoBase
from app.models.empresa_ramo_model import EmpresaRamoCreate, EmpresaRamoResponse
from app.repository.empresaRamo_rapository import associar_ramos, remover_associacao, listar_ramo_por_empresa


def controller_associar_ramos(id_empresa:int, dados: EmpresaRamoCreate) -> dict:
    try:
        associacoes_criadas = associar_ramos(id_empresa, dados)
        return {
            "message": "Associações realizadas com sucesso.",
            "associacoes_criadas": associacoes_criadas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao associar ramos: {e}")

def controller_remover_associacao(id_empresa: int, id_ramo: int) -> dict:
    try:
        remover_associacao(id_empresa, id_ramo)
        return {"detail": "Associação removida com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}")

def controller_listar_ramos_por_empresas(id_empresa:int) -> List[RamoBase]:
    try:
       return listar_ramo_por_empresa(id_empresa)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}")