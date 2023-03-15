
import tensorflow as tf
import tensorflow.keras.backend as K
import numpy as np

# Correntropy
tf_2pi = tf.constant(tf.sqrt(2*np.pi), dtype=tf.float32)

def robust_kernel(alpha, sigma = 0.2):
    return 1 / (tf_2pi * sigma) * K.exp(-1 * K.square(alpha) / (2 * sigma * sigma))

def correntropy(y_true, y_pred):
    return -1 * K.sum(robust_kernel(y_pred - y_true))



urlModelos = "./Modelos_Entrenados/"
modeloKmeans = "kmeansServidor.pkl"
modelos_AE = ["AE_cluster0.h5", "AE_cluster1.h5", "AE_cluster2.h5", "AE_cluster3.h5", "AE_cluster4.h5", "AE_cluster5.h5", "AE_cluster6.h5"]


#OPCION 1 -> Manejo de excepciones.
try:
    for i in range(1):
        print("Carga modelo ",i)
        model = tf.keras.models.load_model(urlModelos + modelos_AE[i], custom_objects={"correntropy" : correntropy})
        print("Fin carga modelo")
except Exception as e:
    if e.__class__.__name__ == "ResourceExhaustedError":
        print("No se puede con GPU")
        with tf.device('/CPU:0'):
            for i in range(1):
                print("Carga modelo ",i)
                model = tf.keras.models.load_model(urlModelos + modelos_AE[i], custom_objects={"correntropy" : correntropy})
                print("Fin carga modelo")

# Fase 1 -> Cargar un modelo y ver si se puede usar GPU
cpu = False
if tf.test.is_gpu_available(cuda_only=True):
    
    try:
        model = tf.keras.models.load_model(urlModelos + modelos_AE[i], custom_objects={"correntropy" : correntropy})
        #TODO: Cargar imagen y usarlo.


    except Exception as e:
        if e.__class__.__name__ == "ResourceExhaustedError":
            cpu = False

else:
    cpu = True

if cpu:
    # Usa CPU
    with tf.device('/CPU:0'):
        model = tf.keras.models.load_model(urlModelos + modelos_AE[0], custom_objects={"correntropy" : correntropy})
        print(model.summary())
else:
    # Usa GPU
    model = tf.keras.models.load_model(urlModelos + modelos_AE[0], custom_objects={"correntropy" : correntropy})
    print(model.summary())


# OPCION 2 -> Comprobar si hay espacio antes de hacer nada.
# Import os to set the environment variable CUDA_VISIBLE_DEVICES
# from tensorflow.python.client import device_lib
# a = device_lib.list_local_devices()
# print(a)
# print(type(a))
# print("###########################")
# print(type(a[0]))