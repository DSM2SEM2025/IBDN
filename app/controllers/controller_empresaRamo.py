import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.model_ramo import RamoBase
from app.models.empresa_ramo_model import EmpresaRamoCreate, EmpresaRamoResponse
from app.repository.empresaRamo_rapository import associar_ramos, remover_associacao, listar_ramo_por_empresa

# Empresa_ramo

def controller_associar_ramos(id_empresa:int, dados: EmpresaRamoCreate) -> dict: # Tipo de retorno alterado para dict
    try:
        associacoes_criadas = associar_ramos(id_empresa, dados)
        # Monta um objeto de resposta mais descritivo
        return {
            "message": "Associações realizadas com sucesso.",
            "associacoes_criadas": associacoes_criadas
        }
    except Exception as e:
        # Recomenda-se usar um status code mais apropriado para erros, como 500 para erro de banco
        raise HTTPException(status_code=500, detail=f"Erro ao associar ramos: {e}")
    
def controller_remover_associacao(id_empresa: int, id_ramo: int) -> dict: # Alterado o tipo de retorno para dict
    try:
        remover_associacao(id_empresa, id_ramo)
        return {"detail": "Associação removida com sucesso."} # Adicionado o retorno
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}")
    
def controller_listar_ramos_por_empresas(id_empresa:int) -> List[RamoBase]:
    try:
       return listar_ramo_por_empresa(id_empresa)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}") 
    