import os
import requests
from zeep import Client, Settings
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from dotenv import load_dotenv

load_dotenv()

WSDL = os.getenv("TARGET_WSDL")
SERVICE_EXTENDED_URL = os.getenv("TARGET_ENDPOINT_OVERRIDE")

BINDING_EXTENDED_QNAME = "{http://tmsfrete.v2.targetmp.com.br}BasicHttpBinding_FreteTMSServiceExtended"

def make_client():
    if not WSDL or not SERVICE_EXTENDED_URL:
        raise RuntimeError("TARGET_WSDL ou TARGET_ENDPOINT_OVERRIDE não definidos no .env")

    history = HistoryPlugin()

    session = requests.Session()
    insecure = os.getenv("TARGET_INSECURE_SSL", "0") == "1"
    session.verify = not insecure

    timeout = int(os.getenv("TARGET_TIMEOUT", "60"))

    transport = Transport(session=session, timeout=timeout)
    settings = Settings(strict=False, xml_huge_tree=True)

    client = Client(
        wsdl=WSDL,
        transport=transport,
        settings=settings,
        plugins=[history]
    )

    service = client.create_service(
        BINDING_EXTENDED_QNAME,
        SERVICE_EXTENDED_URL
    )

    return client, service, history

def make_auth():
    user = os.getenv("TARGET_USER")
    password = os.getenv("TARGET_PASS")
    token = os.getenv("TARGET_TOKEN", "")

    if not user or not password:
        raise RuntimeError("TARGET_USER ou TARGET_PASS não definidos no .env")

    return {
        "Usuario": user,
        "Senha": password,
        "Token": token,
    }
