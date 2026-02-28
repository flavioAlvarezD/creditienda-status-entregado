Hola! °/

Antes que nada en config se debe seleccionar el rango de fechas del cual se quieren obter las órdenes, después ya se ejecuta todo (config.py)
El primer paso es obtener la cookie(obtenerCookie.py)
El siguiente es darle permisos a la cookie (permisos.py)
Luego se obtiene el listado de órdenes, esto se debe hacer en un ciclo para obtenerlas todas (obtenerListado.py)
Se extrae la información de cada orden desde creditienda (cicloCreditienda.py)
Después se extrae la info desde Vtex (infoVtex.py)
Hace una segunda revisión en Splunk para rescatar órdenes que ya se hayan entregado pero aún no se actualizan en creditienda o vtex (cicloSplunk.py)
Después forza el cambio de status de la orden en creditienda (statusEntregado,py)
Finalmente envía un correo para Informar de los cambios

Se puede ejecutar cualquiera de estos archivos y automáticamente ejecutará los archivos anteriores. Esto es útil por si no se tiene splunk, no se quiere modificar algo en creditienda, o mandar un correo
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

