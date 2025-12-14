from typing import List, Dict, Optional
from models import ColaboradorBase, StatusColaborador
from schemas import ColaboradorCreate
from database import COLABORADORES
from utils import remover_acentos, gerar_matricula
from fastapi import HTTPException

def criar_colaborador(db: List[Dict], colaborador: ColaboradorCreate):
    # Verifica se CPF já existe
    for c in db:
        if c.get('cpf') == colaborador.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    matricula = gerar_matricula(db)
    novo = {
        'matricula': matricula,
        'nome': colaborador.nome,
        'cpf': colaborador.cpf,
        'data_nascimento': colaborador.data_nascimento,
        'telefone': colaborador.telefone,
        'endereco': colaborador.endereco,
        'cargo': colaborador.cargo,
        'salario': colaborador.salario,
        'status': getattr(colaborador.status, 'value', colaborador.status)
    }
    db.append(novo)
    return novo

def listar_colaboradores(
    db: List[Dict],
    filtro: Optional[str] = None,
    status: Optional[StatusColaborador] = None,
    ordenar_por: str = "matricula",
    ordem: str = "asc"
):
    resultados = list(db)
    if filtro:
        f = remover_acentos(filtro.lower())
        def matches(item):
            nome = remover_acentos(str(item.get('nome', '')).lower())
            cpf = str(item.get('cpf', '')).lower()
            matricula = str(item.get('matricula', '')).lower()
            return f in nome or f in cpf or f in matricula
        resultados = [r for r in resultados if matches(r)]
    if status:
        status_val = getattr(status, 'value', status)
        resultados = [r for r in resultados if r.get('status') == status_val]
    key = 'nome' if ordenar_por == 'name' else 'matricula'
    resultados = sorted(resultados, key=lambda x: x.get(key) or '', reverse=(ordem != 'asc'))
    return resultados

def buscar_por_cpf(db: List[Dict], cpf: str):
    for c in db:
        if c.get('cpf') == cpf:
            return c
    return None

def buscar_por_matricula(db: List[Dict], matricula: str):
    for c in db:
        if c.get('matricula') == matricula:
            return c
    return None

def editar_colaborador(db: List[Dict], matricula: str, dados: ColaboradorCreate):
    colab = buscar_por_matricula(db, matricula)
    if not colab:
        return None
    for campo, valor in dados.dict().items():
        if campo == 'matricula':
            continue
        colab[campo] = valor
    return colab

def alterar_status(db: List[Dict], matricula: str, novo_status: StatusColaborador):
    colab = buscar_por_matricula(db, matricula)
    if not colab:
        return None
    colab['status'] = getattr(novo_status, 'value', novo_status)
    return colab