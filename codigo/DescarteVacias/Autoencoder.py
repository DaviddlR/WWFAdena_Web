# Imports
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Código
from DescarteVacias.Correntropy import correntropy
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

# def calcularSSIM(original, reconstruccion):
#     print(original.shape)
#     return ssim(original, reconstruccion, channel_axis=2)




def autoencoders(estadoEjecucion, carpetaTemporal):
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

        # Cargar modelo AE.
        autoencoder = tf.keras.models.load_model(urlModelos + modelos_AE[cluster], custom_objects={"correntropy" : correntropy})

        #TODO: Cargar imágenes de la carpeta
        dataset = ImageDataGenerator(rescale=1./255, data_format='channels_last')

        carpeta = dataset.flow_from_directory(
            carpetaTemporal + str(cluster),  #TODO: Creo que esto está mal
            target_size = (IMG_HEIGHT, IMG_WIDTH),
            batch_size=1,
            class_mode=None,
            shuffle=False,
            seed=42
        )

        contador = 0
        while contador < carpeta.n:

            # Aplicamos Autoencoders
            original = carpeta.next()
            prediccion = autoencoder.predict(original)

            contador += 1

            #TODO: Calcular errores

            #TODO: Aplicar clasificador

            #TODO: Check si dudosas

            #TODO: Mover imagen original a carpeta correspondiente
    

def checkGPU():
    cpu = False
    if tf.test.is_gpu_available(cuda_only=True):
        
        try:
            model = tf.keras.models.load_model(urlModelos + modelos_AE[0], custom_objects={"correntropy" : correntropy})
            #TODO: Cargar imagen y usarlo.

        except Exception as e:
            if e.__class__.__name__ == "ResourceExhaustedError":
                cpu = False

    else:
        cpu = True

    return cpu


