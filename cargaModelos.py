
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


for i in range(1):
    print("Carga modelo ",i)
    model = tf.keras.models.load_model(urlModelos + modelos_AE[i], custom_objects={"correntropy" : correntropy})
    print("Fin carga modelo")