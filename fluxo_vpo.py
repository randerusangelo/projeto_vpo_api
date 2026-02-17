from target_client import make_client, build_auth

TAG_PLACA = "CNR9E15"
TAG_CNPJ = "04307343000154"
TAG_RNTRC = "004389570"

ORIGEM_CEP = "38010210" 
DESTINO_CEP = "14780260"

def main():
    client, history = make_client()
    auth = build_auth(client)

    RoteiroReq = client.get_type("ns0:CadastroRoteiroCustomizadoRequest")
    CustoReq   = client.get_type("ns0:ObtencaoCustoRotaRequest")
    CompraReq  = client.get_type("ns0:CompraValePedagioRequest")
    ConfReq    = client.get_type("ns0:ConfirmacaoPedagioRequest")

    resp_roteiro = RoteiroReq()
    print("\n >>> RESP ROTEIRO: ", resp_roteiro)

    id_roteiro = getattr(resp_roteiro, "IdRoteiro", None) or getattr(resp_roteiro, "idRoteiro", None)
    print("ID Roteiro (tentariva):", id_roteiro)

    custo_req = CustoReq(

    )
    resp_custo = client.service.ObterCustoRota(auth=auth, custoRotaRequest=custo_req)
    print("\n>>> RESP CUSTO:", resp_custo)

    valor_viafacil = getattr(resp_custo, "ValorPedagioViaFacil", None) or getattr(resp_custo, "valorPedagioViaFacil", None )
    print("ValorPedagioViaFacil (tentativa):", valor_viafacil)

    compra_req = CompraReq()

    resp_compra = client.service.ComprarPedagioAvulso(auth=auth, CompraRequest=compra_req)
    print("\n>>> RESP COMPRA:", resp_compra)

    id_compra = getattr(resp_compra, "IdCompraValePedagio", None) or getattr(resp_compra, "idCompraValePegagio", None)
    print("ID Compra (tentativa):", id_compra)

    conf_req = ConfReq()
    resp_conf = client.service.ConfirmarPedagioTAG(auth=auth, confirmacaoRequest=conf_req)
    print("\n>>> RESP CONFIRMA:", resp_conf)

    sent = history.last_sent["envelope"].decode("utf-8")
    received = history.last_received["envelope"].decode("utf-8")
    print("\n === SOAP ENVIADO  (última) ===\n", sent)
    print("\n === SOAP RECEBIDO (última) ===\n", received)

if __name__ == "__main__":
    main()