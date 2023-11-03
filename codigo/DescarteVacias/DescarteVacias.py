# Imports
import os
import time
import datetime
import tensorflow as tf
import tensorflow.keras.backend as K
import tempfile

# Código
from codigo.DescarteVacias.Clustering import *
from codigo.DescarteVacias.Autoencoder import *


def comenzarDescarteVacias(estadoEjecucion):
    start_time = time.time()

    print("Descartando vacias...")

    # Inicializamos datos
    estadoEjecucion.estado = "INICIADA"
    estadoEjecucion.mensajeClustering = "Comenzando la ejecución"
    estadoEjecucion.mensajeClasificacion = "Esperando agrupamiento"

    carpetaTemporal = tempfile.TemporaryDirectory()

    try:
        print('Carpeta temporal ', carpetaTemporal)

        # Preprocesamiento + clustering
        clustering(estadoEjecucion, carpetaTemporal)

        # Autoencoders + clasificación
        autoencoders(estadoEjecucion, carpetaTemporal)    

        # Finalizamos la ejecución   

        end_time = time.time()

        sec = round(end_time - start_time)
        tiempo = str(datetime.timedelta(seconds=sec))
        estadoEjecucion.generarTXT(tiempo)
        
        estadoEjecucion.estado = "FINALIZADO"

    # Halla o no excepciones, borramos la carpeta temporal cuando acaba la ejecución
    finally:
        print("---------------- BORRAMOS CARPETA TEMPORAL ----------------")
        carpetaTemporal.cleanup()