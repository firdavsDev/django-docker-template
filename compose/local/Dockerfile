FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# uv — fast package manager (https://docs.astral.sh/uv/)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
# Install straight into the system interpreter (no .venv inside the container)
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_COMPILE_BYTECODE=1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg dependencies
  && apt-get install -y libpq-dev libmagic-dev \
  # Translations dependencies
  && apt-get install -y gettext nodejs npm \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Dependencies are installed here to ensure they will be cached.
COPY ./pyproject.toml ./uv.lock /app/
RUN cd /app && uv sync --frozen --no-install-project --group dev

COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app
