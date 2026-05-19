import requests
from decimal import Decimal
from django.conf import settings

BASE_URL = "https://v6.exchangerate-api.com/v6"

def convertir_moneda(precio_Arg, moneda_de_paso):
    api_key = settings.EXCHANGE_API_KEY
    url=f"{BASE_URL}/{api_key}/latest/ARS"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    tasa= data["conversion_rates"].get(moneda_de_paso)
    if tasa is None:
        raise Exception(f"Tasa de cambio no encontrada para {moneda_de_paso}")

    return round(precio_Arg * tasa, 2)