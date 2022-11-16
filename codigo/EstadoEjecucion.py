# Clase que representará el estado de ejecución.
# Intercambiar información entre el hilo y app


class EstadoEjecucion:
    def __init__(self):
        self.mensaje = "..."
        self.estado = "..."
        self.progreso = 0

    