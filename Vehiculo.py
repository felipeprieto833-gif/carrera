import random
import tkinter as tk

from Temporizador import Temporizador

class Vehiculo:
    reduccion = 8
    ancho = 59
    paso = 4
    intervaloMin = 10
    intervaloMax = 40

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
        self.imagen = tk.PhotoImage(file="car.png").subsample(self.reduccion)

        self.temporizador = Temporizador(canvas, self.intervaloMax, self.mover, obtenerEscala)

        self.canvas.create_text(10, y - 8, anchor="w", text=nombre, font=("Arial", 9, "bold"))
        self.canvas.create_text(10, y + 9, anchor="w", text="", font=("Arial", 8), tags=self.tagInfo)
        self.canvas.create_image(xMin, y, anchor="w", image=self.imagen, tags=self.tag)
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
        self.temporizador.cambiarIntervalo(random.randint(self.intervaloMin, self.intervaloMax))
        self.actualizarInfo()

    def velocidad(self):
        return self.paso * 1000 / self.temporizador.intervaloMs

    def mover(self):
        xAnterior = self.x
        self.x += self.paso * self.direccion

        if self.direccion == 1 and self.x >= self.xMax:
            self.x = self.xMax
            self.direccion = -1
            self.cambiarVelocidad()
            self.dibujar()
            return

        if self.direccion == -1 and self.x <= self.xMin:

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
        self.canvas.coords(self.tag, self.x, self.y)
