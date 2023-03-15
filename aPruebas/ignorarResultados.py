import os

contador = 0
for root, dirs, files in os.walk(estadoEjecucion.rutaOrigen, topdown=False):

    for name in files:

        contador += 1

        # Obtenemos la ruta de la imagen
        rutaIMG = os.path.join(root, name)