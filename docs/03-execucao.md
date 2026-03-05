# Execucao

## Local
1. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

2. Instale dependencias:
```bash
pip install -r requirements.txt
```

3. Configure `.env` e execute:
```bash
python api.py
```

Com `DEBUG=1`, a aplicacao sobe com Flask dev server.  
Com `DEBUG=0`, sobe com Waitress.

## Docker/Podman
Build da imagem:
```bash
docker build -t vpo_api:latest .
```

Subir com compose:
```bash
podman-compose up -d
```

Mapeamento de porta no `podman-compose.yml`:
- host `5020` -> container `5000`
