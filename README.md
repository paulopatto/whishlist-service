# whishlist-service

API REST para time de marketing de um e-commerce para lista de produtos favoritos dos clientes


Documentação da API disponível em: http://localhost:8000/docs

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
docker-compose up -d
```

ou apenas alguns serviços específicos:

```bash
# Banco de dados
docker-compose up postgres -d

# API de produtos
docker-compose up product-api -d
```

4. Run tests

```bash
python -m pytest
```

5. Running lints

```bash
ruff check . --select E,F,I --fix
```

