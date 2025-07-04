from pydantic import BaseModel, Field, field_validator
from enum import Enum
from utils import validar_cpf, parse_date_to_iso, remover_acentos

class StatusColaborador(str, Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"

class ColaboradorCreate(BaseModel):
    nome: str = Field(..., json_schema_extra={"example": "Joao Silva"})
    cpf: str = Field(..., json_schema_extra={"example": "12345678900"})
    data_nascimento: str = Field(..., json_schema_extra={"example": "1990-01-01"})
    telefone: str = Field(..., json_schema_extra={"example": "(11) 91234-5678"})
    endereco: str = Field(..., json_schema_extra={"example": "Rua das Flores, 123"})
    cargo: str = Field(..., json_schema_extra={"example": "Analista de Sistemas"})
    salario: float = Field(..., json_schema_extra={"example": 3500.00})
    status: StatusColaborador = StatusColaborador.ATIVO

    @field_validator('cpf')
    def cpf_valido(cls, v):
        if not validar_cpf(v):
            raise ValueError("Invalid CPF. Enter 11 digits.")
        return v

    @field_validator('data_nascimento')
    def data_iso(cls, v):
        return parse_date_to_iso(v)

    @field_validator('nome')
    def nome_sem_acentos(cls, v):
        return remover_acentos(v)

class ColaboradorOut(ColaboradorCreate):
    matricula: str = Field(..., json_schema_extra={"example": "COL-001"})

    class Config:
        from_attributes = True