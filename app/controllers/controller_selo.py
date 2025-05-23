import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from ..repository.selos_repository import select_selo_empresa, delete_selos_expirados, update_renovar_selo, update_solicitar_renovacao, update_expirar_selo_automatico, get_selos_por_empresas as repo_get_selos, select_selo_empresa, update_rejeitar_renovacao


async def get_selos_por_empresas(
    empresa_id: int,
    pagina: int = 1,
    limite: int = 10,
    status: Optional[str] = None,
    expiracao_proxima: Optional[bool] = None
):  
    try:
        resultado = await repo_get_selos(
            empresa_id=empresa_id,
            pagina=pagina,
            limite=limite,
            status=status,
            expiracao_proxima=expiracao_proxima
        )
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=500,
        )
def retornar_empresas_com_selos_criados():
    try:
        selos = select_selo_empresa()
        return selos 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
def remover_selos_expirados():
    """
    Controller para remover selos que estão expirados há mais de 30 dias.
    """
    try:
        selos_removidos = delete_selos_expirados()
        return {
            "status": "success",
            "mensagem": f"Remoção de selos expirados processada com sucesso",
            "dados": selos_removidos
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao remover selos expirados: {str(e)}"
        )


def controller_renovar_selo(selo_id: int):
    """
    Controller para renovar um selo (alterar status de pendente para ativo).
    Esta função é utilizada pelo administrador para aprovar renovações.
    """
    try:
        selo = select_selo_empresa(selo_id=selo_id)
        if not selo:
            raise HTTPException(
                status_code=404, 
                detail=f"Selo com ID {selo_id} não encontrado"
            )
            
        resultado = update_renovar_selo(selo_id)
        return {
            "status": "success",
            "mensagem": f"Selo com ID {selo_id} renovado com sucesso",
            "dados": resultado
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao renovar selo: {str(e)}"
        )


def controller_solicitar_renovacao(selo_id: int):
    """
    Controller para solicitar renovação de um selo (alterar status de expirado para pendente).
    """
    try:
        selo = select_selo_empresa(selo_id=selo_id)
        if not selo:
            raise HTTPException(
                status_code=404, 
                detail=f"Selo com ID {selo_id} não encontrado"
            )
            
        if selo.get("status", "").lower() != "expirado":  # Corrigido aqui
            raise HTTPException(
                status_code=400, 
                detail=f"Apenas selos com status 'expirado' podem solicitar renovação"
            )
            
        resultado = update_solicitar_renovacao(selo_id)
        return {
            "status": "success",
            "mensagem": f"Solicitação de renovação para o selo ID {selo_id} enviada com sucesso",
            "dados": resultado
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao solicitar renovação do selo: {str(e)}"
        )


def controller_expirar_selo_automatico():
    """
    Controller para expirar selos automaticamente.
    Esta função é executada periodicamente para alterar o status de selos ativos
    que atingiram sua data de expiração.
    """
    try:
        selos_expirados = update_expirar_selo_automatico()
        
        return {
            "status": "success",
            "mensagem": "Verificação de selos expirados concluída",
            "dados": {
                "selos_expirados": selos_expirados,
                "data_execucao": datetime.now().isoformat()
            }
        }
    except Exception as e:
        print(f"Erro ao expirar selos automaticamente: {str(e)}")
        return {
            "status": "error",
            "mensagem": f"Erro ao processar expiração automática de selos",
            "erro": str(e)
        }


def controller_rejeitar_renovacao_selo(selo_id: int, motivo: str = ""):
    """
    Controller para rejeitar a renovação de um selo (alterar status de pendente para expirado).
    Esta função é utilizada pelo administrador quando não aprova a renovação solicitada.
    """
    try:
        selo = select_selo_empresa(selo_id=selo_id)
        if not selo:
            raise HTTPException(
                status_code=404, 
                detail=f"Selo com ID {selo_id} não encontrado"
            )
        if selo.get("status") != "pendente":
            raise HTTPException(
                status_code=400, 
                detail=f"Apenas selos com status 'pendente' podem ter a renovação rejeitada"
            )
        resultado = update_rejeitar_renovacao(selo_id, motivo)
        
        return {
            "status": "success",
            "mensagem": f"Renovação do selo ID {selo_id} rejeitada com sucesso",
            "dados": resultado
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao rejeitar renovação do selo: {str(e)}"
        )