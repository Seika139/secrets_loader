# syntax=docker/dockerfile:1
ARG BASE_IMAGE=python:3.9-slim-bookworm

FROM ${BASE_IMAGE} AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock README.md LICENSE src/ tests/ /app/
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry lock --no-interaction --directory /app
RUN poetry install --with dev --no-root --no-interaction --directory /app

FROM ${BASE_IMAGE} AS tester
WORKDIR /app
COPY --from=builder /app /app
RUN pip install --upgrade pip && pip install poetry && poetry install --with dev --no-root --no-interaction --directory /app
