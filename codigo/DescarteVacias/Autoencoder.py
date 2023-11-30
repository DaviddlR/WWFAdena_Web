# Imports
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
import shutil
import time

import pickle

from codigo.DescarteVacias.modeloAE import getRobustAE_decreaseFilters


# Variables globales
urlModelos = "./Modelos_Entrenados/"
modelos_AE = ["7GR_RAE_cluster0.h5", "7GR_RAE_cluster1.h5", "7GR_RAE_cluster2.h5", "7GR_RAE_cluster3.h5", "7GR_RAE_cluster4.h5", "7GR_RAE_cluster5.h5", "7GR_RAE_cluster6.h5"]
modeloClasificador = "7GR_RandomForest_balanceado_6_4.pickle"
numClusters = 7

# Datos de las imágenes
IMG_WIDTH = 384
IMG_HEIGHT = 256

bloquesAncho = 6
bloquesAlto = 4


###### Medidas de error ######
def calcularErrores(original, reconstruccion, ancho, alto, bloquesAncho, bloquesAlto):

    listaErrores = []

    # Paso 1: Dividir la imagen en bloques
    M = int(ancho / bloquesAncho)
    N = int(alto / bloquesAlto)

    tilesOriginal = [original[x:x+M,y:y+N] for x in range(0,original.shape[0], M) for y in range(0,original.shape[1], N)]
    tilesReconstruccion = [reconstruccion[x:x+M,y:y+N] for x in range(0,reconstruccion.shape[0],M) for y in range(0,reconstruccion.shape[1],N)]

    # Paso 2: Para cada bloque, calcular errores
    for i, bloqueOriginal in enumerate(tilesOriginal):
        bloqueReconstruccion = tilesReconstruccion[i]

        valorMse = calcularMSE(bloqueOriginal, bloqueReconstruccion)
        valorMae = calcularMAE(bloqueOriginal, bloqueReconstruccion)
        valorSsim = calcularSSIM(bloqueOriginal, bloqueReconstruccion)

        listaErrores.append(valorMse)
        listaErrores.append(valorMae)
        listaErrores.append(valorSsim)

    # Paso 3: Devolver la lista con todos los errores de cada bloque [E11, E12, E13, E21, E22, E23...]
    return listaErrores


mse = tf.keras.losses.MeanSquaredError()
mae = tf.keras.losses.MeanAbsoluteError()

def calcularMSE(original, reconstruccion):
    return mse(original, reconstruccion).numpy()

def calcularMAE(original, reconstruccion):
    return mae(original, reconstruccion).numpy()

def calcularSSIM(original, reconstruccion):
    return ssim(original, reconstruccion, channel_axis=2, data_range=1)




###### Función principal ######
def autoencoders(estadoEjecucion, carpetaTemporal):

    # Mensaje GUI
    estadoEjecucion.mensajeClasificacion = "Analizando si se puede utilizar GPU"

    # Obtenemos la carpeta temporal donde están las imágenes
    carpetaTemporal = carpetaTemporal.name

    # Comprobamos si se puede usar GPU
    cpu = checkGPU()

    # El código es idéntico si usa GPU o CPU. Solo cambia el dispositivo a utilizar
    if cpu:
        # Usa CPU
        estadoEjecucion.usaGPU = "CPU"
        with tf.device('/CPU:0'):
            aplicarClasificacion(estadoEjecucion, carpetaTemporal)
    else:
        # Usa GPU
        estadoEjecucion.usaGPU = "GPU"
        aplicarClasificacion(estadoEjecucion, carpetaTemporal)

    time.sleep(5)




def aplicarClasificacion(estadoEjecucion, carpetaTemporal):

    mover = estadoEjecucion.moverIMG


    # Cargar clasificador (Random Forest)
    clasificador = pickle.load(open(os.path.relpath(urlModelos + modeloClasificador), 'rb'))
    #clasificador = tf.keras.models.load_model(urlModelos + modeloClasificador)

    # Para cada cluster -> AEFinalTest.py
    # https://stackoverflow.com/questions/41715025/keras-flowfromdirectory-get-file-names-as-they-are-being-generated 
    contador = 0

    for cluster in range(numClusters):

        print("INICIO CLUSTER ", cluster)

        # Cargamos imágenes
        carpetaImagenes = os.path.join(carpetaTemporal, str(cluster))
        

        dataset = ImageDataGenerator(rescale=1./255, data_format='channels_last')

        carpeta = dataset.flow_from_directory(
            carpetaImagenes,
            target_size = (IMG_HEIGHT, IMG_WIDTH),
            batch_size=1,
            class_mode=None,
            shuffle=False,
            seed=42
        )

        

        estadoEjecucion.mensajeClasificacion = "Analizando grupo " + str(cluster + 1) + "/7 - " + estadoEjecucion.usaGPU
        

        # Si hay imágenes asignadas a ese cluster...
        if carpeta.n > 0:

            # Hay imágenes -> cargamos Autoencoder
            autoencoder = getRobustAE_decreaseFilters((IMG_HEIGHT, IMG_WIDTH, 3))
            autoencoder.load_weights(os.path.relpath(urlModelos + modelos_AE[cluster]))
            # NOTA --> No hace falta cargar correntropy para inferencia

            # autoencoder = tf.keras.models.load_model(urlModelos + modelos_AE[cluster], custom_objects={"correntropy" : correntropy})
            
            # Nombres de archivos
            filepath_carpeta = carpeta.filenames
            print(filepath_carpeta)
            filepath = list()

            for file in filepath_carpeta:
                file = file.split(os.sep)
                file = file[1]
                filepath.append(file)

            i = 0
            # Predicciones hasta que no haya más imagenes
            while i < carpeta.n:

                # Aplicamos Autoencoders
                original = carpeta.next()
                rutaIMG = os.path.join(estadoEjecucion.rutaOrigen, filepath[i])

                prediccion = autoencoder.predict(original)

                # https://stackoverflow.com/questions/41715025/keras-flowfromdirectory-get-file-names-as-they-are-being-generated 

                # Hallamos errores. -----------------------------

                errores = calcularErrores(original[0], prediccion[0], IMG_WIDTH, IMG_HEIGHT, bloquesAncho, bloquesAlto)
                errores.append(cluster)

                # Aplicar clasificador
                resultadosImagen = [errores]
                prediccionClasificador = clasificador.predict_proba(resultadosImagen)
                prediccionClasificador = prediccionClasificador[0]  # [Probabilidad_Vacio, Probabilidad_Animales] --> JUSTO AL REVES QUE MLP
                



                # Check si dudosas
                if estadoEjecucion.dudosas:
                    umbral = estadoEjecucion.umbralDudosas
                    if prediccionClasificador[1] > umbral:
                        # Mover a carpeta vacio
                        moverImagen(rutaIMG, estadoEjecucion.rutaAnimales, mover)
                        
                    elif prediccionClasificador[0] > umbral:
                        # Mover a carpeta animales
                        moverImagen(rutaIMG, estadoEjecucion.rutaVacio, mover)

                    else:
                        # Mover a carpeta dudosas
                        moverImagen(rutaIMG, estadoEjecucion.rutaDudosas, mover)

                else:
                    if prediccionClasificador[0] < prediccionClasificador[1]:  # [0,1] Animales
                        # Mover a carpeta vacio
                        moverImagen(rutaIMG, estadoEjecucion.rutaAnimales, mover)
                    else:                                                      # [1,0] Vacio
                        # Mover a carpeta animales
                        moverImagen(rutaIMG, estadoEjecucion.rutaVacio, mover)


                i += 1
                contador += 1
                estadoEjecucion.actualizarBarraClasificacion(contador)

        print("FIN CLUSTER ", cluster)
        del dataset


    estadoEjecucion.mensajeClasificacion = "¡Hecho!"
    
        






# UTILS
#         
def moverImagen(origen, destino, mover):
    if mover:
        shutil.move(origen, destino)
    else:
        shutil.copy2(origen, destino)

def checkGPU():
    cpu = False

    # Comprobamos si hay GPU en el dispositivo
    if tf.test.is_gpu_available(cuda_only=True):

        # Intentamos cargar un autoencoder
        try:
            model = getRobustAE_decreaseFilters((IMG_HEIGHT, IMG_WIDTH, 3))
            autoencoder = model.load_weights(os.path.relpath(urlModelos + modelos_AE[0]))

        except Exception as e:
            if e.__class__.__name__ == "ResourceExhaustedError":
                cpu = True

    else:
        cpu = True

    return cpu


