# Imports
import os
import time
import tensorflow as tf
import tensorflow.keras.backend as K
import tempfile

# Código
from codigo.DescarteVacias.Clustering import *
from codigo.DescarteVacias.Autoencoder import *

# TODO: Aquí creo que debería ir la creación de directorios temporales
# TODO: Esta función comienza y acaba la ejecución. Modificar estado
def comenzarDescarteVacias(estadoEjecucion):
    print("Descartando vacias...")

    # Inicializamos datos
    estadoEjecucion.ejecucionEnCurso = True
    estadoEjecucion.estado = "INICIADA"
    estadoEjecucion.mensajeClustering = "Comenzando la ejecución"
    estadoEjecucion.mensajeClasificacion = "Esperando agrupamiento"

    carpetaTemporal = tempfile.TemporaryDirectory()
    print('Carpeta temporal ', carpetaTemporal)

    # Preprocesamiento + clustering
    clustering(estadoEjecucion, carpetaTemporal)

    # Autoencoders + clasificación
    autoencoders(estadoEjecucion, carpetaTemporal)

    # TODO: Estado ejecución -> generarTXT
    

    # Finalizamos la ejecución

    estadoEjecucion.ejecucionEnCurso = False
    estadoEjecucion.estado = "FINALIZADO"