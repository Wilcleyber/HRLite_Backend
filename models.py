from pydantic import BaseModel, Field, validator
from enum import Enum
import re

class StatusColaborador(str, Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"

class ColaboradorBase(BaseModel):
    nome: str = Field(..., example="Joao Silva")
    cpf: str = Field(..., example="12345678900")
    data_nascimento: str = Field(..., example="1990-01-01")
    telefone: str = Field(..., example="(11) 91234-5678")
    endereco: str = Field(..., example="Rua das Flores, 123")
    cargo: str = Field(..., example="Analista de Sistemas")
    salario: float = Field(..., example=3500.00)
    status: StatusColaborador = StatusColaborador.ATIVO
    
class ColaboradorCreate(ColaboradorBase):
    pass

class ColaboradorOut(ColaboradorBase):
    matricula: str = Field(...,example="COL-001")