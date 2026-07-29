from zeep.helpers import serialize_object
from lxml import etree
import base64
from target_client import make_client, make_auth

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

def tem_erro(data: dict) -> tuple[bool, dict | None]:
    err = data.get("Erro")
    if not err:
        return False, None

    msg = err.get("MensagemErro") or err.get("Mensagem") 
    cod = err.get("CodigoErro")
    cod_esp = err.get("CodigoErroEspecifico")

    existe =  any(v not in (None, "") for v in (msg, cod, cod_esp))
    return existe, err if existe else None

def normalizar_pdf_bytes(valor):

    if valor is None:
        return None

    if isinstance(valor, (bytes, bytearray)):
        return bytes(valor)

    if isinstance(valor, str):
        try:
            return base64.b64decode(valor, validate=True)
        except Exception:
            return None
    return None

def emitir_documento_service(
        tipo_documento: int,
        id_entidade: int
):
    


    client, service, history = make_client()
    auth = make_auth()

    EmissaoReq = client.get_type("ns0:EmissaoDocumentoRequest")

    #tipo_documento = 4   #4 = ReciboPedagioTAG
    #id_entidade = 599266

    req = EmissaoReq(
        Tipo=int(tipo_documento),
        IdEntidade=int(id_entidade)
    )

    resp = service.EmitirDocumento(auth=auth, emissaoDocumento=req)
    data = serialize_object(resp)

    has_error, err_obj = tem_erro(data)
    if has_error:
        return{
            "ok": False,
            "erro": err_obj,
            "raw": data,
            "pdf_bytes": None,
        }

    pdf_bytes = normalizar_pdf_bytes(data.get("DocumentoBinario"))

    return{
        "ok": True,
        "erro": None,
        "raw": data,
        "pdf_bytes": pdf_bytes,
    }

if __name__ == "__main__":
    r = emitir_documento_service(4, 600446)
    print(r)
