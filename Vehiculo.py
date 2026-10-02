import os
import random
import tkinter as tk

from Temporizador import Temporizador

RUTA_IMAGEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "car.png")


class Vehiculo:
    REDUCCION = 8           # car.png (465x350) se reduce a 1/8 -> 59x44 px
    ANCHO = 59              # ancho de la imagen ya reducida
    PASO = 4                # pixeles que avanza en cada tick del timer
    INTERVALO_MIN = 10      # ms entre ticks (mas pequeño = mas rapido)
    INTERVALO_MAX = 40

    # Imagenes compartidas por todos los vehiculos (se cargan una sola vez)
    imagenDerecha = None
    imagenIzquierda = None

    @classmethod
    def cargarImagenes(cls):
        if cls.imagenDerecha is None:
            original = tk.PhotoImage(file=RUTA_IMAGEN)
            cls.imagenDerecha = original.subsample(cls.REDUCCION)
            # Subsample negativo en x refleja la imagen horizontalmente
            cls.imagenIzquierda = cls.imagenDerecha.subsample(-1, 1)

    def __init__(self, numero, nombre, canvas, y, xMin, xMax, obtenerEscala, alTerminar):
        self.numero = numero
        self.nombre = nombre
        self.canvas = canvas
        self.y = y
        self.xMin = xMin
        self.xMax = xMax
        self.alTerminar = alTerminar
        self.tag = f"vehiculo{numero}"
        self.tagInfo = f"info{numero}"
        Vehiculo.cargarImagenes()

        # Cada vehiculo tiene su propio timer independiente
        self.temporizador = Temporizador(canvas, self.INTERVALO_MAX, self.mover, obtenerEscala)

        self.canvas.create_text(10, y - 8, anchor="w", text=nombre, font=("Arial", 9, "bold"))
        self.canvas.create_text(10, y + 9, anchor="w", text="", font=("Arial", 8), tags=self.tagInfo)
        self.reiniciar()

    def reiniciar(self):
        self.temporizador.detener()
        self.x = self.xMin
        self.direccion = 1
        self.rondasCompletadas = 0
        self.rondasObjetivo = 0
        self.terminado = False
        self.tiempoFinal = None
        self.dibujar()
        self.actualizarInfo()

    def iniciar(self, rondas):
        self.rondasObjetivo = rondas
        self.cambiarVelocidad()
        self.temporizador.iniciar()

    def cambiarVelocidad(self):
        # Velocidad aleatoria = intervalo aleatorio del timer
        self.temporizador.cambiarIntervalo(random.randint(self.INTERVALO_MIN, self.INTERVALO_MAX))
        self.actualizarInfo()

    def velocidad(self):
        return self.PASO * 1000 / self.temporizador.intervaloMs

    def mover(self):
        xAnterior = self.x
        self.x += self.PASO * self.direccion

        if self.direccion == 1 and self.x >= self.xMax:
            # Llego al extremo derecho: da la vuelta
            self.x = self.xMax
            self.direccion = -1
            self.cambiarVelocidad()
            self.dibujar()
            return

        if self.direccion == -1 and self.x <= self.xMin:
            # Llego al extremo izquierdo: completa una ronda (ida y vuelta)
            self.x = self.xMin
            self.rondasCompletadas += 1
            if self.rondasCompletadas >= self.rondasObjetivo:
                self.temporizador.detener()
                self.terminado = True
                self.dibujar()
                self.actualizarInfo()
                self.alTerminar(self)
                return
            self.direccion = 1
            self.cambiarVelocidad()
            self.dibujar()
            return

        self.canvas.move(self.tag, self.x - xAnterior, 0)

    def actualizarInfo(self):
        if self.terminado:
            texto = f"Meta! ({self.rondasCompletadas}/{self.rondasObjetivo})"
        elif self.rondasObjetivo == 0:
            texto = "En parrilla"
        else:
            texto = f"Ronda {self.rondasCompletadas + 1}/{self.rondasObjetivo}  {self.velocidad():.0f} px/s"
        self.canvas.itemconfig(self.tagInfo, text=texto)

    def dibujar(self):
        """Dibuja el carro mirando hacia la direccion en que se mueve."""
        self.canvas.delete(self.tag)
        imagen = self.imagenDerecha if self.direccion == 1 else self.imagenIzquierda
        self.canvas.create_image(self.x, self.y, anchor="w", image=imagen, tags=self.tag)
