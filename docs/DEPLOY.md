# 🚀 VDS Deployment Guide (Ubuntu, from zero)

Full path from a fresh Ubuntu server to a running project. Template-specific steps (env files, logs, compose usage) are in [setup-and-run.md](./setup-and-run.md) — this guide covers the server itself.

**Architecture used here (recommended): host nginx + certbot for TLS, everything else in Docker.** The compose `nginx` service is for the alternative all-in-Docker setup — see §8.3. Never run both: they fight over ports 80/443.

---

## 1. Update & prepare server

```bash
sudo apt update && sudo apt upgrade -y
git --version || sudo apt install -y git
```

---

## 2. Install Docker

```bash
# remove old versions (if any)
sudo apt-get remove docker docker-engine docker.io containerd runc -y

# prerequisites + GPG key
sudo apt-get install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl --retry 5 -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# install (Compose v2 comes as a plugin — no separate install)
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# run docker without sudo
sudo usermod -aG docker $USER
```

👉 **Log out & back in** (or `newgrp docker`), then verify: `docker compose version`.

<details>
<summary>DNS troubleshooting ("Could not resolve host")</summary>

```bash
nslookup download.docker.com   # check resolution

# permanent fix for systemd-based Ubuntu:
sudo nano /etc/systemd/resolved.conf   # add: DNS=8.8.8.8 8.8.4.4
sudo systemctl restart systemd-resolved
```

</details>

---

## 3. SSH access to GitHub

```bash
ssh-keygen -t ed25519 -C "you@email.com" -f ~/.ssh/github_ed25519 -N ""
cat ~/.ssh/github_ed25519.pub
```

Add the public key at **GitHub → Settings → SSH and GPG keys → New SSH Key**, then:

```bash
cat >> ~/.ssh/config <<'EOF'
Host github.com
    IdentityFile ~/.ssh/github_ed25519
EOF

ssh -T git@github.com   # expect: "You've successfully authenticated..."
```

---

## 4. Clone & configure project

```bash
git clone git@github.com:<your-username>/<your-repo>.git
cd <your-repo>

# production env files
cp -r ".envs/.production(example)" .envs/.production
nano .envs/.production/.django     # SECRET_KEY, SERVER_IP, SERVER_DOMAIN, SENTRY_DSN
nano .envs/.production/.postgres   # real DB name/user/password

# generate safe secrets (hex only — no $ # % symbols, they break env parsers)
openssl rand -hex 32   # → SECRET_KEY
openssl rand -hex 24   # → POSTGRES_PASSWORD

# log directory (entrypoint chowns it automatically)
mkdir -p logs
```

---

## 5. Deploy

```bash
# everything except the containerized nginx (host nginx handles TLS, §8)
docker compose -f production.yml up -d --build django postgres redis celery celery-beat

docker ps                                        # all containers Up?
docker compose -f production.yml logs -f django  # watch boot
tail -f logs/errors.log                          # app errors (on host, no volumes needed)
```

Django is bound to `127.0.0.1:8000` — reachable only through nginx.

> ⚠️ Docker published ports **bypass UFW** (Docker writes its own iptables rules). Never publish `0.0.0.0` ports you don't intend to expose — UFW will not save you.

### Updates: one-command redeploy

After pushing changes from local, SSH in and run:

```bash
./scripts/deploy.sh            # pulls master
./scripts/deploy.sh mybranch   # or any branch
```

The script picks the cheapest safe action automatically:

| What changed | Action |
|---|---|
| only code | cached rebuild (~seconds) + swap django/celery containers — postgres/redis/nginx keep running |
| `pyproject.toml` / `uv.lock` / Dockerfiles / `production.yml` | full rebuild + `up -d` |
| `.envs/.production/` (detected via checksum — not in git) | full rebuild + `up -d` |
| nothing relevant (docs etc.) | nothing |

It then health-checks django on `127.0.0.1:8000`, shows container status, and prunes superseded image layers. Using the containerized nginx? Set `SERVICES=""` at the top of the script.

> Code is baked into the image, so a bare container restart never loads new code — the "fast path" is a cached rebuild where only the final `COPY` layer changes.

---

## 6. Database backup & restore

The postgres image ships maintenance scripts (see Makefile):

```bash
docker exec postgres backup                    # create dump
docker exec postgres backups                   # list dumps
docker cp postgres:/backups ./backups          # copy out of container
scp ubuntu@<SERVER_IP>:~/<repo>/backups/*.sql.gz ./   # pull to local machine
docker exec postgres restore <file>.sql.gz     # restore
```

---

## 7. 🔥 Firewall (UFW)

```bash
sudo apt install ufw -y
sudo ufw allow OpenSSH     # FIRST — or you lock yourself out
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status verbose
```

---

## 8. 🕸 nginx reverse proxy + HTTPS

```bash
sudo apt install nginx -y
sudo systemctl enable --now nginx
```

### 8.1 Reverse proxy config

```bash
sudo nano /etc/nginx/sites-available/project.conf
```

```nginx
# rate limiting (anti-flood) — zone defined outside server{}
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

server {
    listen 80;
    server_name YOUR_DOMAIN.COM;

    client_max_body_size 50M;

    location /static/ {
        alias /home/<user>/<repo>/src/static/;   # or serve via whitenoise and drop this
    }

    location / {
        limit_req zone=mylimit burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/project.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

`X-Forwarded-Proto` is required — Django's `SECURE_PROXY_SSL_HEADER` relies on it; without it you get a redirect loop after enabling SSL.

### 8.2 HTTPS (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d YOUR_DOMAIN.COM
sudo certbot renew --dry-run   # verify auto-renewal
```

Certbot rewrites the config for 443 + redirect automatically. Done.

### 8.3 Alternative: containerized nginx

`production.yml` includes an `nginx` service (config: `.envs/.production/nginx.conf`, manual certs in `.envs/.certs/`). To use it instead: **skip §8.1–8.2 entirely, don't install host nginx**, and deploy with plain `docker compose -f production.yml up -d --build`. TLS renewal is manual — that's why host nginx + certbot is the recommended path.

---

## 9. 🔐 Fail2Ban (SSH brute-force protection)

```bash
sudo apt install fail2ban -y
sudo tee /etc/fail2ban/jail.local > /dev/null <<'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5
ignoreip = 127.0.0.1/8

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
EOF

sudo systemctl enable --now fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
```

---

## 10. Post-deploy checklist

- [ ] `https://YOUR_DOMAIN.COM/admin/panel/` opens over HTTPS
- [ ] `http://` redirects to `https://`
- [ ] `curl http://<SERVER_IP>:8000` from outside → connection refused (django is localhost-only)
- [ ] `docker exec postgres backup` works; put it in cron for nightly backups
- [ ] `tail logs/errors.log` — empty or expected content
- [ ] `sudo ufw status` — only 22/80/443 open
- [ ] Sentry receives a test error (`SENTRY_DSN` set)

---

[Telegram](https://t.me/davronbek_dev)
