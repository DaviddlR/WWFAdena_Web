# Imports
import os
import time

import pickle
import cv2 as cv

# Variables globales
rutaModeloKmeans = "./Modelos_Entrenados/kmeansServidor.pkl"

# Tamaño del histograma (puede ser reducido)
#h_bins = 60
r_bins = 85
g_bins = 85
b_bins = 85
hist_size = [r_bins, g_bins, b_bins]  # Tamaño que tendrá el histograma (podríamos reducirlos / ampliarlos hasta 180, 256)

# Rango de valores de cada canal que encontramos en la imagen
#h_ranges = [0,180]
r_ranges = [0,256]
g_ranges = [0, 256]
b_ranges = [0, 256]
ranges = r_ranges + g_ranges + b_ranges

# 3 canales (HSV o BGR)
channels = [0,1,2]

# Recortado de imagenes
x0 = 0
y0 = 0
x1 = 256
y1 = 388


def clustering(estadoEjecucion, carpetaTemporal):


    # Crear 7 carpetas dentro de carpeta temporal, una por cluster
    sp = estadoEjecucion.sp
    carpetaTemporal = carpetaTemporal.name

    cluster0 = os.path.join(carpetaTemporal, "0")
    cluster1 = os.path.join(carpetaTemporal, "1")
    cluster2 = os.path.join(carpetaTemporal, "2")
    cluster3 = os.path.join(carpetaTemporal, "3")
    cluster4 = os.path.join(carpetaTemporal, "4")
    cluster5 = os.path.join(carpetaTemporal, "5")
    cluster6 = os.path.join(carpetaTemporal, "6")

    os.mkdir(cluster0)
    os.mkdir(cluster1)
    os.mkdir(cluster2)
    os.mkdir(cluster3)
    os.mkdir(cluster4)
    os.mkdir(cluster5)
    os.mkdir(cluster6)

    # Cargar modelo Kmeans (kmeansPRUEBA.ipynb)
    kmeansModel = pickle.load(open(rutaModeloKmeans, "rb"))
    centroids = kmeansModel.cluster_centers_
    print(centroids.shape)
    print(centroids)


    #TODO: Procesamos cada imagen y la asignamos a un cluster
    contador = 0
    for root, dirs, files in os.walk(estadoEjecucion.rutaOrigen, topdown=False):
        for name in files:
            
            contador += 1

            # Obtenemos la ruta de la imagen
            rutaIMG = os.path.join(root, name)
            img = cv.imread(rutaIMG)

            # Preprocesamiento: Reducir tamaño
            resizedImg = rescaleFrame(img, 384, 288)

            # Modificamos espacio de color
            #resizedImg = cv.cvtColor(resizedImg, cv.COLOR_BGR2RGB)

            # Calcular histograma y normalizar
            histograma_test = cv.calcHist([img], channels, None, hist_size, ranges, accumulate = False)
            cv.normalize(histograma_test, histograma_test, alpha = 0, beta = 1, norm_type = cv.NORM_MINMAX)

            histograma_test = histograma_test.reshape(r_bins*g_bins*b_bins)
            histograma_test = histograma_test.reshape(1,-1)

            # Aplicar clustering
            indiceCluster = kmeansModel.predict(histograma_test)[0]
            print("Indice cluster: ", indiceCluster)

            # Segundo preprocesamiento (cortar barra inferior)
            crop = resizedImg[x0:x1, y0:y1]

            # Una vez tenemos el indice del cluster, copiar la imagen
            rutaClusterImagen = os.path.join(carpetaTemporal, str(indiceCluster),name)
            cv.imwrite(rutaClusterImagen + name, crop)


    

    time.sleep(120)




# Escalar una imagen a una anchura y altura dada
def rescaleFrame(frame, width, height):
    height_ = height  # Altura
    width_ = width  # Anchura

    finalDimensions = (width_, height_)

    return cv.resize(frame, finalDimensions, interpolation=cv.INTER_AREA)