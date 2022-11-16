# Imports básicos
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
import tensorflow as tf
import tensorflow.keras.backend as K

import numpy as np

# WLS - En window 11 viene por defecto.

# Hilos
import threading
import time

# Código
from codigo.EstadoEjecucion import *
from codigo.DescarteVacias.Correntropy import *

# Variables globales

separadorPickerDirectory = "/"
sp = ""

urlBase = str(os.path.expanduser("~"))

# TODO: URL destino será carpeta temporal (check TODO list)
if "\\" in urlBase:
    print("Windows")
    urlDestino = urlBase + "\\Airesultados"
    sp = "\\"
else:
    print("Linux")
    urlDestino = urlBase + "/Airesultados"
    sp = "/"

urlModelos = "./Modelos_Entrenados/"
modeloKmeans = "kmeansServidor.pkl"
modelos_AE = ["AE_cluster0.h5", "AE_cluster1.h5", "AE_cluster2.h5", "AE_cluster3.h5", "AE_cluster4.h5", "AE_cluster5.h5", "AE_cluster6.h5"]
modeloClasificadora = "MLP_2_20_150_Cluster.h5"


# Parámetros de configuración recogidos del formulario y estado de la ejecución
# TODO: ¿Crear una clase para cada tipo de ejecución? (descarte, segmentación...)? O usar herencia??
estadoEjecucion = EstadoEjecucion()



# Creación de la APP
app = Flask(__name__)


# Página principal (acceder a URL)
@app.route("/")
def pantallaPrincipal():
    return render_template("principal.html")


# Página que se muestra durante el procesamiento.
# Recibe los datos del formulario
@app.route('/procesando', methods=["POST", "GET"])
def procesando():

    # Recopilamos datos del formulario y lo almacenamos en EstadoEjecucion
    if request.method == "POST":

        datosFormulario = request.form

        # Datos completos del formulario
        estadoEjecucion.formularioCompleto = datosFormulario

        # Carpeta de imágenes
        ocultoDirectorio = request.form["Oculto"]
        directorio = ocultoDirectorio.split(separadorPickerDirectory)[0]
        estadoEjecucion.rutaOrigen = urlBase + sp + directorio

        # Carpeta donde se almacenarán los resultados
        estadoEjecucion.rutaDestino = urlDestino

        # Check si almacenar dudosas
        if "dudosas" in estadoEjecucion.formularioCompleto:
            estadoEjecucion.dudosas = True
        else:
            estadoEjecucion.dudosas = False

        print("Resumen del form")
        print(datosFormulario)
        print("Ruta origen: ", urlBase + "\\" + directorio)
        print("Ruta destino: ", urlDestino)

        

        

        # Si el directorio no está creado, lo creamos
        # if not os.path.exists(urlDestino):
        #     os.mkdir(urlDestino)
        
        
        # if "dudosas" in form_data:
        #     print("Dudosas")
        # else:
        #     print("No dudosas")

    print(urlBase)
    

    return render_template('procesando.html')

# Función para comenzar la ejecución. Inicia nuevo hilo.
@app.route("/comenzarTarea", methods=["POST"])
def empezarTareaLarga():
    print("Comienza tarea larga")
    hilo = threading.Thread(target=lambda: tareaLarga())
    hilo.start()

    # Inicializamos datos
    estadoEjecucion.estado = "INICIADA"

    #return jsonify({}), 202, {'url':'/estadoTarea'}
    return {"url":"/estadoTarea"}

# Función para comprobar el estado de la tarea y actualizar mensajes.
@app.route("/estadoTarea")
def getEstadoTarea():

    # Obtiene el estado de la tarea
    mensaje = estadoEjecucion.mensaje
    estado = estadoEjecucion.estado
    progreso = estadoEjecucion.progreso

    respuesta = {'estado':estado, "mensaje":mensaje, "progreso":progreso}

    # Devuelve toda la info
    return jsonify(respuesta)


# PROCESO EN SEGUNDO PLANO
def tareaLarga():

    modelos = []
    for i in range(1):
        estadoEjecucion.mensaje = "Cargando modelo " + str(i)
        model = tf.keras.models.load_model(urlModelos + modelos_AE[i], custom_objects={"correntropy" : correntropy})
        modelos.append(model)
    
    

    print("Durmiendo...")
    estadoEjecucion.mensaje = "Durmiendo..."
    time.sleep(40)

    for modeloAE in modelos:
        print(modeloAE.summary())

    estadoEjecucion.estado = "FINALIZADO"
    print("Ejecutando cosas")
    estadoEjecucion.mensaje = "Ejecutando cosas"
    time.sleep(5)
    print("ya casi esta...")
    estadoEjecucion.mensaje = "Ya casi esta..."
    time.sleep(5)
    print("Hecho")
    estadoEjecucion.mensaje = "Hecho :D"
    estadoEjecucion.estado = "FINALIZADO"

# MAIN
if __name__ == '__main__':

    # Inicio de la APP
    app.run(debug=True)  # Se puede especificar el puerto