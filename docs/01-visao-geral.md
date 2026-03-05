# Visao Geral

A `target_vpo` e uma API Flask para integracao com o servico de Vale Pedagio Obrigatorio (Target/TMS Frete).

## Tecnologias
- Python 3.12
- Flask + Waitress
- Zeep (SOAP)
- Redis (cache para `/custorota`)

## Estrutura do projeto
```text
.
|-- api.py
|-- target_client.py
|-- src/services/
|   |-- buscar_roteiro.py
|   |-- consultar_situacao_veiculo_tag.py
|   |-- obter_custo_rota.py
|   |-- comprar_pegadio_avulso.py
|   |-- cancelar_compra_vale_pedagio.py
|   |-- confirmar_pedagio_tag.py
|   `-- emitir_documento.py
|-- requirements.txt
|-- Dockerfile
`-- podman-compose.yml
```
