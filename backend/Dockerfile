FROM python:3.12-slim

# Define o diretório principal de trabalho
WORKDIR /app

# Copia os arquivos de dependência
COPY pyproject.toml poetry.lock* ./

# Instala o Poetry e dependências
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --without dev

# Copia o código da aplicação 
COPY . .

# Expõe a porta e inicia o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
