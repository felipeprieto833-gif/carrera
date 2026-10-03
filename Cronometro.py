import time

class Cronometro:

    def __init__(self):
        self.tiempoInicio = None
        self.tiempoAcumulado = 0.0
        self.escala = 1.0

    def iniciar(self):
        self.tiempoAcumulado = 0.0
        self.tiempoInicio = time.perf_counter()

    def cambiarEscala(self, nuevaEscala):
        if self.tiempoInicio is not None:
            ahora = time.perf_counter()
            self.tiempoAcumulado += (ahora - self.tiempoInicio) * self.escala
            self.tiempoInicio = ahora
        self.escala = nuevaEscala

    def tiempoTranscurrido(self):
        if self.tiempoInicio is None:
            return self.tiempoAcumulado
        return self.tiempoAcumulado + (time.perf_counter() - self.tiempoInicio) * self.escala

    def detener(self):
        self.tiempoAcumulado = self.tiempoTranscurrido()
        self.tiempoInicio = None
        return self.tiempoAcumulado

    def reiniciar(self):
        self.tiempoInicio = None
        self.tiempoAcumulado = 0.0
