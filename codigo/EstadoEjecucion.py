# Clase que representará el estado de ejecución.
# Intercambiar información entre el hilo y app


class EstadoEjecucion:
    def __init__(self):

        # Parámetros de configuración generales
        self.formularioCompleto = ""

        # Parámetros de ejecución para descarte de imágenes vacías.
        self.rutaOrigen = ""
        self.rutaDestino = ""
        self.dudosas = False


        # Estado de ejecución
        self.mensaje = "..."
        self.estado = "..."
        self.progreso = 0

    