# Imports
import os
import time

import pickle
import cv2 as cv

# Variables globales
rutaModeloKmeans = "./Modelos_Entrenados/KmeansImagenesNorm7_ESTE.pkl"

rutaModeloKmeans = os.path.relpath(rutaModeloKmeans)

# Recortado de imagenes para preprocesamiento
x0 = 0
y0 = 0
alto = 256
ancho = 384

numeroDeCanales = 3  # RGB


def ecualizarHistograma(img):
    img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)

    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv.equalizeHist(img_yuv[:,:,0])

    # convert the YUV image back to RGB format
    img = cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)

    return img


def clustering(estadoEjecucion, carpetaTemporal):
    
    estadoEjecucion.mensajeClustering = "Agrupando imágenes"

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

    cluster0 = os.path.join(cluster0, "imgs")
    cluster1 = os.path.join(cluster1, "imgs")
    cluster2 = os.path.join(cluster2, "imgs")
    cluster3 = os.path.join(cluster3, "imgs")
    cluster4 = os.path.join(cluster4, "imgs")
    cluster5 = os.path.join(cluster5, "imgs")
    cluster6 = os.path.join(cluster6, "imgs")

    os.mkdir(cluster0)
    os.mkdir(cluster1)
    os.mkdir(cluster2)
    os.mkdir(cluster3)
    os.mkdir(cluster4)
    os.mkdir(cluster5)
    os.mkdir(cluster6)

    # Cargar modelo Kmeans
    kmeansModel = pickle.load(open(rutaModeloKmeans, "rb"))
    centroids = kmeansModel.cluster_centers_
    print(centroids.shape)
    print(centroids)

    

    # Procesamos cada imagen y la asignamos a un cluster
    contador = 0
    for root, dirs, files in os.walk(estadoEjecucion.rutaOrigen, topdown=False):

        for name in files:

            # Obtenemos la ruta de la imagen
            rutaIMG = os.path.join(root, name)

            # Evitamos las imágenes que se han procesado en otras ejecuciones
            if not "00_Resultados_" in rutaIMG:
                contador += 1

                # Cargamos la imagen
                img = cv.imread(rutaIMG)

                # Preprocesamiento: Reducir tamaño, normalizar y adecuar para clustering
                resizedImg = rescaleFrame(img, ancho, alto)

                resizedImgNorm = cv.normalize(resizedImg, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
                resizedImgNorm = resizedImgNorm.reshape(ancho * alto * numeroDeCanales)
                resizedImgNorm = resizedImgNorm.reshape(1,-1)

                # Aplicar clustering
                indiceCluster = kmeansModel.predict(resizedImgNorm)[0]
                #print("Indice cluster: ", indiceCluster)

                # Una vez tenemos el indice del cluster, copiar la imagen
                rutaClusterImagen = os.path.join(carpetaTemporal, str(indiceCluster),"imgs",name)

                # Ecualizamos la imagen para luego los AE
                imagenEcualizada = ecualizarHistograma(resizedImg)
                cv.imwrite(rutaClusterImagen, imagenEcualizada)

                # Actualizamos la barra de clustering
                estadoEjecucion.actualizarBarraClustering(contador)


    estadoEjecucion.mensajeClustering = "¡Hecho!"


# Escalar una imagen a una anchura y altura dada
def rescaleFrame(frame, width, height):
    height_ = height  # Altura
    width_ = width  # Anchura

    finalDimensions = (width_, height_)

    return cv.resize(frame, finalDimensions, interpolation=cv.INTER_AREA)