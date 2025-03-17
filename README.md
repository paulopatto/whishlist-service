# whishlist-service

API REST para time de marketing de um e-commerce para lista de produtos favoritos dos clientes

## Development

1. Criar um ambiente virtual python

```bash
python -m venv .favorites.env
source .favorites.env/bin/activate

# Copiar o .env-sample e configurar os valores
cp .env-sample .env
```

2. Instalar as dependências

```bash
pip install -r REQUIREMENTS
```

3. Executar o servidor (modo dev)

```bash
uvicorn src.main:app --reload
```

3.1. Executar o servidor via docker localmente

```bash
docker build -t favorites-service:development .
docker run -p 8000:8000 favorites-service:development
```

3.2 Executar o servidor via docker localmente com docker-compose

```bash
docker-compose up
```

ou apenas o banco de dados

```bash
docker-compose up db
```

4. Run tests

```bash
python -m pytest
```

5. Running lints

```bash
ruff check . --select E,F,I --fix
```

