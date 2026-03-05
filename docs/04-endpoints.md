# Endpoints

Todos os endpoints (exceto `/health`) esperam `Content-Type: application/json`.

## GET /health
Retorno esperado:
```text
OK
```

## POST /buscarroteiro
Busca roteiros cadastrados.

```json
{
  "qtd_itens_por_pagina": 99,
  "numero_pagina": 1,
  "id_roteiro": null,
  "nome_roteiro": null
}
```

## POST /tagdisponiveis
Consulta disponibilidade de TAG por placa.

```json
{
  "placa": "ABC1D23"
}
```

## POST /custorota
Obtem custo da rota e usa cache Redis por 300s.

```json
{
  "categoria": 14,
  "rota": 135316,
  "modo": 2
}
```

## POST /comprarpedagio
Realiza compra de pedagio avulso.

```json
{
  "id_modo": 2,
  "rota": 135316,
  "categoria": 14,
  "origem": 3150703,
  "destino": 3543402,
  "placa": "ABC1D23",
  "cnpj": "10667654000127",
  "valor": "386.99",
  "compra_simples": true,
  "vigencia_horas": 24
}
```

## POST /cancelarcompra
Cancela uma compra por `id_compra`.

```json
{
  "id_compra": 599266,
  "via_facil": true
}
```

## POST /confirmarpedagio
Confirma pedagio TAG por `id_compra`.

```json
{
  "id_compra": 599266
}
```

## POST /emitirdocumento
Emite documento.
- `formato: pdf` retorna arquivo PDF
- `formato: json` retorna base64 do PDF

```json
{
  "tipo_documento": 4,
  "id_entidade": 599266,
  "formato": "pdf"
}
```

## Exemplo rapido com curl
```bash
curl -X POST http://localhost:5000/custorota \
  -H "Content-Type: application/json" \
  -d "{\"categoria\":14,\"rota\":135316,\"modo\":2}"
```
