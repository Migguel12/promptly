from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database

# Cria as tabelas no banco de dados SQLite automaticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Promptly API")

@app.post("/commands/", response_model=schemas.Command)
def create_command(command: schemas.CommandCreate, db: Session = Depends(database.get_db)):
    # Criando o comando no banco
    db_command = models.CommandModel(
        name=command.name,
        template=command.template,
        description=command.description,
        tags=command.tags
    )
    db.add(db_command)
    db.commit()
    db.refresh(db_command)
    return db_command

@app.get("/commands/", response_model=List[schemas.Command])
def read_commands(q: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.CommandModel)
    if q:
        # Busca simples que olha no nome ou nas tags
        query = query.filter(
            models.CommandModel.name.contains(q) | 
            models.CommandModel.tags.contains(q)
        )
    return query.all()

@app.get("/")
def health_check():
    return {"status": "online", "project": "Promptly"}

@app.delete("/commands/{command_id}")
def delete_command(command_id: int, db: Session = Depends(database.get_db)):
    db_command = db.query(models.CommandModel).filter(models.CommandModel.id == command_id).first()
    if not db_command:
        raise HTTPException(status_code=404, detail="Comando não encontrado")

    db.delete(db_command)
    db.commit()
    return {"message": f"Comando {command_id} deletado com sucesso"}
