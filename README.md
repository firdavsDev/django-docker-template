![Django project](https://github.com/name/name_api.git)

# Name EXTENSION API


Folder Structure Conventions
============================

> Folder structure options and naming conventions for the current project

### A typical top-level directory layout

    .
    ├── .envs                   # Environment veriables
    ├── compose                 # Docker files and bash commands
    ├── requirements            # Third party libraries
    ├── config                  # Project configuration files 
    ├── src                     # Project applicateions directory ('lib' or 'apps') 
    ├── local.yml               # docker-compose (running in local)
    ├── production.yml          # docker-compose (to deploy in production)
    └── README.md
    └── ...

## Outline

- Prerequisites
- Setup
    - Development
    - Production
- Documentation

## Prerequisites

This project has the following prerequisites

- python 3.11+
- docker 24.0+
- docker compose v2

## Setup

- Type the command below to setup the project locally:

-  docker compose -f local.yml up --build

### Development

- Install virtual environment:

```
git clone https://github.com/orginazation/name_api.git
cd root folder
python -m venv --prompt="v" .env
```

- If *pre commit* has not been installed please install by running following command:

```
pip install pre-commit
pre-commmit install
```

- Type the command below to deploy the project locally:

```
docker compose -f local.yml up -d
```

- You should be good to go now
- http://localhost:8000

### Production
- https://github.com/firdavsDev/docker-template-deployment
