from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ramo_model import Ramo, RamoCreate, RamoOut, RamoUpdate
from models.empresa_ramo_model import EmpresaRamo
from database import get_db

router = APIRouter(prefix="/ramos", tags=["Ramos"])

@router.post("/", response_model=RamoOut)
def create_ramo(ramo: RamoCreate, db: Session = Depends(get_db)):
    novo_ramo = Ramo(**ramo.dict())
    db.add(novo_ramo)
    db.commit()
    db.refresh(novo_ramo)

    return novo_ramo

@router.put("/{ramo_id}", response_model=RamoOut)
def update_ramo(ramo_id: int, dados: RamoUpdate, db: Session = Depends(get_db)):
    ramo = db.query(Ramo).filter(Ramo.id == ramo_id).first()
    if not ramo:
        raise HTTPException(status_code=404, datail="Ramo não encontrado")
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(ramo, key, value)
    db.cammit()
    db.refresh(ramo)
    return ramo