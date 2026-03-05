# Operacao e Troubleshooting

## Logs
- Em `DEBUG=1`: log em nivel `DEBUG` no console.
- Em `DEBUG=0`: arquivo rotativo em `logs/api.log` (1MB, 3 backups).

## Erros comuns
- `TARGET_WSDL ou TARGET_ENDPOINT_OVERRIDE nao definidos no .env`
  - Defina ambas as variaveis no `.env`.
- `TARGET_USER ou TARGET_PASS nao definidos no .env`
  - Configure credenciais de autenticacao.
- `Content-Type deve ser application/json`
  - Envie header `Content-Type: application/json`.

## Observacoes
- O endpoint `/custorota` depende de Redis para cache.
- As respostas dos endpoints encapsulam o retorno SOAP no campo `raw`.
