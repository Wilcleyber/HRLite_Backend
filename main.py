from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import criar_tabelas, get_db
from schemas import ColaboradorCreate, ColaboradorOut, StatusColaborador
from fastapi.middleware.cors import CORSMiddleware
import crud

app = FastAPI(title="HRLite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

criar_tabelas()

@app.post("/colaboradores", response_model=ColaboradorOut)
def criar_colaborador(colaborador: ColaboradorCreate, db: Session = Depends(get_db)):
    db_colab = crud.criar_colaborador(db, colaborador)
    return db_colab

@app.get("/colaboradores", response_model=List[ColaboradorOut])
def listar_colaboradores(
    filtro: Optional[str] = Query(None, description="Filter by name, CPF, or matricula."),
    status: Optional[StatusColaborador] = Query(None, description="Filter by status."),
    ordenar_por: str = Query("matricula", description="Order by 'name' or 'matricula'."),
    ordem: str = Query("asc", description="asc or desc."),
    db: Session = Depends(get_db)
):
    return crud.listar_colaboradores(db, filtro, status, ordenar_por, ordem)

@app.get("/colaboradores/{matricula}", response_model=ColaboradorOut)
def obter_colaborador(matricula: str, db: Session = Depends(get_db)):
    colab = crud.buscar_por_matricula(db, matricula)
    if not colab:
        raise HTTPException(status_code=404, detail="Employee not found")
    return colab

@app.put("/colaboradores/{matricula}", response_model=ColaboradorOut)
def editar_colaborador(matricula: str, dados: ColaboradorCreate, db: Session = Depends(get_db)):
    colab = crud.editar_colaborador(db, matricula, dados)
    if not colab:
        raise HTTPException(status_code=404, detail="Employee not found")
    return colab

@app.patch("/colaboradores/{matricula}/status", response_model=ColaboradorOut)
def alterar_status(matricula: str, status: StatusColaborador, db: Session = Depends(get_db)):
    colab = crud.alterar_status(db, matricula, status)
    if not colab:
        raise HTTPException(status_code=404, detail="Employee not found")
    return colab