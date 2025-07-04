from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from models import ColaboradorBase, StatusColaborador
from schemas import ColaboradorCreate
from database import Colaborador, get_db
from utils import remover_acentos, gerar_matricula

def criar_colaborador(db: Session, colaborador: ColaboradorCreate):
    matricula = gerar_matricula(db)
    db_colab = Colaborador(
        matricula=matricula,
        nome=colaborador.nome,
        cpf=colaborador.cpf,
        data_nascimento=colaborador.data_nascimento,
        telefone=colaborador.telefone,
        endereco=colaborador.endereco,
        cargo=colaborador.cargo,
        salario=colaborador.salario,
        status=colaborador.status
    )
    
    db.add(db_colab)
    db.commit()
    db.refresh(db_colab)
    return db_colab

def listar_colaboradores(
    db: Session,
    filtro: str = None,
    status: StatusColaborador = None,
    ordenar_por: str = "matricula",
    ordem: str = "asc"
):
    query = db.query(Colaborador)
    if filtro:
        filtro = remover_acentos(filtro.lower())
        query = query.filter(
            or_(
                Colaborador.nome.ilike(f"%{filtro}%"),
                Colaborador.cpf.ilike(f"%{filtro}%"),
                Colaborador.matricula.ilike(f"%{filtro}%")
            )
        )
    if status:
        query = query.filter(Colaborador.status == status)
    if ordenar_por == "name":
        query = query.order_by(asc(Colaborador.nome) if ordem == "asc" else desc(Colaborador.nome))
    else:
        query = query.order_by(asc(Colaborador.matricula) if ordem == "asc" else desc(Colaborador.matricula))
    return query.all()

def buscar_por_cpf(db: Session, cpf: str):
    return db.query(Colaborador).filter(Colaborador.cpf == cpf).first()

def buscar_por_matricula(db: Session, matricula: str):
    return db.query(Colaborador).filter(Colaborador.matricula == matricula).first()

def editar_colaborador(db: Session, matricula: str, dados: ColaboradorCreate):
    colab = buscar_por_matricula(db, matricula)
    if not colab:
        return None
    for campo, valor in dados.dict().items():
        setattr(colab, campo, valor)
    db.commit()
    db.refresh(colab)
    return colab

def alterar_status(db: Session, matricula: str, novo_status: StatusColaborador):
    colab = buscar_por_matricula(db, matricula)
    if not colab:
        return None
    colab.status = novo_status
    db.commit()
    db.refresh(colab)
    return colab