from sqlalchemy import Column, Integer, String
from .database import Base

class CommandModel(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)       # Ex: "Kubernetes Logs"
    template = Column(String)               # Ex: "kubectl logs -f {pod} -n {ns}"
    description = Column(String)
    tags = Column(String)                   # Salvaremos como string separada por vírgula
