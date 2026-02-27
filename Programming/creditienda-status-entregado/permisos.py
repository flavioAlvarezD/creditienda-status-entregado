import requests
from obtenerCookie import cookie

print("""
Otorgando Permisos
""")

url = "https://creditienda-proveedores.concredito.com.mx/api/modulos/20/permisos"

payload = {}
headers = {
  'authorization': cookie,
  'Host': 'creditienda-proveedores.concredito.com.mx',
  'Referer': 'https://creditienda-proveedores.concredito.com.mx/'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
