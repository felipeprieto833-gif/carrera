class Temporizador:
    
    def __init__(self, widget, intervaloMs, funcion, obtenerEscala=lambda: 1.0):
        self.widget = widget
        self.intervaloMs = intervaloMs
        self.funcion = funcion
        self.obtenerEscala = obtenerEscala
        self.idAfter = None
        self.activo = False

    def iniciar(self):
        if self.activo:
            return
        self.activo = True
        self._programar()

    def cambiarIntervalo(self, intervaloMs):
        self.intervaloMs = intervaloMs

    def detener(self):
        self.activo = False
        if self.idAfter is not None:
            self.widget.after_cancel(self.idAfter)
            self.idAfter = None

    def _programar(self):
        retardo = max(1, round(self.intervaloMs / self.obtenerEscala()))
        self.idAfter = self.widget.after(retardo, self._ejecutar)

    def _ejecutar(self):
        if not self.activo:
            return
        self.funcion()
        
        if self.activo:
            self._programar()
