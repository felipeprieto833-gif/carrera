import time


class Cronometro:
    """Cronometro del juego: mide tiempo transcurrido escalado por la velocidad del juego.

    Si la escala es 2.0 el tiempo del juego avanza el doble de rapido que el real,
    asi los tiempos de la tabla no dependen de como se movio el slider.
    """

    def __init__(self):
        self.tiempoInicio = None
        self.tiempoAcumulado = 0.0
        self.escala = 1.0

    def iniciar(self):
        self.tiempoAcumulado = 0.0
        self.tiempoInicio = time.perf_counter()

    def cambiarEscala(self, nuevaEscala):
        # Se guarda lo acumulado con la escala anterior antes de cambiarla
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
