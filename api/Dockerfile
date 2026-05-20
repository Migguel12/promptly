# Usando uma imagem leve do Python baseada em Debian Bookworm
FROM python:3.11-slim-bookworm

WORKDIR /app

# Instalando dependências de sistema básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Expondo a porta da API
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
