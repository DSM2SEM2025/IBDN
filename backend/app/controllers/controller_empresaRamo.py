import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.model_ramo import RamoBase
from app.models.empresa_ramo_model import EmpresaRamoCreate, EmpresaRamoResponse
from app.repository.empresaRamo_rapository import associar_ramos, remover_associacao, listar_ramo_por_empresa

# Empresa_ramo

def controller_associar_ramos(id_empresa:int, dados: EmpresaRamoCreate) -> List[EmpresaRamoResponse]:
    try:
        associacoes = associar_ramos(id_empresa, dados)
        return associacoes
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}") 
    
def controller_remover_associacao(id_empresa: int, id_ramo:int) -> None:
    try:
        return remover_associacao(id_empresa,id_ramo)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}") 
    
def controller_listar_ramos_por_empresas(id_empresa:int) -> List[RamoBase]:
    try:
       return listar_ramo_por_empresa(id_empresa)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}") 
    