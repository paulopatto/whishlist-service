FROM python:3.12-slim

ARG PORT=8000
ARG PYTHON_ENV=production

ENV PORT=${PORT}
ENV PYTHON_ENV=${PYTHON_ENV}
ENV PYTHONPATH=/app

WORKDIR /app
COPY REQUIREMENTS .
RUN pip install --no-cache-dir -r REQUIREMENTS

COPY src/ ./src/

EXPOSE ${PORT}

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
