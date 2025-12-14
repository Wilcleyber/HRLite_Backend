from typing import Iterator, List, Dict
from models import StatusColaborador

# In-memory storage: a list of collaborator dicts
COLABORADORES: List[Dict] = []

def get_db() -> Iterator[List[Dict]]:
    """Dependency replacement: yields the in-memory list acting as the database."""
    yield COLABORADORES

def criar_tabelas():
    """No-op initializer for compatibility with existing startup code.

    Also ensures a default example collaborator exists so it remains present
    while the API process is running.
    """
    if not COLABORADORES:
        exemplo = {
            "matricula": "COL-001",
            "nome": "Exemplo Usuario",
            "cpf": "00000000000",
            "data_nascimento": "1990-01-01",
            "telefone": "(00) 00000-0000",
            "endereco": "Endereco Exemplo, 1",
            "cargo": "Exemplo",
            "salario": 0.0,
            "status": StatusColaborador.ATIVO.value
        }
        COLABORADORES.append(exemplo)