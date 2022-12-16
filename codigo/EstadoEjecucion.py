# Clase que representará el estado de ejecución.
# Intercambiar información entre el hilo y app
import os
from datetime import datetime

class EstadoEjecucion:
    def __init__(self):

        # Parámetros de configuración generales
        self.formularioCompleto = ""
        self.tarea = ""
        self.version = ""
        self.sp = ""  # Este separador es dependiente del SO
        self.imagenesTotales = 0

        # Parámetros de ejecución para descarte de imágenes vacías.
        self.rutaOrigen = ""
        self.rutaDestino = ""
        self.rutaAnimales = ""
        self.rutaVacio = ""
        self.rutaDudosas = ""
        self.moverIMG = False
        self.dudosas = False
        self.umbralDudosas = 0


        # Estado de ejecución
        self.mensajeClustering = "..."
        self.mensajeClasificacion = "..."
        self.barraClustering = 0
        self.barraClasificacion = 0
        self.usaGPU = "..."
        self.estado = "..."
        self.ejecucionEnCurso = False
        self.interrumpirEjecucion = False


    def mostrarEstado(self):
        print("\nESTADO")
        print("Tarea: ", self.tarea)
        print("Version: ", self.version)
        print("Ruta origen: ",self.rutaOrigen)
        print("Ruta destino: ", self.rutaDestino)
        print("Dudosas: ", self.dudosas)
        print("Umbral: ", self.umbralDudosas)

    def generarTXT(self):
        a = 1
        # Tarea

        # Versión del modelo

        # Ruta de origen de las imágenes

        # Ruta de destino de las imágenes

        # Mover o copiar imágenes

        # Umbral de dudosas. Si no hay dudosas, poner un guion.

        # Uso o no de GPU

        # Tiempo de ejecución????

    def adjuntarFormulario(self, formulario):

        #TODO: Dependiendo de la tarea elegida se hará un procesamiento u otro

        # Ruta del usuario
        urlBase = str(os.path.expanduser("~"))

        # Modelo a utilizar
        self.tarea = formulario["modelo"]
        self.version = formulario["version"]

        # Carpeta origen de imágenes
        ocultoDirectorio = formulario["Oculto"]
        directorio = ocultoDirectorio.split("/")[0]  # Este separador es independiente del SO
        self.rutaOrigen = os.path.join(urlBase, directorio)
        #self.rutaOrigen = urlBase + self.sp + directorio

        # Carpeta donde se almacenarán los resultados
        now = datetime.now()
        fechaActual = now.strftime("%d-%m-%Y__%H-%M-%S")	
        nombreCarpetaDestino = "zResultados_" + self.tarea.replace(" ","") + "_" + fechaActual
        urlDestino = os.path.join(self.rutaOrigen, nombreCarpetaDestino)

        self.rutaDestino = urlDestino
        

        # if "\\" in urlBase:
        #     print("Windows")
        #     urlDestino = urlBase + "\\Airesultados"
        #     self.sp = "\\"
        # else:
        #     print("Linux")
        #     urlDestino = urlBase + "/Airesultados"
        #     self.sp = "/"

        # Creamos carpetas de resultados
        rutaAnimales = os.path.join(urlDestino, "Animales")
        rutaVacio = os.path.join(urlDestino, "Vacio")
        rutaDudosas = os.path.join(urlDestino, "Dudosas")

        # TODO: Comprobar que no exista ya
        os.mkdir(urlDestino)

        os.mkdir(rutaAnimales)
        os.mkdir(rutaVacio)
        

        self.rutaAnimales = rutaAnimales
        self.rutaVacio = rutaVacio
        self.rutaDudosas = rutaDudosas

        # Formulario completo
        self.formularioCompleto = formulario

        # Check si copiar o mover
        if formulario['moverimg'] == 'copiar':
            self.moverIMG = False
        else:
            self.moverIMG = True

        # Check si almacenar dudosas
        if "dudosas" in formulario:
            self.dudosas = True
            os.mkdir(rutaDudosas)
            self.umbralDudosas = float(formulario["umbralDudosas"])
        else:
            self.dudosas = False


        # Calculamos el número de imágenes
        contador = 0
        for root, dirs, files in os.walk(self.rutaOrigen, topdown=False):
            for name in files:
                
                contador += 1

        self.imagenesTotales = contador

    
    def actualizarBarraClustering(self, numImagenes):
        self.barraClustering = int((100 * numImagenes) / self.imagenesTotales)

    def actualizarBarraClasificacion(self, numImagenes):
        self.barraClasificacion = int((100 * numImagenes) / self.imagenesTotales)
    