from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from models.empresa_ramo_model import EmpresaRamo
from models.empresas_model import Empresa
from models.ramo_model import Ramo
from models.empresa_ramo_model import EmpresaRamoOut
from database import get_db

router = APIRouter(prefix="/empresa_ramo", tags=["EmpresaRamo"])


# Get ramos (plural) de uma empresa (detalhado)
@router.get("/empresa/{id_empresa}", response_model=list[EmpresaRamoOut])
def get_ramos_por_empresa(id_empresa: int, db: Session = Depends(get_db)):
    relacoes = (
        db.query(EmpresaRamo)
        .join(Empresa, Empresa.id == EmpresaRamo.id_empresa)
        .join(Ramo, Ramo.id == EmpresaRamo.id_ramo)
        .filter(EmpresaRamo.id_empresa == id_empresa)
        .with_entities(
            EmpresaRamo.id_empresa,
            EmpresaRamo.id_ramo,
            Empresa.razao_social.label("empresa_nome"),
            Ramo.nome.label("ramo_nome"),
            Ramo.descricao.label("ramo_descricao")
        )
        .all()
    )
    return relacoes

@router.get("ramo/{id_ramo}", response_model=list[EmpresaRamoOut])
def get_empresa_por_ramo(id_ramo: int, db: Session = Depends(get_db)):
    relacoes = (
        db.query(EmpresaRamo)
        .join(Empresa, Empresa.id == EmpresaRamo.id_empresa)
        .join(Ramo, Ramo.id == EmpresaRamo.id_ramo)
        .filter(EmpresaRamo.id_ramo == id_ramo)
        .with_entities(
            EmpresaRamo.id,
            EmpresaRamo.id_empresa,
            EmpresaRamo.id_ramo,
            Empresa.razao_social.label("empresa_nome"),
            Ramo.nome.label("ramo_nome"),
            Ramo.descricao.label("ramo_descricao")
        )
        .all()
    )
    return relacoes

# Deleta {ramos} das empresas
@router.delete("/")
def delete_empresa_ramo(id_empresa: int = Query(...), id_ramo: int = Query(...), db: Session = Depends(get_db)):
    relacao = db.query(EmpresaRamo).filter(
        and_(
            EmpresaRamo.id_empresa == id_empresa,
            EmpresaRamo.id_ramo == id_ramo
        )
    ).first()

    if not relacao:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    
    db.delete(relacao)
    db.commit

    return {"mensagem": "Ramo desvinculado da empresa com sucesso!"}

@router.post("/")
def atribuir_ramo(id_empresa: int, id_ramo: int, db: Session = Depends(get_db)):
    existente = db.query(EmpresaRamo).filter_by(id_empresa=id_empresa, id_ramo=id_ramo).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ramo já atribuído à empresa")
    relacao = EmpresaRamo(id_empresa=id_empresa, id_ramo=id_ramo)
    db.add(relacao)
    db.commit()
    return {"mensagem": "Ramo atribuído com sucesso"}