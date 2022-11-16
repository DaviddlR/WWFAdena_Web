# Imports básicos
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
import tensorflow as tf
import keras
import keras.backend as K
import numpy as np

# WLS - En window 11 viene por defecto.

# Hilos
import threading
import time

# Código
from codigo.EstadoEjecucion import *

# Variables globales

# Separador. Windows = \\ Linux = /
# TODO: Creo que no hace falta para rutas dentro del proyecto
sp = ""
separadorPickerDirectory = "/"

urlBase = str(os.path.expanduser("~"))
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


## Funciones auxiliares
# Correntropy
tf_2pi = tf.constant(tf.sqrt(2*np.pi), dtype=tf.float32)

def robust_kernel(alpha, sigma = 0.2):
    return 1 / (tf_2pi * sigma) * K.exp(-1 * K.square(alpha) / (2 * sigma * sigma))

def correntropy(y_true, y_pred):
    return -1 * K.sum(robust_kernel(y_pred - y_true))


# Creación de la APP
app = Flask(__name__)
estadoEjecucion = EstadoEjecucion()

# Página principal (acceder a URL)
@app.route("/")
def pantallaPrincipal():
    return render_template("principal.html")


# Página que se muestra durante el procesamiento.
# Recibe los datos del formulario
@app.route('/procesando', methods=["POST", "GET"])
def procesando():
    if request.method == "POST":
        form_data = request.form
        ocultoDirectorio = form_data["Oculto"]
        print(ocultoDirectorio)

        # TODO: Las separaciones en linux =! Windows. Detectar el SO y actuar en consecuencia.
        directorio = ocultoDirectorio.split(separadorPickerDirectory)[0]

        print("Resumen del form")
        print(form_data)
        print("Ruta origen: ", urlBase + "\\" + directorio)
        print("Ruta destino: ", urlDestino)

        # Si el directorio no está creado, lo creamos
        # if not os.path.exists(urlDestino):
        #     os.mkdir(urlDestino)
        
        
        if "dudosas" in form_data:
            print("Dudosas")
        else:
            print("No dudosas")

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
    for i in range(7):
        estadoEjecucion.mensaje = "Cargando modelo " + str(i)
        model = keras.models.load_model(urlModelos + modelos_AE[i], custom_objects={"correntropy" : correntropy})
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