
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg dependencies
  && apt-get install -y libpq-dev libmagic-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p $HOME
RUN mkdir $APP_HOME


RUN addgroup --system django \
    && adduser --system --ingroup django django


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start



COPY --chown=django:django . $APP_HOME

RUN mkdir -p $APP_HOME/src/static
RUN chown django $APP_HOME/src/static

RUN mkdir -p $APP_HOME/src/media
RUN chown django $APP_HOME/src/media


USER django

WORKDIR $APP_HOME

ENTRYPOINT ["/entrypoint"]
