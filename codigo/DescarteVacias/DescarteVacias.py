# Imports
import os
import time
import tensorflow as tf
import tensorflow.keras.backend as K

# TODO: Aquí creo que debería ir la creación de directorios temporales
# TODO: Esta función comienza y acaba la ejecución. Modificar estado
def comenzarDescarteVacias(estadoEjecucion):
    print("Descartando vacias...")

    # Inicializamos datos
    estadoEjecucion.estado = "INICIADA"
    estadoEjecucion.mensaje = "Comenzando la ejecución"

    # Preprocesamiento

    # Clustering

    # Autoencoders + clasificación
    

    # Finalizamos la ejecución
    estadoEjecucion.estado = "FINALIZADO"
    