from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, enconding="unicode")

def buscar_roteiro_service(
        qtd_itens_por_pagina: int = 99,
        numero_pagina: int = 1,
        id_roteiro: int | None = None,
        nome_roteiro: str | None = None,
):
    
    client, service, history = make_client()
    auth = make_auth()

    BuscaReq = client.get_type("ns0:BuscaRoteiroRequest")

    busca = BuscaReq(
        QuantidadeItensPorPagina=int(qtd_itens_por_pagina),
        NumeroPagina=int(numero_pagina),
        IdRoteiro=id_roteiro,
        NomeRoteiro=nome_roteiro,
    )

    resp = service.BuscarRoteiro(
        auth=auth,
        buscaRoteiro=busca
    )

    data = serialize_object(resp)

    return{
        "request": {
            "QuantidadePorPagina": int(qtd_itens_por_pagina),
            "NumeroPagina": int(numero_pagina),
            "IdRoteiro": id_roteiro,
            "NomeRoteiro": nome_roteiro,
        },

        "raw": data,
    }

if __name__ == "__main__":
    buscar_roteiro_service()