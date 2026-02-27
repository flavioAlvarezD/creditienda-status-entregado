import pandas as pd
import requests
import warnings
warnings.filterwarnings('ignore')
import json
from obtenerCookie import cookie
from cicloSplunk import listaSplunk, sinLogsEnSplunk

# Toma archivos locales para pruebas
#listaSplunk = pd.read_excel('listaSplunk.xlsx')
#sinLogsEnSplunk = pd.read_excel('sinLogsEnSplunk.xlsx')

# Paso previo: otorga permisos a la cookie
print("""
Paso 2: Otorgando Permisos
""")
try:
    url = "https://creditienda-proveedores.concredito.com.mx/api/modulos/20/permisos"

    payload = {}
    headers = {
    'authorization': cookie,
    'Host': 'creditienda-proveedores.concredito.com.mx',
    'Referer': 'https://creditienda-proveedores.concredito.com.mx/'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False, timeout=10)

except Exception as e:
    print("Error al otorgar permisos a la cookie")

# Elimina de la lista órdenes que aún no se han entregado
listaSplunk = listaSplunk.query("horaEntrega not in ['noEnviado', 'enCamino', 'sinInfoEnSplunk']")
listaSplunk = listaSplunk.dropna(subset=['horaEntrega'])
#listaSplunk.to_excel('listaSplunk2.xlsx', index=False) # Genera un excel si se desea revisar

lista = []


for index, row in listaSplunk.iterrows():
    folio = row["folio"][1:]
    numeroOrden = row["numeroOrden"]
    fechaCompra = row["fechaCompra"]
    nombreProducto = row["nombreProducto"]
    sku = row["sku"]
    guia = row["guia"]
    paqueteria = row["paqueteria"]
    fechaInvoice = row["fechaInvoice"]
    horaEntrega = row["horaEntrega"]

    try:

        url = f"https://creditienda-proveedores.concredito.com.mx/creditienda/proveedores/mcreditienda-ordenes/{folio}/aceptar"

        payload = json.dumps({
                                "asignarGuia": True,
                                "contado": "false"
                                })

        headers = {
        'authorization': cookie,
        'referer': f'https://creditienda-proveedores.concredito.com.mxhttps:/creditienda-proveedores.concredito.com.mx/mcreditienda-ordenes/detalle?id={folio}&tipo=false',
        'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        cambioStatus = True if response.status_code == 200 else False

        print(numeroOrden, ": ", response.text)

        dataSelected = {
                       'numeroOrdenS': numeroOrden,
                       'cambioStatus': cambioStatus,
                       'fechaCompra': fechaCompra,
                       'nombreProducto': nombreProducto,
                       'sku': sku,
                       'guia': guia,
                       'paqueteria' : paqueteria,
                       'fechaInvoice': fechaInvoice,
                       'horaEntrega': horaEntrega
                       }
        lista.append(dataSelected)


    except Exception as e:
        print('error')
        dataSelected = {
                       'numeroOrdenS': numeroOrden,
                       'cambioStatus': False,
                       'fechaCompra': fechaCompra,
                       'nombreProducto': nombreProducto,
                       'sku': sku,
                       'guia': guia,
                       'paqueteria' : paqueteria,
                       'fechaInvoice': fechaInvoice,
                       'horaEntrega': horaEntrega
                       }
        lista.append(dataSelected)
        print(numeroOrden, ": ", response.text)

listaStatusEntregado = pd.DataFrame(lista)
numRowsCiclo = listaStatusEntregado.shape[0]
numRowsSinLogs = sinLogsEnSplunk.shape[0]
#listaStatusEntregado.to_excel('listaStatusEntregado.xlsx', index=False) # Genera un excel si se desea revisar

entregadoCD = pd.concat([listaStatusEntregado, sinLogsEnSplunk], axis=0, ignore_index=True)
entregadoCD.to_excel('entregadoCD.xlsx', index=False)