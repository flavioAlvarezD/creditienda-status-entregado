import requests
import json

url = "https://creditienda-proveedores.concredito.com.mx/api/login"

payload = json.dumps({
  "username": "User",
  "password": "Password"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False, timeout=10)
#print(response.text)

data = response.json()
cookie = data['body']['token']
print("la cookie es:", cookie)
print("""
      Paso 1 Realizado con éxito""")
