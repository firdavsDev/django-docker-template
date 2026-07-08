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
  && apt-get install -y gettext \
  # privilege drop in entrypoint (root fixes ./logs ownership, then gosu django)
  && apt-get install -y gosu \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p $HOME
RUN mkdir $APP_HOME


RUN addgroup --system django \
    && adduser --system --ingroup django django


# Dependencies are installed here to ensure they will be cached.
COPY ./pyproject.toml ./uv.lock /deps/
RUN cd /deps && uv sync --frozen --no-install-project --no-dev --extra production \
    && rm -rf /deps

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start



COPY --chown=django:django . $APP_HOME

RUN mkdir $APP_HOME/src/static
RUN chown django $APP_HOME/src/static

RUN mkdir $APP_HOME/src/media
RUN chown django $APP_HOME/src/media

RUN mkdir -p $APP_HOME/logs
RUN chown django $APP_HOME/logs


# No USER directive: entrypoint starts as root to chown the bind-mounted
# logs dir, then drops to the django user via gosu.

WORKDIR $APP_HOME

ENTRYPOINT ["/entrypoint"]
