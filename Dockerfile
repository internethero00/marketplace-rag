FROM python:3.12-slim AS builder

ENV POETRY_VERSION=2.4.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_NO_CACHE_DIR=1

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only main --no-root

COPY src ./src
RUN poetry install --only main


FROM python:3.12-slim AS runtime

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home --uid 1000 app

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY src ./src
COPY alembic.ini ./
COPY migrations ./migrations

USER app

EXPOSE 8000

CMD ["uvicorn", "marketplace_rag.main:app", "--host", "0.0.0.0", "--port", "8000"]
