from cicloCreditienda import listaCD
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Toma el archivo directamente en caso de necesitar hacer tests locales
#listaCD = pd.read_excel('listaCD.xlsx')

tiendaVtex =

print('''
    Paso 5: Iniciando proceso de Vtex''')

lista = []

for index, row in listaCD.iterrows():
    orderId = row['numeroOrden']
    try:
        url = f"https://{tiendaVtex}.vtexcommercestable.com.br/api/oms/pvt/orders/{orderId}"

        payload = {}
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': appkey,
        'X-VTEX-API-AppToken': apptoken
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()
        guia = None if data['packageAttachment']['packages'] == [] else data['packageAttachment']['packages'][0]['trackingNumber']
        fechaInvoice = None if not data['packageAttachment']['packages'] else (datetime.strptime(data['packageAttachment']['packages'][0]['issuanceDate'][:19], "%Y-%m-%dT%H:%M:%S") - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S")
        # Saca el unix de inicio de la hora para poder ejecutar la búsqueda en Splunk
        fechaInvoiceUnix = None if not data['packageAttachment']['packages'] else datetime.strptime(fechaInvoice[:13], "%Y-%m-%dT%H").timestamp()
        sellerId = None if not data['sellers'][0]['id'] else data['sellers'][0]['id']
        print(orderId, '=', response.status_code)

        dataSelected = {
            'orderId': orderId,
            'guiaV': guia,
            'fechaInvoice': fechaInvoice,
            'fechaInvoiceUnix': fechaInvoiceUnix,
            'sellerId': sellerId
        }

        lista.append(dataSelected)
        time.sleep(.4)

    except Exception as e:
        print('Error en la orden ', orderId)
        time.sleep(.4)

listaVtex = pd.DataFrame(lista)
listaVtex = pd.concat([listaCD, listaVtex], axis=1)
#listaVtex.to_excel('listaVtex.xlsx', index=False) # Genera un excel si se desea revisar