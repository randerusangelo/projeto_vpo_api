# Configuracao

Use o arquivo `.env.example` como base:

```bash
cp .env.example .env
```

## Variaveis TARGET
- `TARGET_WSDL`: URL ou caminho do WSDL.
- `TARGET_ENDPOINT_OVERRIDE`: endpoint SOAP do servico Target.
- `TARGET_USER`: usuario de autenticacao.
- `TARGET_PASS`: senha de autenticacao.
- `TARGET_TOKEN`: token adicional (opcional).
- `TARGET_TIMEOUT`: timeout HTTP em segundos (padrao: `60`).
- `TARGET_INSECURE_SSL`: `1` para desabilitar validacao SSL, `0` para habilitar.

## Variaveis da API
- `HOST`: host da API (padrao: `0.0.0.0`).
- `PORT`: porta da API (padrao no codigo: `5000`).
- `DEBUG`: `1/true` ativa modo debug Flask.
- `THREADS`: threads do Waitress (padrao: `4`).
- `CONNECTION_LIMIT`: limite de conexoes (padrao: `100`).
- `CHANNEL_TIMEOUT`: timeout de canal do Waitress (padrao: `30`).

## Variaveis Redis
- `REDIS_HOST`: host Redis para cache Flask-Caching.
- `REDIS_PORT`: porta Redis (padrao: `6379`).
- `REDIS_DB`: banco Redis (padrao: `0`).
