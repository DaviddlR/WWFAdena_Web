# Imports
import os
import time


def clustering(estadoEjecucion, carpetaTemporal):

    #TODO: Crear 7 carpetas dentro de carpeta temporal, una por cluster
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

    #TODO: Cargar modelo Kmeans (kmeansPRUEBA.ipynb)



    #TODO: Cargar imagen y preprocesar (reducir tamaño)


    #TODO: Calcular histograma y preprocesarlo según el mismo archivo


    #TODO: Aplicar clustering


    #TODO: Segundo preprocesamiento (cortar barra inferior)


    #TODO: Una vez tenemos el indice del cluster, copiar la imagen