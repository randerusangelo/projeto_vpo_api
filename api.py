from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import os
import io
import base64

#Implementacao dos metodos da api da TargetBank
from buscar_roteiro import buscar_roteiro_service
from consultar_situacao_veiculo_tag import consultar_tags_disponiveis
from obter_custo_rota import obter_custo_rota
from comprar_pegadio_avulso import comprar_pedagio_avulso
from cancelar_compra_vale_pedagio import cancelar_compra_vale_pedagio
from confirmar_pedagio_tag import confirmar_pedagio_tag
from emitir_documento import emitir_documento

import inspect

print("emitir_documento veio de:", inspect.getfile(emitir_documento))
print("assinatura emitir_documento:", inspect.signature(emitir_documento))


load_dotenv()

app = Flask (__name__)

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

#ROTA PARA TESTAR O SERVIDOR
@app.get("/health")
def health():
    return "OK",200

#ROTA PARA BUSCAR ROTEIROS
@app.post("/buscarroteiro") 
def buscarroteiro():
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 400
    
    body = request.get_json() or {}

    try:
        resultado = buscar_roteiro_service(
            qtd_itens_por_pagina=int(body.get("qtd_itens_por_pagina", 99)),
            numero_pagina=int(body.get("numero_pagina", 1)),
            id_roteiro=body.get("id_roteiro"),
            nome_roteiro=body.get("nome_roteiro"),
        )

        return jsonify(resultado), 200
    
    except ValueError:
        return jsonify({"error": "qtd_itens_por_pagina e numero_pagina devem ser numéricos"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#ROTA PARA VER AS TAGS DISPONIVEIS
@app.get("/tagdisponiveis")
def tagdisponiveis():
    placa = request.args.get("placa", "").strip()

    if not placa:
        return jsonify({"error": "placa obrigatória"}), 400
    
    try: 
        resultado = consultar_tags_disponiveis(placa)
        return jsonify(resultado), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#ROTA PARA OBTER CUSTO     
@app.get("/custorota")
def custorota():
    categoria = request.args.get("categoria")
    rota = request.args.get("rota")
    modo = request.args.get("modo")

    if not categoria or not rota or not modo:
        return jsonify({
            "error": "parametros obrigatorios: categoria, rota e modo"
        }), 400
    
    try:
        categoria = int(categoria)
        rota = int(rota)
        modo = int(modo)
    except ValueError:
        return jsonify({"error": "categoria, rota e modo devem ser numéricos"}), 400

    try:
        resultado = obter_custo_rota(
            categoria_veiculo=categoria,
            id_rota_modelo=rota,
            modo_pagamento=modo,
        )

        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#ROTA PARA REALIZAR A COMPRA DO PEDAGIO
@app.post("/comprarpedagio")
def comprarpedagio():
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 400
    
    body = request.get_json()

    obrigatorios = [
        "id_modo",
        "rota",
        "categoria",
        "origem",
        "destino",
        "placa",
        "cnpj",
        "valor",
    ]

    faltando = [campo for campo in obrigatorios if not body.get(campo)]
    if faltando: 
        return jsonify({
            "error": f"Campos obrigatórios faltando: {', '.join(faltando)}"
        }),400
    
    def parse_bool(valor):
        return str(valor).strip().lower() in ("1", "true", "t", "yes", "y", "sim")

    try: 
        resultado = comprar_pedagio_avulso(
            id_modo_compra=int(body["id_modo"]),
            id_rota_modelo=int(body["rota"]),
            codigo_categoria_veiculo=int(body["categoria"]),
            municipio_origem_ibge=int(body["origem"]),
            municipio_destino_ibge=int(body["destino"]),
            placa=body["placa"],
            cpf_cnpj_transportador=body["cnpj"],
            valor_previo_calculado=str(body["valor"]),
            compra_simples=parse_bool(body.get("compra_simples", True)),
            vigencia_horas=int(body.get("vigencia_horas", 24)),

        )

        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}),400
    
    except Exception as e:
        return jsonify({"error": str(e)}),500

#ROTA PARA CANCELAR
@app.post("/cancelarcompra")
def cancelarcomrpa():
    if not request.is_json:
        return jsonify({"error": "Content_Type deve ser application/json"}), 400
    
    body = request.get_json()
    id_compra = body.get("id_compra")
    via_facil = body.get("via_facil", True)

    if not id_compra:
        return jsonify({"error": "id_compra é obrigatório"}), 400
    
    def parse_bool(valor)->bool:
        return str(valor).strip().lower() in ("1", "true", "t", "yes", "y", "sim")
    
    try: 
        resultado = cancelar_compra_vale_pedagio(
            id_compra=int(id_compra),
            via_facil=True,
        )

        return jsonify(resultado), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Rota para Confirmação de compra 
@app.post("/confirmarpedagio")
def confirmarpedagio():
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}),400
    
    body = request.get_json()
    id_compra = body.get("id_compra")

    if not id_compra:
        return jsonify({"error": "id_compra é obrigatório"}), 400
    
    try: 
        resultado = confirmar_pedagio_tag(int(id_compra))
        return jsonify(resultado), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Rota para Emissão de Documento
@app.post("/emitirdocumento")
def emitir_documento():
    if not request.is_json:
        return jsonify({"error": "Content-Type deve ser application/json"}), 400
    
    body = request.get_json() or {}

    tipo_documento = body.get("tipo_documento")
    id_entidade = body.get("id_entidade")
    formato = (body.get("formato") or "pdf").strip().lower()

    if tipo_documento is None or id_entidade is None:
        return jsonify({"error": "Campo obrigatórios: tipo_documento, id_entidade"}), 400

    try: 
        res = emitir_documento(int(tipo_documento), int(id_entidade))

        if not res["ok"]:
            return jsonify({
                "ok": False,
                "erro": res["erro"],
                "raw": res["raw"],
            }), 400
        
        pdf_bytes = res["pdf_bytes"]
        if not pdf_bytes:
            return jsonify({
                "ok": False,
                "error": "DocumentoBinario veio vazio ou em formato inesperado",
                "raw": res["raw"],
            }), 500
        
        if formato == "pdf":
            filename = f"documento_{int(id_entidade)}.pdf"
            return send_file(
                io.BytesIO(pdf_bytes),
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename,
            )
        
        if formato == "json":
            pdf_b64 = base64.b64encode(pdf_bytes).decode("ascii")
            return jsonify({
                "ok": True,
                "tipo_documento": int(tipo_documento),
                "id_entidade": int(id_entidade),
                "pdf_base64": pdf_b64,
            }), 200
        
        return jsonify({"error": "formato inválido. Use 'pdf' ou 'json' ."}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        #debug=DEBUG
    )