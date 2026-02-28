from obtenerCookie import cookie
from config import fechaFin, fechaInicio
import requests
import pandas as pd
from tkinter import messagebox, Tk

#Se debe obtener la clave del proveedor
claveProveedor=

codigoStatus = 10
page = 0
orderList = []

# Inicia la búsqueda de Órdenes con Guía Asignada
while codigoStatus < 201:

      try:
            url = f"https://creditienda-proveedores.concredito.com.mx/creditienda/proveedores/mcreditienda-ordenes/?claveProveedor={claveProveedor}&page={page}&limit=100&fechaInicial={fechaInicio}&fechaFinal={fechaFin}&estatus=guia+asignada"
            print("""
                  Paso 2: """, url, """
                  """)

            payload = {}
            
            headers = {
            'Authorization': cookie,
            'Referer': 'https://creditienda-proveedores.concredito.com.mx/mcreditienda-ordenes'
            }

            response = requests.request("GET", url, headers=headers, data=payload, verify=False, timeout=10)
            print (response.text)

            codigoStatus = (response.status_code)

            data = response.json()

            ordersListTemp = pd.DataFrame(data)

            orderList.append(ordersListTemp)

      except Exception as e:
            print('Páginas de órdenes con guía terminadas')

      print(page)
      page += 1

else:
    print("Fin del bucle")
orderList = pd.concat(orderList, ignore_index=True)
#orderList.to_excel("listaOrders.xlsx") # Genera un excel si se desea revisar
orderList =  orderList[orderList['estatusFactura'] == 'PENDIENTE']
listaFolios =  orderList['folio'].str[2:]
print("""
      Paso 2 Realizado con éxito""")