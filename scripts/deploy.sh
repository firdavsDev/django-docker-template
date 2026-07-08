#!/usr/bin/env bash
#
# Production update script. Run on the VDS after pushing changes:
#
#   ./scripts/deploy.sh [branch]      # default branch: master
#
# What it does:
#   1. git pull the branch
#   2. decide the cheapest safe action from what actually changed:
#      - deps/Dockerfile/compose/.envs changed  -> full rebuild + up -d
#      - only code changed                      -> cached rebuild, swap app
#                                                  containers only (postgres/
#                                                  redis/nginx keep running)
#      - nothing relevant changed (docs etc.)   -> do nothing
#
# Note: code is baked into the image, so a restart alone never picks up new
# code — the "fast path" is a cached rebuild (seconds) + container swap.

set -euo pipefail

BRANCH="${1:-master}"
COMPOSE_FILE="production.yml"

# Services to run. Recommended setup uses host nginx, so the nginx container
# is excluded. Using the containerized nginx instead? Set SERVICES="".
SERVICES="django postgres redis celery celery-beat"
APP_SERVICES="django celery celery-beat"   # rebuilt/swapped on code changes

# Paths that require a FULL rebuild + recreate of everything
FULL_REBUILD_PATTERN='^(compose/production/|production\.yml|pyproject\.toml|uv\.lock)'

ENV_DIR=".envs/.production"
STATE_FILE=".deploy_state"

cd "$(dirname "$0")/.."

log() { echo -e "\033[1;32m[deploy]\033[0m $*"; }

# --- 1. Pull -----------------------------------------------------------------
log "Fetching origin/$BRANCH..."
git fetch origin "$BRANCH"
OLD_REV=$(git rev-parse HEAD)
git merge --ff-only "origin/$BRANCH"
NEW_REV=$(git rev-parse HEAD)

# --- 2. Detect what changed ---------------------------------------------------
CHANGED_FILES=""
if [ "$OLD_REV" != "$NEW_REV" ]; then
    CHANGED_FILES=$(git diff --name-only "$OLD_REV" "$NEW_REV")
    log "Changed files ($OLD_REV -> $NEW_REV):"
    echo "$CHANGED_FILES" | sed 's/^/    /'
fi

# .envs/.production is not tracked by git — detect changes via checksum
ENVS_SUM=$(find "$ENV_DIR" -type f -exec md5sum {} + 2>/dev/null | sort | md5sum | cut -d' ' -f1)
LAST_ENVS_SUM=$(cat "$STATE_FILE" 2>/dev/null || echo "none")
ENVS_CHANGED=0
[ "$ENVS_SUM" != "$LAST_ENVS_SUM" ] && ENVS_CHANGED=1

FULL_REBUILD=0
if [ "$ENVS_CHANGED" = "1" ]; then
    log ".envs/.production changed -> full rebuild"
    FULL_REBUILD=1
elif echo "$CHANGED_FILES" | grep -qE "$FULL_REBUILD_PATTERN"; then
    log "Dependencies / Dockerfiles / compose file changed -> full rebuild"
    FULL_REBUILD=1
fi

# --- 3. Act --------------------------------------------------------------------
if [ "$FULL_REBUILD" = "1" ]; then
    log "Full rebuild + up -d..."
    # shellcheck disable=SC2086
    docker compose -f "$COMPOSE_FILE" up -d --build $SERVICES
elif [ -n "$CHANGED_FILES" ]; then
    log "Code-only change: cached rebuild, swapping app containers..."
    # shellcheck disable=SC2086
    docker compose -f "$COMPOSE_FILE" build $APP_SERVICES
    # shellcheck disable=SC2086
    docker compose -f "$COMPOSE_FILE" up -d --no-deps $APP_SERVICES
else
    log "Nothing changed — nothing to do."
    exit 0
fi

echo "$ENVS_SUM" > "$STATE_FILE"

# --- 4. Verify ------------------------------------------------------------------
log "Waiting for django to answer..."
for i in $(seq 1 30); do
    if curl -fsS -o /dev/null http://127.0.0.1:8000/admin/panel/ 2>/dev/null; then
        log "Django is up ✔"
        break
    fi
    [ "$i" = "30" ] && { log "WARNING: django not answering after 30s — check logs:"; docker compose -f "$COMPOSE_FILE" logs --tail 30 django; exit 1; }
    sleep 1
done

docker compose -f "$COMPOSE_FILE" ps

# reclaim disk from superseded image layers
docker image prune -f > /dev/null
log "Deploy finished: $(git log -1 --oneline)"
