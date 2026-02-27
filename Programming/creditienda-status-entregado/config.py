from datetime import datetime, timedelta

# Genera las fechas para la búsqueda
# Fecha del día de hoy
fechaA = datetime.now().strftime("%Y-%m-%d")

# Fecha de hace 7 días
fechaB = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
# Fecha de inicio de mes
#fechaB = datetime.now().strftime("%Y-%m") + "-01"

#print(fechaA)
#print(fechaB)
fechaInicio = fechaB
fechaFin = fechaA
