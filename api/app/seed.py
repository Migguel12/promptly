from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models

def seed():
    db: Session = SessionLocal()
    
    # Lista de comandos úteis para popular
    commands = [
        {
            "name": "K8s Get Pods",
            "template": "kubectl get pods -n {namespace}",
            "description": "Lista pods em um namespace",
            "tags": "k8s,infra"
        },
        {
            "name": "Docker Clean Images",
            "template": "docker image prune -a",
            "description": "Remove todas as imagens não utilizadas",
            "tags": "docker,cleanup"
        },
        {
            "name": "K8s Describe Pod",
            "template": "kubectl describe pod {pod_name} -n {namespace}",
            "description": "Detalha um pod específico",
            "tags": "k8s,debug"
        },
        {
            "name": "Git Undo Last Commit",
            "template": "git reset --soft HEAD~1",
            "description": "Desfaz o último commit mantendo os arquivos",
            "tags": "git"
        }
    ]

    for cmd in commands:
        # Verifica se já existe para não duplicar
        exists = db.query(models.CommandModel).filter_by(name=cmd['name']).first()
        if not exists:
            db_command = models.CommandModel(**cmd)
            db.add(db_command)
    
    db.commit()
    db.close()
    print("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    seed()
