import re
import unicodedata
from sqlalchemy.orm import Session
from datetime import datetime
from database import Colaborador

def validar_cpf(cpf: str) -> bool:
    return bool(re.match(r'^\d{11}$', cpf))

def gerar_matricula(db: Session) -> str:
    ultimo = db.query(Colaborador).order_by(Colaborador.matricula.desc()).first()
    if not ultimo or not ultimo.matricula:
        proximo_num = 1
    else:
        try:
            proximo_num = int(ultimo.matricula.split('-')[-1]) + 1
        except Exception:
            proximo_num = 1
    return f"COL-{proximo_num:03d}"

def parse_date_to_iso(date_str: str) -> str:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError("Date format must be ISO (YYYY-MM-DD) or common formats like DD/MM/YYYY.")

def remover_acentos(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )