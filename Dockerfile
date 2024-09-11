FROM python:3.12.5-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

ENV PYTHONUNBUFFERED=1

WORKDIR /app








