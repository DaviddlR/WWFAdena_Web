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
        self.fechaEjecucion = ""
        self.horaEjecucion = ""

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


    def mostrarEstado(self):
        print("\nESTADO")
        print("Tarea: ", self.tarea)
        print("Version: ", self.version)
        print("Ruta origen: ",self.rutaOrigen)
        print("Ruta destino: ", self.rutaDestino)
        print("Dudosas: ", self.dudosas)
        print("Umbral: ", self.umbralDudosas)

    def generarTXT(self, tiempoEjecucion):
        a = 1
        rutaTXT = os.path.join(self.rutaDestino, "Resumen_Ejecucion.txt")

        f = open(rutaTXT, "w")

        # Fecha de la ejecución
        f.write("Fecha: " + self.fechaEjecucion + "\n")

        # Hora de la ejecución
        f.write("Hora: " + self.horaEjecucion + "\n")

        # Tarea
        f.write("Tarea: " + self.tarea + "\n")

        # Versión del modelo
        f.write("Versión: " + self.version + "\n")

        # Ruta de origen de las imágenes
        f.write("Ruta de origen: " + self.rutaOrigen + "\n")

        # Ruta de destino de las imágenes
        f.write("Ruta de destino: " + self.rutaDestino + "\n")

        # Mover o copiar imágenes
        if self.moverIMG:
            f.write("Mover imágenes \n")
        else:
            f.write("Copiar imágenes \n")

        # Almacenar o no dudosas
        if self.dudosas:
            f.write("Almacenar imágenes dudosas \n")
            f.write("Umbral: " + str(self.umbralDudosas) + "\n")
        else:
            f.write("No almacenar imágenes dudosas \n")
        
        # Uso o no de GPU
        f.write("Modo de ejecución: " + self.usaGPU + "\n")

        # Número de imágenes
        f.write("Número de imágenes: " + str(self.imagenesTotales) + "\n")

        # Tiempo de ejecución
        f.write("Tiempo de ejecución: " + tiempoEjecucion + "\n")

        f.close()

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

        if not os.path.isdir(self.rutaOrigen):
            return False

        # Carpeta donde se almacenarán los resultados
        now = datetime.now()
        fechaActual = now.strftime("%d-%m-%Y__%H-%M-%S")	
        nombreCarpetaDestino = "00_Resultados_" + self.tarea.replace(" ","") + "_" + fechaActual
        urlDestino = os.path.join(self.rutaOrigen, nombreCarpetaDestino)

        self.rutaDestino = urlDestino

        # Almacenamos fecha y hora de ejecución
        fechaSeparado = fechaActual.split("__")
        self.fechaEjecucion = fechaSeparado[0]
        self.horaEjecucion = fechaSeparado[1].replace("-",":")

        # Creamos carpetas de resultados
        rutaAnimales = os.path.join(urlDestino, "Animales")
        rutaVacio = os.path.join(urlDestino, "Vacio")
        rutaDudosas = os.path.join(urlDestino, "Dudosas")

        # Comprobar que no exista ya
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

                rutaIMG = os.path.join(root, name)

                if not "00_Resultados_" in rutaIMG:
                    contador += 1

        self.imagenesTotales = contador
        print(contador)

        return True

    
    def actualizarBarraClustering(self, numImagenes):
        self.barraClustering = int((100 * numImagenes) / self.imagenesTotales)

    def actualizarBarraClasificacion(self, numImagenes):
        self.barraClasificacion = int((100 * numImagenes) / self.imagenesTotales)
    