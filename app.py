# Imports básicos
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os


import numpy as np

# WLS - En window 11 viene por defecto.

# Hilos
import threading
import time

# Código
from codigo.EstadoEjecucion import *
from codigo.DescarteVacias.Correntropy import *
from codigo.DescarteVacias.DescarteVacias import comenzarDescarteVacias

# Variables globales

urlModelos = "./Modelos_Entrenados/"
modeloKmeans = "kmeansServidor.pkl"
modelos_AE = ["AE_cluster0.h5", "AE_cluster1.h5", "AE_cluster2.h5", "AE_cluster3.h5", "AE_cluster4.h5", "AE_cluster5.h5", "AE_cluster6.h5"]
modeloClasificadora = "MLP_2_20_150_Cluster.h5"


# Parámetros de configuración recogidos del formulario y estado de la ejecución
# TODO: ¿Crear una clase para cada tipo de ejecución? (descarte, segmentación...)? O usar herencia??




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

    # Recopilamos datos del formulario y lo almacenamos en EstadoEjecucion
    if request.method == "POST":

        estadoEjecucion.__init__()
        estadoEjecucion.adjuntarFormulario(request.form)
        estadoEjecucion.mostrarEstado()    

    return render_template('procesando.html')




# Función para comenzar la ejecución. Inicia nuevo hilo.
@app.route("/comenzarTarea", methods=["POST"])
def empezarTareaLarga():
    hilo = threading.Thread(target=lambda: tareaLarga())
    hilo.start()

    return {"url":"/estadoTarea"}

# PROCESO EN SEGUNDO PLANO
def tareaLarga():
    comenzarDescarteVacias(estadoEjecucion)

# Función para comprobar el estado de la tarea y actualizar mensajes.
@app.route("/estadoTarea")
def getEstadoTarea():

    # Obtiene el estado de la tarea
    mensajeClustering = estadoEjecucion.mensajeClustering
    mensajeClasificacion = estadoEjecucion.mensajeClasificacion
    barraClustering = str(estadoEjecucion.barraClustering)
    barraClasificacion = str(estadoEjecucion.barraClasificacion)
    estado = estadoEjecucion.estado

    respuesta = {'estado':estado, "mensajeClustering":mensajeClustering, "mensajeClasificacion":mensajeClasificacion,
     "barraClustering":barraClustering, "barraClasificacion":barraClasificacion}

    # Devuelve toda la info
    return jsonify(respuesta)


# MAIN
if __name__ == '__main__':

    # Inicio de la APP
    app.run(debug=True)  # Se puede especificar el puerto