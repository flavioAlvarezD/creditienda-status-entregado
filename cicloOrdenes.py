from obtenerCookie import cookie
from obtenerListado import listaFolios
import requests
import pandas as pd

listadoFolios = listaFolios.tolist()

datosOrdenes = []

for folio in (listadoFolios):
  #print(folio)

  url = f"https://creditienda-proveedores.concredito.com.mx/creditienda/mcreditienda-ordenes-proveedores/{folio}/detalle"

  payload = {}
  headers = {
    'Authorization': cookie,
    'Referer': f'https://creditienda-proveedores.concredito.com.mx/mcreditienda-ordenes-proveedores/detalle?id={folio}&tipo=false'
  }

  response = requests.request("GET", url, headers=headers, data=payload, verify=False, timeout=10)

  data = response.json()

  numeroOrden = data.get('numeroOrden')
  fechaCompra = data.get('fechaCompra')
  estatus = data.get('estatus')
  numeroGuia = data.get('numeroGuia')
  paqueteria = data.get('paqueteria')
  nombreProducto = data.get('nombreProducto')
  costo = data.get('costo')

  dataSelected = {
                  'folio': folio,
                  'numeroOrden': numeroOrden,
                  'fechaCompra': fechaCompra,
                  'estatus': estatus,
                  'numeroGuia': numeroGuia,
                  'paqueteria': paqueteria,
                  'nombreProducto': nombreProducto,
                  'costo': costo
                  }
  datosOrdenes.append(dataSelected)

  
df = pd.DataFrame(datosOrdenes)
#df.to_excel("datosDeOrdenes.xlsx", index=False)  # Genera un excel si se desea revisar

print("""
      Paso 3 Realizado con éxito""")
