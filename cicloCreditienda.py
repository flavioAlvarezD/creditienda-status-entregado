from obtenerListado import orderList, cookie
import requests
import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')


print('''
      Paso 4: Iniciando proceso de Creditienda''')

lista = []

for index, row in orderList.iterrows():
    id = row['id']
    print(f'Buscando orden {id}')

    try:
        url = f"https://creditienda-proveedores.concredito.com.mx/creditienda/proveedores/mcreditienda-ordenes/{id}/detalle"

        payload = {}
        headers = {
        'Authorization': cookie,
        'Referer': f'https://creditienda-proveedores.concredito.com.mx/mcreditienda-ordenes/detalle?id={id}&tipo=false'
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        data = response.json()

        dataSelected = {
            'numeroOrden': data['numeroOrden'],
            'fechaCompra': data['fechaCompra'],
            'sku': data['sku'],
            'estatus': data['estatus'],
            'guia': data['numeroGuia'],
            'paqueteria': data['paqueteria'],
            'nombreProducto': data['nombreProducto'],
            'folio': data['folio']
        }

        lista.append(dataSelected)

        time.sleep(.4)

    except Exception as e:
        print('Error en la orden ', id)
        time.sleep(.2)

listaCD = pd.DataFrame(lista)
listaCD['numeroOrden'] = listaCD['numeroOrden'] + '-01'
#listaCD.to_excel('listaCD.xlsx', index=False) # Genera un excel si se desea revisar