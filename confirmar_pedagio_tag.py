from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

def confirmar_pedagio_tag(
        id_compra: int,
):
    
    if not id_compra:
        raise ValueError("id_compra é obrigatório")

    client, service, history = make_client()
    auth = make_auth()

    service = client.bind("FreteService", "BasicHttpBinding_FreteTMSServiceExtended")

    ConfirmaReq = client.get_type("ns0:ConfirmacaoPedagioRequest")
    confirmacao = ConfirmaReq(
        IdCompraValePedagioViaFacil = int(id_compra) #Obtido em comprar pedagio avulso
    )

    resp = service.ConfirmarPedagioTAG(auth=auth, confirmacaoRequest=confirmacao)

    data = serialize_object(resp)

    return{
        "request": {
            "IdCompraValePedagioViaFacil": int(id_compra)
        },
        "raw": data,
    }

if __name__ == "__main__":
    confirmar_pedagio_tag()