from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth

#limite para cancelar compra é de 2:48 horas

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

def cancelar_compra_vale_pedagio(
        id_compra: int,
        via_facil: bool = True,
):
    
    if not id_compra:
        raise ValueError("id_compra é obrigatório")

    client, service, history = make_client()
    auth = make_auth()

    CancelaReq = client.get_type("ns0:CancelaCompraValePedagioRequest")

    #id_compra = 599266
    #via_facil = True

    req = CancelaReq(
        IdCompraValePedagio=int(id_compra),
        ViaFacil=bool(via_facil),
    )

    resp = service.CancelarCompraValePedagio(auth=auth, cancelaVPRequest=req)
    data = serialize_object(resp)

    return{
        "request":{
            "IdCompraValePedagio": int(id_compra),
            "ViaFacil": bool(via_facil),
        },
        "raw": data,
    }

if __name__ == "__main__":
    cancelar_compra_vale_pedagio()
