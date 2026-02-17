from datetime import datetime, timedelta, timezone
from zeep.helpers import serialize_object
from lxml import etree
from target_client import make_client, make_auth

def xml_of(envelope):
    return etree.tostring(envelope, pretty_print=True, encoding="unicode")

def comprar_pedagio_avulso(
        id_modo_compra:int,
        id_rota_modelo:int,
        codigo_categoria_veiculo: int,
        municipio_origem_ibge: int,
        municipio_destino_ibge: int,
        placa: str,
        cpf_cnpj_transportador: str,
        valor_previo_calculado: str,
        compra_simples: bool = True,
        vigencia_horas: int = 24,
):
    
    placa = (placa or "").strip().upper()
    if not placa:
        raise ValueError("placa é obrigatória")
    
    cpf_cnpj_transportador = (cpf_cnpj_transportador or "").strip()
    if not cpf_cnpj_transportador:
        raise ValueError("CpfCnpjTransportador é obrigatório")

    inicio = datetime.now(timezone.utc)
    fim = inicio + timedelta(hours=int(vigencia_horas))

    client, service, history = make_client()
    auth = make_auth()

    CompraReq = client.get_type("ns0:CompraValePedagioRequest")

    payload = {
        "IdModoCompraValePedagio": int(id_modo_compra),
        "IdRotaModelo": int (id_rota_modelo), 
        "CodigoCategoriaVeiculo": int(codigo_categoria_veiculo),
        "MunicipioOrigemCodigoIBGE": int(municipio_origem_ibge),
        "MunicipioDestinoCodigoIBGE": int(municipio_destino_ibge),
        "Placa": placa,
        "CpfCnpjTransportador": cpf_cnpj_transportador,
        "InicioVigencia": inicio,
        "FimVigencia": fim,
        "ValorPrevioCalculado": str(valor_previo_calculado),
        "CompraSimples": bool(compra_simples),
    }

    """req = CompraReq(
        IdModoCompraValePedagio=2,          # modo TAG 
        IdRotaModelo=135316,                # IdRotaModelo / IdRotaCliente retornado no cadastrar/obter custo
        CodigoCategoriaVeiculo=14,          # caminhão 9 eixos 
        MunicipioOrigemCodigoIBGE=3150703,  # pirajuba
        MunicipioDestinoCodigoIBGE=3543402, 
        #MunicipioDestinoCodigoIBGE=3548500, # Santos 
        Placa="PPI5E18",
        #MotoristaRNTRC="004389571",
        CpfCnpjTransportador="10667654000127",
        #ItemFinanceiro=False,
        InicioVigencia=inicio,
        FimVigencia=fim,
        ValorPrevioCalculado="386.99",
        CompraSimples=True,
    )"""

    req = CompraReq(**payload)
    resp = service.ComprarPedagioAvulso(auth=auth, compraRequest=req)
    data = serialize_object(resp)
    
    return{
        "request": {
            **payload,
            "InicioVigencia": inicio.isoformat(),
            "FimVigencia": fim.isoformat(),
        },
        "raw": data,
    }

if __name__ == "__main__":
    comprar_pedagio_avulso()