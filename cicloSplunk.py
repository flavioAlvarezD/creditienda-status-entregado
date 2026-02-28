import requests
import pandas as pd
from infoVtex import listaVtex
import time
import warnings
warnings.filterwarnings('ignore')

# Toma el archivo directamente en caso de necesitar hacer tests
#listaVtex = pd.read_excel('listaVtex.xlsx')

print('''
    Paso 6: Iniciando proceso de Splunk''')

lista = []
listaVtex = listaVtex.dropna(subset=['guiaV'])

for index, row in listaVtex.iterrows():
    trackingId = row['guiaV']
    fechaInvoice = row['fechaInvoice']
    fechaInvoiceUnix = row['fechaInvoiceUnix']

    print(trackingId, fechaInvoice, fechaInvoiceUnix)

    try:

        url = "https://reportservices.doto.com.mx:8089/services/search/jobs/export"

        payload = f'search=search%20index%3Dshipment%20result.tracking_code%3D{trackingId}%0Aearliest%3D{fechaInvoiceUnix}%20latest%3Dnow%0A%0A%7C%20spath%20result.tracking_code%20output%3DtrackingId%0A%7C%20spath%20result.carrier%20output%3Dcarrier%0A%7C%20spath%20result.tracking_details%7B%7D.status%20output%3Dstatus%0A%7C%20spath%20result.tracking_details%7B%7D.datetime%20output%3DhoraStatus%0A%7C%20eval%20mvEntregado%20%3D%20mvfind(status%2C%20%22Entregado%22)%0A%0A%7C%20eval%20horaEntrega%20%3D%20mvindex(horaStatus%2C%20mvEntregado)%0A%7C%20eval%20horaEntrega%20%3D%20if(isnull(horaEntrega)%2C%20%22enCamino%22%2C%20horaEntrega)%0A%7C%20eval%20horaEntrega%20%3D%20substr(horaEntrega%2C%201%2C%2016)%0A%0A%7C%20dedup%20trackingId%0A%0A%7C%20table%20trackingId%20carrier%20horaEntrega&output_mode=json&preview=false'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': tokenSplunk
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        data = response.json()

        trackingIdS =  data['result']['trackingId'] if "result" in data  else 'sinInfo'
        horaEntrega =  data['result']['horaEntrega'] if "result" in data  else 'noEnviado'
        carrier =  data['result']['carrier'] if "result" in data  else 'sinCarrierAsignado'

        dataSelected = {
            'trackingIdS': trackingIdS,
            'horaEntrega': horaEntrega,
            'carrier': carrier
        }
        lista.append(dataSelected)
        time.sleep(.4)

    except Exception as e:
            print('Error en la guía ', trackingId)
            time.sleep(.4)

listaSplunk = pd.DataFrame(lista)
listaSplunk = pd.concat([listaVtex, listaSplunk], axis=1)
listaSplunk['horaEntrega'] = listaSplunk['horaEntrega'].fillna('sinInfoEnSplunk')
#listaSplunk.to_excel('listaSplunk.xlsx', index=False) # Genera un excel si se desea revisar

# Genera archivo con órdenes que pueden provocar errores
sinLogsEnSplunk = listaSplunk[listaSplunk['horaEntrega'] =='sinInfoEnSplunk']
#sinLogsEnSplunk.to_excel('sinLogsEnSplunk.xlsx', index=False) # Genera un excel si se desea revisar