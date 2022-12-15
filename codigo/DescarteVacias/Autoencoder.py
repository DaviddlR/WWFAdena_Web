# Imports
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
import shutil
import time

# Código
from codigo.DescarteVacias.Correntropy import correntropy
#from skimage.metrics import structural_similarity as ssim

# Variables globales
urlModelos = "./Modelos_Entrenados/"
modelos_AE = ["AE_cluster0.h5", "AE_cluster1.h5", "AE_cluster2.h5", "AE_cluster3.h5", "AE_cluster4.h5", "AE_cluster5.h5", "AE_cluster6.h5"]
modeloClasificador = "MLP_2_20_150_Cluster.h5"
numClusters = 7

IMG_WIDTH = 384
IMG_HEIGHT = 256

# Medidas de error
def calcularMSE(original, reconstruccion):
	err = np.sum((original.astype("float") - reconstruccion.astype("float")) ** 2)
	err /= float(original.shape[0] * original.shape[1])
	
	return err

def calcularMAE(original, reconstruccion):
    return np.mean(np.abs(original.astype("float") - reconstruccion.astype("float")))

def calcularSSIM(original, reconstruccion):
    return ssim(original, reconstruccion, channel_axis=2)




def autoencoders(estadoEjecucion, carpetaTemporal):

    estadoEjecucion.mensajeClasificacion = "Analizando si se puede utilizar GPU"

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

    # Cargar clasificador
    clasificador = tf.keras.models.load_model(urlModelos + modeloClasificador)

    # Para cada cluster -> AEFinalTest.py
    # https://stackoverflow.com/questions/41715025/keras-flowfromdirectory-get-file-names-as-they-are-being-generated 
    contador = 0

    for cluster in range(numClusters):

        if estadoEjecucion.interrumpirEjecucion:
            break

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
            autoencoder = tf.keras.models.load_model(urlModelos + modelos_AE[cluster], custom_objects={"correntropy" : correntropy})
            
            # Nombres de archivos
            filepath_carpeta = carpeta.filenames
            print(filepath_carpeta)
            filepath = list()
            for file in filepath_carpeta:
                #print(file)
                file = file.split("\\")
                #print(file)
                file = file[1]
                #print(file)
                filepath.append(file)

            i = 0
            # Predicciones hasta que no haya más imagenes
            while i < carpeta.n and not estadoEjecucion.interrumpirEjecucion:

                # Aplicamos Autoencoders
                original = carpeta.next()
                rutaIMG = os.path.join(estadoEjecucion.rutaOrigen, filepath[i])
                # print(estadoEjecucion.rutaOrigen)
                # print(filepath[i])
                # print(rutaIMG)

                prediccion = autoencoder.predict(original)

                # https://stackoverflow.com/questions/41715025/keras-flowfromdirectory-get-file-names-as-they-are-being-generated 

                # Hallamos errores.
                msi = calcularMSE(original[0], prediccion[0])
                mae = calcularMAE(original[0], prediccion[0])
                valor_ssim = calcularSSIM(original[0], prediccion[0])

                # Guardamos resultados
                resultadosImagen = [msi, mae, valor_ssim, cluster]
                resultadosImagen = [resultadosImagen]

                # Aplicar clasificador
                prediccionClasificador = clasificador.predict(resultadosImagen)
                prediccionClasificador = prediccionClasificador[0]
                

                # Check si dudosas
                if estadoEjecucion.dudosas:
                    umbral = estadoEjecucion.umbralDudosas
                    if prediccionClasificador[1] > umbral:
                        # Mover a carpeta vacio
                        shutil.move(rutaIMG, estadoEjecucion.rutaVacio)
                        
                    elif prediccionClasificador[0] > umbral:
                        # Mover a carpeta animales
                        shutil.move(rutaIMG, estadoEjecucion.rutaAnimales)
                    else:
                        # Mover a carpeta dudosas
                        shutil.move(rutaIMG, estadoEjecucion.rutaDudosas)
                else:
                    if prediccionClasificador[0] < prediccionClasificador[1]:  # [0,1] Vacio
                        # Mover a carpeta vacio
                        shutil.move(rutaIMG, estadoEjecucion.rutaVacio)
                    else:                                          # [1,0] Animales
                        # Mover a carpeta animales
                        shutil.move(rutaIMG, estadoEjecucion.rutaAnimales)

                #TODO: Mover imagen original a carpeta correspondiente


                i += 1
                contador += 1
                estadoEjecucion.actualizarBarraClasificacion(contador)

        print("FIN CLUSTER ", cluster)


    estadoEjecucion.mensajeClasificacion = "¡Hecho!"
        
        
    

def checkGPU():
    cpu = False

    if tf.test.is_gpu_available(cuda_only=True):

        try:
            model = tf.keras.models.load_model(urlModelos + modelos_AE[0], custom_objects={"correntropy" : correntropy})
            #TODO: Cargar imagen y usarlo.

        except Exception as e:
            if e.__class__.__name__ == "ResourceExhaustedError":
                cpu = True

    else:
        cpu = True

    return cpu


