FROM nginx:1.27-bookworm

ENV APP_HOME=/home/app
ENV LOGS=/home/app/logs

# nginx workers already run as the image's built-in "nginx" user (uid/gid 101);
# the master starts as root and pre-opens the log files, so no custom user is needed.
RUN set -eux; \
    mkdir -p "$APP_HOME" "$LOGS" /etc/nginx/ssl; \
    touch "$LOGS/nginx-access.log" "$LOGS/nginx-error.log"; \
    chown -R nginx:nginx "$APP_HOME" "$LOGS"; \
    rm /etc/nginx/conf.d/default.conf

COPY ./.envs/.production/nginx.conf /etc/nginx/conf.d/
COPY ./.envs/.certs/name.crt /etc/nginx/ssl/name.crt
COPY ./.envs/.certs/name.key /etc/nginx/ssl/name.key
