# Imports
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

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

    carpetaTemporal = carpetaTemporal.name

    # Comprobamos si se puede usar GPU
    cpu = checkGPU()

    # El código es idéntico si usa GPU o CPU. Solo cambia el dispositivo a utilizar
    if cpu:
        # Usa CPU
        print("USA CPU")
        with tf.device('/CPU:0'):
            aplicarClasificacion(carpetaTemporal)
    else:
        # Usa GPU
        print("USA GPU")
        aplicarClasificacion(carpetaTemporal)




def aplicarClasificacion(carpetaTemporal):

    # Cargar clasificador
    clasificador = tf.keras.models.load_model(urlModelos + modeloClasificador)

    # Para cada cluster -> AEFinalTest.py
    # https://stackoverflow.com/questions/41715025/keras-flowfromdirectory-get-file-names-as-they-are-being-generated 
    for cluster in range(numClusters):
        print("INICIO CLUSTER ", cluster)

        # Cargamos imágenes
        carpetaImagenes = os.path.join(carpetaTemporal, str(cluster))
        print(carpetaImagenes)

        dataset = ImageDataGenerator(rescale=1./255, data_format='channels_last')

        carpeta = dataset.flow_from_directory(
            carpetaImagenes,
            target_size = (IMG_HEIGHT, IMG_WIDTH),
            batch_size=1,
            class_mode=None,
            shuffle=False,
            seed=42
        )

        contador = 0

        # Si hay imágenes asignadas a ese cluster...
        if carpeta.n > 0:

            # Hay imágenes -> cargamos Autoencoder
            autoencoder = tf.keras.models.load_model(urlModelos + modelos_AE[cluster], custom_objects={"correntropy" : correntropy})
            
            # Nombres de archivos
            filepath_carpeta = carpeta.filenames
            filepath = list()
            for file in filepath_carpeta:
                file = file.split("\\")[1]
                filepath.append(file)

            # Predicciones hasta que no haya más imagenes
            while contador < carpeta.n:

                # Aplicamos Autoencoders
                original = carpeta.next()
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
                print(filepath[contador])
                print(prediccionClasificador)

                #TODO: Check si dudosas

                #TODO: Mover imagen original a carpeta correspondiente


                contador += 1

        print("FIN CLUSTER ", cluster)


        
        
    

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


