# whishlist-service
API REST para time de marketing de um e-commerce para lista de produtos favoritos dos clientes




## Development

1. Criar um ambiente virtual python


```bash
python -m venv .favorites.env
source .favorites.env/bin/activate
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
