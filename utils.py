import re
import unicodedata
from datetime import datetime

def validar_cpf(cpf: str) -> bool:
    return bool(re.match(r'^\d{11}$', cpf))

def gerar_matricula(db) -> str:
    """Generate next matricula based on in-memory list `db`.

    `db` is expected to be a list of dicts with key 'matricula'.
    """
    ultimo_num = 0
    for item in db:
        m = item.get('matricula')
        if not m:
            continue
        try:
            num = int(m.split('-')[-1])
            if num > ultimo_num:
                ultimo_num = num
        except Exception:
            continue
    proximo_num = ultimo_num + 1
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