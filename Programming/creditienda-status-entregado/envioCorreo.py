import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from statusEntregado import entregadoCD, numRowsSinLogs, numRowsCiclo
from datetime import datetime, timedelta

fechaA = (datetime.now() - timedelta(days=0)).strftime("%Y/%m/%d_%H:%M")

#fechaA = (datetime.now() - timedelta(hours=6)).strftime("%Y/%m/%d_%H:%M") # Obtiene la fecha Actual
print(fechaA)

print('''
    Paso Final: Enviando archivo con resultados''')

entregadoCD.to_excel('entregadoCD.xlsx', index=False)

# Rutas de los archivos
CREDENTIALS_FILE = "credentials.json"  # Archivo descargado desde Google Cloud
TOKEN_FILE = "token.json"  # Se generará automáticamente después de la primera autenticación
ATTACHMENT_PATH = "entregadoCD.xlsx"  # Archivo a adjuntar

# Alcances necesarios para Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def authenticate_gmail():
    """Autenticación con OAuth2 para usar Gmail API."""
    creds = None

    # Cargar credenciales almacenadas si existen
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Si no hay credenciales válidas, solicitar autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)  # Abre el navegador para autenticarse

        # Guardar credenciales para usos futuros
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds

def send_email():
    """Envía un correo con un archivo adjunto usando Gmail API."""
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    sender_email = 
    recipient_emails = []
    #recipient_email = "jalvarez@doto.com.mx" 
    subject = f"Proceso Creditienda {fechaA}"
    body_text = f'El proceso de verificación de órdenes en Creditienda ha terminado. Se modificó el Status de {numRowsCiclo} órdenes a "Entregado" y hay {numRowsSinLogs} órdenes que no cuentan con info en Splunk.'

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipient_emails)
    #message["To"] = recipient_email
    message["Subject"] = subject

    # Agregar el cuerpo del mensaje
    message.attach(MIMEText(body_text, "plain"))

    # Adjuntar el archivo
    with open(ATTACHMENT_PATH, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(ATTACHMENT_PATH)}")
    message.attach(part)

    # Convertir el mensaje a base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    send_message = {"raw": raw_message}

    # Enviar el correo
    message = service.users().messages().send(userId="me", body=send_message).execute()
    print(f"Correo enviado con éxito, ID: {message['id']}. Proceso  C O M P L E T A D O")

# Ejecutar la función de envío
send_email()