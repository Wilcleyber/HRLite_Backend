from sqlalchemy import create_engine, Column, Integer, String, Float, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from models import StatusColaborador

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Colaborador(Base):
    __tablename__ = "colaboradores"

    matricula = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    data_nascimento = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    salario = Column(Float, nullable=False)
    status = Column(Enum(StatusColaborador), default=StatusColaborador.ATIVO, nullable=False)

def criar_tabelas():
    Base.metadata.create_all(bind=engine)