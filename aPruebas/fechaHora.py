from datetime import datetime

now = datetime.now()
fechaActual = now.strftime("%d-%m-%Y__%H-%M-%S")

fechaSeparado = fechaActual.split("__")
print(fechaSeparado[0])
print(fechaSeparado[1].replace("-",":"))