from decimal import Decimal
from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

def calcular_pedagio(
        codigo_ibge_origem : int, cep_origem  : str,
        codigo_ibge_destino: int, cep_destino : str,
        categoria_veiculo  : int,
        nome_rota          : str = "CALC_PEDAGIO_PY",
        tipo_caminho       : int = 1
):
    client, service, history = make_client()
    auth = make_auth()

    RotaDetalhadaRequest = client.get_type("ns0:RotaDetalhadaRequest")
    RotaDetalhadaParada = client.get_type("ns0:RotaDetalhadaParada")
    ArrayOfRotaDetalhadaParada = client.get_type("ns0:ArrayOfRotaDetalhadaParada")

    paradas = ArrayOfRotaDetalhadaParada(
        RotaDetalhadaParada=[

            RotaDetalhadaParada(CodigoIBGEMunicipio=codigo_ibge_origem , CEP=cep_origem),
            RotaDetalhadaParada(CodigoIBGEMunicipio=codigo_ibge_destino, CEP=cep_destino),
        ]
    )

    rota = RotaDetalhadaRequest(

        NomeRota=nome_rota,
        CategoriaVeiculo=categoria_veiculo,
        Paradas=paradas,
        RotaTemporaria=False,
        SomenteCalculo=False,
        IdTipoCaminhoRota=tipo_caminho,
    )

    resp = service.CadastrarRoteiroDetalhado(auth=auth, rotaDetalhada=rota)
    data = serialize_object(resp)
    id_rota_cliente = data.get("IdRotaCliente")
    print("\nIdRotaCliente = ", id_rota_cliente)

    pedagios = []
    raw_ped = (data.get("Pedagios") or {})
    raw_list = raw_ped.get("RotaDetalhadaInfoPedagio") if isinstance(raw_ped, dict) else None
    raw_list = raw_list or []

    for p in raw_list:
        pedagios.append({
            "ordem": p.get("Ordem"),
            "nome":p.get("NomePedagio"),
            "categoria":p.get("IdDmCategoriaVeiculo"),
            "valor":float(p.get("Valor") or 0),
        })

    result = {
        "erro": data.get("Erro"),
        "origem": data.get("Origem"),
        "destino": data.get("Destino"),
        "pedagios": pedagios,
        "total_pedagio": float(data.get("ValorTotalPedagio") or 0),
        "soap_enviado": xml_of(history.last_sent["envelope"]),
        "soap_received": xml_of(history.last_received["envelope"]),
    }

    return result

if __name__ == "__main__":
    out = calcular_pedagio(
        codigo_ibge_origem=3150703, cep_origem="38210000", #pirajuba-mg
        #codigo_ibge_destino=3548500, cep_destino="11010020", #santos
        codigo_ibge_destino=3543402, cep_destino="14077230",#ribeirao preto
        categoria_veiculo=14,
        nome_rota="TESTE_ROTA_DETALHADA_PY"
    )

    print(out["total_pedagio"])
    for p in out ["pedagios"]:
        print(p["ordem"], p["nome"], p["valor"])

    