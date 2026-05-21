# 🚀 Promptly

O **Promptly** é um gerenciador de snippets e comandos técnicos focado em produtividade para DevOps e Desenvolvedores. Ele permite gerenciar comandos complexos com variáveis (como `{namespace}` ou `{pod_name}`) através de uma API robusta e invocá-los globalmente no Linux através de uma interface fluida com o Rofi, copiando o comando final direto para o seu Clipboard (`Ctrl + V`).

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Banco de Dados:** PostgreSQL 15
- **Orquestração:** Docker & Docker Compose
- **Client (Linux Host):** Bash, Rofi, JQ, Xclip

## 🏗️ Arquitetura e Resiliência DevOps

O projeto foi desenhado seguindo boas práticas de infraestrutura:
- **Docker Healthchecks:** A API aguarda estritamente o container do PostgreSQL estar saudável (`service_healthy`) antes de iniciar.
- **Retry Logic:** O backend possui uma lógica de re-tentativa de conexão com o banco de dados (5 retries espaçados), garantindo resiliência contra falhas de inicialização de rede.
- **Persistência:** Dados mapeados via Docker Volumes locais.

---

## 🚀 Como Rodar o Projeto (Setup Rápido)

Se você quer testar o projeto na sua máquina local, siga os passos abaixo.

### 1. Pré-requisitos e Instalação Local (Host)
A API roda dentro do Docker, mas a interface do Rofi precisa rodar diretamente no seu sistema operacional (Ubuntu/Debian) para capturar o teclado. No seu terminal local, instale as ferramentas necessárias:

```bash
sudo apt update && sudo apt install rofi xclip jq curl -y
```

### 2. Clonar e Subir a Infraestrutura
```bash
# Clonar o repositório
git clone [https://github.com/migguelprs/promptly.git](https://github.com/migguelprs/promptly.git)
cd promptly

# Subir os containers (API + Banco)
docker compose up -d --build
```

### 3. Popular o Banco de Dados (Seed)
Para não começar com o banco vazio, execute o script para carregar alguns comandos úteis de Kubernetes, Docker e Git:
```bash
docker exec -it promptly_api python -m app.seed
```

### 4. Configurar o Atalho Global (Client)
Dê permissão de execução para o script local:
```bash
chmod +x client/promptly.sh
```

**Configuração do Atalho no Ubuntu (Evitando problemas de foco):**
1. Vá em **Configurações -> Teclado -> Atalhos de Teclado -> Atalhos Personalizados**.
2. Clique em `+` e preencha:
   - **Nome:** `Promptly`
   - **Comando:** `env GDK_BACKEND=x11 /caminho/completo/para/promptly/client/promptly.sh`
   - **Atalho:** Escolha uma combinação que não conflite com o sistema (Alt + Space costuma dar conflito no GNOME, por isso recomendamos **Super + Z**).

---

## 🔌 Endpoints da API

Com os containers rodando, você pode acessar a documentação interativa (Swagger) em:
🔗 **http://localhost:8000/docs**

- `GET /commands/` - Lista ou busca comandos filtrados.
- `POST /commands/` - Cadastra um novo snippet.
- `DELETE /commands/{id}` - Remove um comando por ID.
