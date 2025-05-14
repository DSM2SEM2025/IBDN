from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.empresa_ramo_model import EmpresaRamo
from database import get_db

router = APIRouter(prefix="/empresa_ramo", tags=["EmpresaRamo"])

@router.post("/")
def atribuir_ramo(id_empresa: int, id_ramo: int, db: Session = Depends(get_db)):
    existente = db.query(EmpresaRamo).filter_by(id_empresa=id_empresa, id_ramo=id_ramo).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ramo já atribuído à empresa")
    relacao = EmpresaRamo(id_empresa=id_empresa, id_ramo=id_ramo)
    db.add(relacao)
    db.commit()
    return {"mensagem": "Ramo atribuído com sucesso"}