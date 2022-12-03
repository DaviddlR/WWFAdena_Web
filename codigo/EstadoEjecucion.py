# Clase que representará el estado de ejecución.
# Intercambiar información entre el hilo y app
import os

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
        self.dudosas = False
        self.umbralDudosas = 0


        # Estado de ejecución
        self.mensajeClustering = "..."
        self.mensajeClasificacion = "..."
        self.barraClustering = 0
        self.barraClasificacion = 0
        self.estado = "..."


    def mostrarEstado(self):
        print("\nESTADO")
        print("Tarea: ", self.tarea)
        print("Version: ", self.version)
        print("Ruta origen: ",self.rutaOrigen)
        print("Ruta destino: ", self.rutaDestino)
        print("Dudosas: ", self.dudosas)
        print("Umbral: ", self.umbralDudosas)

    def adjuntarFormulario(self, formulario):

        # Configuracion inicial

        urlBase = str(os.path.expanduser("~"))

        if "\\" in urlBase:
            print("Windows")
            urlDestino = urlBase + "\\Airesultados"
            self.sp = "\\"
        else:
            print("Linux")
            urlDestino = urlBase + "/Airesultados"
            self.sp = "/"

        # Creamos carpetas de resultados
        rutaAnimales = os.path.join(urlDestino, "Animales")
        rutaVacio = os.path.join(urlDestino, "Vacio")
        rutaDudosas = os.path.join(urlDestino, "Dudosas")

        # TODO: Comprobar que no exista ya
        os.mkdir(urlDestino)
        os.mkdir(rutaAnimales)
        os.mkdir(rutaVacio)
        os.mkdir(rutaDudosas)

        self.rutaAnimales = rutaAnimales
        self.rutaVacio = rutaVacio
        self.rutaDudosas = rutaDudosas

        # Formulario completo
        self.formularioCompleto = formulario

        # Modelo a utilizar
        self.tarea = formulario["modelo"]
        self.version = formulario["version"]

        # TODO: Rellenar formulario según la tarea que sea. Por ahora solo descarte vacías.

        # Carpeta de imágenes
        ocultoDirectorio = formulario["Oculto"]
        directorio = ocultoDirectorio.split("/")[0]  # Este separador es independiente del SO
        self.rutaOrigen = urlBase + self.sp + directorio

        # Carpeta donde se almacenarán los resultados
        self.rutaDestino = urlDestino

        # Check si almacenar dudosas
        if "dudosas" in formulario:
            self.dudosas = True
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
    