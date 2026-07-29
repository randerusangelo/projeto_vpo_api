#pronto
from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth
from typing import Any

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

TAG_MAP = {
    "DisponivelSemParar": {"key": "2", "text": "Via Fácil (Sem Parar)"},
    "DisponivelVeloe": {"key": "5", "text": "Veloe"},
    "DisponivelConectCar": {"key": "6", "text": "ConectCar"},
    "DisponivelMoveMais": {"key": "7", "text": "Move Mais"},
    "DisponivelTaggy": {"key": "9", "text": "Taggy"},
}

def extrair_true(dados: Any,wanted_flags: set[str]) -> set[str]:
    found: set[str] = set()

    if isinstance(dados, dict):
        for k, v in dados.items():
            if k in wanted_flags and v is True:
                found.add(k)
            found |= extrair_true(v, wanted_flags)

    elif isinstance(dados, list):
        for item in dados:
            found |= extrair_true(item, wanted_flags)
    return found

def consultar_tags_disponiveis(placa: str):

    placa = (placa or "").strip().upper()
    if not placa:
        raise ValueError("placa é obrigatorio")

    client, service, history = make_client()
    auth = make_auth()

    ConsultaReq = client.get_type("ns0:ConsultaSituacaoVeiculoTAGRequest")

    req = ConsultaReq(Placa = placa)

    resp = service.ConsultarSituacaoVeiculoTAG(
        auth=auth,
        consultaSituacaoVeiculoTAGRequest=req
    )

    data = serialize_object(resp)
    
    wanted_flags = set(TAG_MAP.keys())
    flags_true = sorted(extrair_true(data, wanted_flags))
    tags_sap_disponiveis = [TAG_MAP[f] for f in flags_true]


    return {
        "placa": placa,
        "flags_true": flags_true,
        "tags_sap_disponiveis": tags_sap_disponiveis,
        "raw": data,
    }

if __name__ == "__main__":
    consultar_tags_disponiveis()
    
