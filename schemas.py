from pydantic import BaseModel, Field, field_validator
from enum import Enum
from utils import validar_cpf, parse_date_to_iso, remover_acentos
import re

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

    # Valida/normaliza CPF: remove tudo que não for número e checa 11 dígitos
    @field_validator('cpf', mode='before')
    def cpf_valido(cls, v):
        v_str = re.sub(r'\D', '', str(v or ''))
        if not validar_cpf(v_str):
            raise ValueError("CPF inválido. Digite 11 números.")
        return v_str

    # Normaliza data para ISO (aceita DD/MM/YYYY ou YYYY-MM-DD)
    @field_validator('data_nascimento', mode='before')
    def data_iso(cls, v):
        try:
            return parse_date_to_iso(str(v))
        except ValueError:
            raise ValueError("Data de nascimento inválida. Use o formato DD/MM/AAAA ou YYYY-MM-DD.")

    # Remove acentos do nome (ex.: "João" -> "Joao")
    @field_validator('nome', mode='before')
    def nome_sem_acentos(cls, v):
        return remover_acentos(str(v or ''))

class ColaboradorOut(ColaboradorCreate):
    matricula: str = Field(..., json_schema_extra={"example": "COL-001"})

    model_config = {
        "from_attributes": True
    }