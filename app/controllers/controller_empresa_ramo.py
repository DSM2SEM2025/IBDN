from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.empresas_model import Empresa
from models.ramo_model import Ramo
from models.empresa_ramo_model import EmpresaRamo

def get_ramos_por_empresa(id_empresa: int, db: Session):
    relacoes = (
        db.query(EmpresaRamo)
        .join(Empresa, Empresa.id == EmpresaRamo.id_empresa)
        .join(Ramo, Ramo.id == EmpresaRamo.id_ramo)
        .filter(EmpresaRamo.id_empresa == id_empresa)
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

def get_empresas_por_ramo(id_ramo: int, db: Session):
    relacoes = (
        db.query(EmpresaRamo)
        .join(Empresa, Empresa.id == EmpresaRamo.Id_empresa)
        .join(Ramo, Ramo.id == EmpresaRamo.id_ramo)
        .filter(EmpresaRamo.id_ramo == id_ramo)
        .with_entities(
            EmpresaRamo.id,
            EmpresaRamo.id_empresa,
            EmpresaRamo.id_ramo,
            Empresa.razao_social.label("empresa_nome"),
            Ramo.nome.label("ramo_nome"),

        )
    )