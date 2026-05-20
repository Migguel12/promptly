import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/promptly")

def get_engine():
    retries = 5
    while retries > 0:
        try:
            # Tenta criar o engine e conectar
            engine = create_engine(DATABASE_URL)
            engine.connect()
            print("Conexão com o PostgreSQL estabelecida com sucesso!")
            return engine
        except OperationalError:
            retries -= 1
            print(f"Banco de dados ainda não está pronto... Tentando novamente em 3s ({retries} tentativas restantes)")
            time.sleep(3)

    raise Exception("Erro fatal: Não foi possível conectar ao banco de dados após várias tentativas.")

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
