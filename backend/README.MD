# 📦 API de Almoxarifado

## 🚀 Instruções de Uso

### 📁 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/) (se for rodar localmente)

---

### 📦 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo/backend
```

---

### 🐳 3. Suba os containers com Docker

```bash
docker compose up --build
```

---

### 🧱 4. Execute as migrações com Alembic

Para criar e aplicar as migrações do banco de dados dentro do container:

```bash
docker exec -it backend-backend-1 python -m scripts.create_migrations upgrade
```

Para gerar uma nova migração após mudar os modelos:

```bash
docker exec -it backend-backend-1 python -m scripts.create_migrations create
```

---

### 👤 5. Crie o usuário administrador

```bash
docker exec -it backend-backend-1 python -m scripts.create_admin
```

---

### 🌐 6. Acesse a API

A API estará disponível em:

```
http://localhost:8000
```

Documentação automática (Swagger UI):

```
http://localhost:8000/docs
```
