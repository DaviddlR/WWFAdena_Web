# Clase que representará el estado de ejecución.
# Intercambiar información entre el hilo y app
import os

class EstadoEjecucion:
    def __init__(self):

        # Parámetros de configuración generales
        self.formularioCompleto = ""
        self.tarea = ""
        self.version = ""

        # Parámetros de ejecución para descarte de imágenes vacías.
        self.rutaOrigen = ""
        self.rutaDestino = ""
        self.dudosas = False
        self.umbralDudosas = 0


        # Estado de ejecución
        self.mensaje = "..."
        self.estado = "..."
        self.progreso = 0

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
        sp = ""

        urlBase = str(os.path.expanduser("~"))

        if "\\" in urlBase:
            print("Windows")
            urlDestino = urlBase + "\\Airesultados"
            sp = "\\"
        else:
            print("Linux")
            urlDestino = urlBase + "/Airesultados"
            sp = "/"


        # Formulario completo
        self.formularioCompleto = formulario

        # Modelo a utilizar
        self.tarea = formulario["modelo"]
        self.version = formulario["version"]

        # TODO: Rellenar formulario según la tarea que sea. Por ahora solo descarte vacías.

        # Carpeta de imágenes
        ocultoDirectorio = formulario["Oculto"]
        directorio = ocultoDirectorio.split("/")[0]
        self.rutaOrigen = urlBase + sp + directorio

        # Carpeta donde se almacenarán los resultados
        self.rutaDestino = urlDestino

        # Check si almacenar dudosas
        if "dudosas" in formulario:
            self.dudosas = True
            self.umbralDudosas = float(formulario["umbralDudosas"])
        else:
            self.dudosas = False
    