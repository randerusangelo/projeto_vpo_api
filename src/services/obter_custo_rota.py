from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

def obter_custo_rota(
        categoria_veiculo: int,
        id_rota_modelo: int,
        modo_pagamento: int,
):
    client, service, history = make_client()
    auth = make_auth()

    Req = client.get_type("ns0:ObtencaoCustoRotaRequest")

    req = Req(
        CategoriaVeiculo=int(categoria_veiculo),
        #IdRotaModelo=135316,
        IdRotaModelo=int(id_rota_modelo),
        ModoPagamentoRota=int(modo_pagamento),  
    )

    resp = service.ObterCustoRota(auth=auth, custoRotaRequest=req)
    data = serialize_object(resp)

    #v_viafacil = data.get("ValorPedagioViaFacil")
    #print("\nValorPedagioViaFacil:", v_viafacil)

    return{
        "request": {
            "CategoriaVeiculo": categoria_veiculo,
            "IdRotaModelo": id_rota_modelo,
            "ModoPagamentoRota": modo_pagamento,
        },
        "valor_viafacil": data.get("ValorPedagioViaFacil"),
        "raw": data,
    }

if __name__ == "__main__":
    obter_custo_rota()
