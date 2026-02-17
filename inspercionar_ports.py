import os
import requests
from zeep import Client
from zeep.transports import Transport


WSDL = os.getenv("TARGET_WSDL", "https://homolog.transportesbra.com.br/frete/TMS/FreteService.svc?singleWsdl")

session = requests.Session()
if os.getenv("TARGET_INSECURE_SSL", "1") == "1":
    session.verify = False

client = Client(wsdl=WSDL, transport=Transport(session=session, timeout=60))

print("\n=== SERVICES / PORTS / OPERAÇÕES ===")

for service_name, service in client.wsdl.services.items():
    print(f"\nService: {service_name}")
    for port_name, port in service.ports.items():
        binding_qname = port.binding.name  # QName
        ops = sorted(list(port.binding._operations.keys()))

        address = None
        try:
            address = port.binding_options.get("address")
        except Exception:
            pass

        print(f"  Port: {port_name}")
        print(f"    Binding QName: {binding_qname}")
        print(f"    Address: {address}")
        print(f"    Ops ({len(ops)}):")
        for op in ops:
            print(f"      - {op}")

