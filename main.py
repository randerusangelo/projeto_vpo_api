import os
from dotenv import load_dotenv
import requests
import urllib3
from zeep import Client
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin

load_dotenv()

WSDL = os.getenv("TARGET_WSDL")
USER = os.getenv("TARGET_USER")
PASS = os.getenv("TARGET_PASS")
TIMEOUT = int(os.getenv("TARGET_TIMEOUT", "60"))
INSECURE_SSL = os.getenv("TARGET_INSECURE_SSL", "1") == "1"

print("WSDL:", WSDL)
print("Usuário:", USER)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()
session.auth = (USER, PASS)
session.verify = False  # homolog (cert self-signed)

client = Client(wsdl=WSDL, transport=Transport(session=session, timeout=TIMEOUT))

print("\n=== OPERAÇÕES DISPONÍVEIS NO WSDL ===")

for service in client.wsdl.services.values():
    print(f"\nService: {service.name}")

    for port_name, port in service.ports.items():
        print(f" Port: {port_name}")

        # Endpoint (forma compatível)
        address = None
        try:
            # SOAP 1.1/1.2 address costuma ficar nos binding_options
            address = port.binding_options.get("address")
        except Exception:
            pass

        if not address:
            # fallback: tenta extrair de __dict__ (debug)
            address = getattr(port, "address", None)

        print(f" Endpoint: {address}")

        # Lista operações
        for op in port.binding._operations.keys():
            print(f"  - {op}")
