import tkinter as tk
from tkinter import ttk

from Cronometro import Cronometro
from Temporizador import Temporizador
from Vehiculo import Vehiculo


class InterfazCarrera(tk.Tk):
    ANCHO_PISTA = 960
    ALTO_CARRIL = 48
    MARGEN_INFO = 150

    DATOS_VEHICULOS = [
        "Chicharito Hernandez",
        "Pate cumbia",
        "El popis",
        "Sol Naciente",
        "Halcon Nocturno",
        "Molly",
        "Verde Fuxia",
        "Tornado Loco",
        "Betrosky, Un poco loco",
        "Meteoro",
    ]

    def __init__(self):
        super().__init__()
        self.title("Carrera de vehiculos - Temporizadores")
        self.resizable(False, False)

        self.escala = 1.0
        self.cronometro = Cronometro()
        self.vehiculos = []
        self.llegadas = []
        self.enCarrera = False

        self.crearPista()
        self.crearPanelControl()
        self.crearVehiculos()

        self.temporizadorReloj = Temporizador(self, 50, self.actualizarReloj)

    def crearPista(self):
        altoPista = self.ALTO_CARRIL * len(self.DATOS_VEHICULOS) + 20
        self.canvas = tk.Canvas(self, width=self.ANCHO_PISTA, height=altoPista, bg="#3f3f46",highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.xMin = self.MARGEN_INFO
        self.xMax = self.ANCHO_PISTA - 20 - Vehiculo.ancho

        for i in range(len(self.DATOS_VEHICULOS)):
            y0 = 10 + i * self.ALTO_CARRIL
            self.canvas.create_rectangle(0, y0, self.ANCHO_PISTA, y0 + self.ALTO_CARRIL,fill="#cce6ee" if i % 2 == 0 else "#CED6D7",outline="", tags=f"carril{i + 1}")
            for x in range(self.MARGEN_INFO, self.ANCHO_PISTA, 30):
                self.canvas.create_line(x, y0, x + 15, y0, fill="white", width=2)

        tamCuadro = 8
        xBandera = self.xMin - 2 * tamCuadro - 4
        for fila in range((altoPista - 20) // tamCuadro):
            for col in range(2):
                color = "black" if (fila + col) % 2 == 0 else "white"
                yc = 10 + fila * tamCuadro
                xc = xBandera + col * tamCuadro
                self.canvas.create_rectangle(xc, yc, xc + tamCuadro, yc + tamCuadro, fill=color, outline="")
        xRetorno = self.xMax + Vehiculo.ancho + 4
        self.canvas.create_line(xRetorno, 10, xRetorno, altoPista - 10, fill="#ffff00", width=4)

    def crearPanelControl(self):
        panel = tk.Frame(self)
        panel.grid(row=0, column=1, sticky="n", padx=(0, 10), pady=10)

        marcoApuesta = tk.LabelFrame(panel, text="Apuesta", padx=8, pady=6)
        marcoApuesta.pack(fill="x", pady=4)
        self.comboApuesta = ttk.Combobox(marcoApuesta, state="readonly", width=24,values=[f"{i + 1}. {nombre}" for i, nombre in enumerate(self.DATOS_VEHICULOS)])
        self.comboApuesta.pack()
        self.comboApuesta.bind("<<ComboboxSelected>>", lambda evento: self.resaltarApuesta())

        marcoRondas = tk.LabelFrame(panel, text="Rondas (ida y vuelta)", padx=8, pady=6)
        marcoRondas.pack(fill="x", pady=4)
        self.varRondas = tk.IntVar(value=2)
        self.spinRondas = tk.Spinbox(marcoRondas, from_=1, to=20, width=6, textvariable=self.varRondas, justify="center")
        self.spinRondas.pack()

        marcoVelocidad = tk.LabelFrame(panel, text="Velocidad del juego", padx=8, pady=6)
        marcoVelocidad.pack(fill="x", pady=4)
        self.sliderVelocidad = tk.Scale(marcoVelocidad, from_=0.25, to=4.0, resolution=0.25,
                                        orient="horizontal", length=200, command=self.cambiarEscala)
        self.sliderVelocidad.set(1.0)
        self.sliderVelocidad.pack()

        marcoBotones = tk.Frame(panel)
        marcoBotones.pack(fill="x", pady=6)
        self.botonIniciar = tk.Button(marcoBotones, text="Iniciar carrera", width=13, bg="#16a34a", fg="white",
                                      command=self.iniciarCarrera)
        self.botonIniciar.pack(side="left", padx=2)
        self.botonReiniciar = tk.Button(marcoBotones, text="Reiniciar", width=13, command=self.reiniciarCarrera)
        self.botonReiniciar.pack(side="left", padx=2)

        self.labelReloj = tk.Label(panel, text="Tiempo: 0.00 s", font=("Consolas", 14, "bold"))
        self.labelReloj.pack(pady=4)
        self.labelEstado = tk.Label(panel, text="Elige un vehiculo y presiona Iniciar", wraplength=240,
                                    justify="center")
        self.labelEstado.pack(pady=4)

        marcoTabla = tk.LabelFrame(panel, text="Resultados", padx=4, pady=4)
        marcoTabla.pack(fill="x", pady=4)
        self.tabla = ttk.Treeview(marcoTabla, columns=("pos", "vehiculo", "tiempo"), show="headings", height=10)
        self.tabla.heading("pos", text="#")
        self.tabla.heading("vehiculo", text="Vehiculo")
        self.tabla.heading("tiempo", text="Tiempo (s)")
        self.tabla.column("pos", width=30, anchor="center")
        self.tabla.column("vehiculo", width=130)
        self.tabla.column("tiempo", width=80, anchor="e")
        self.tabla.tag_configure("apuesta", background="#fde68a")
        self.tabla.pack()

    def crearVehiculos(self):
        for i, nombre in enumerate(self.DATOS_VEHICULOS):
            yCentro = 10 + i * self.ALTO_CARRIL + self.ALTO_CARRIL // 2
            vehiculo = Vehiculo(i + 1, nombre, self.canvas, yCentro, self.xMin, self.xMax,
                                lambda: self.escala, self.vehiculoTermino)
            self.vehiculos.append(vehiculo)

    def resaltarApuesta(self):
        apuesta = self.vehiculoApostado()
        for i in range(len(self.vehiculos)):
            if i % 2 == 0:
                colorBase = "#cce6ee"
            else:
                colorBase = "#CED6D7"

            if apuesta is not None and apuesta.numero == i + 1:
                colorCarril = "#ff0a02"
            else:
                colorCarril = colorBase

            self.canvas.itemconfig(f"carril{i + 1}", fill=colorCarril)

    def vehiculoApostado(self):
        indice = self.comboApuesta.current()
        return self.vehiculos[indice] if indice >= 0 else None

    def bloquearControles(self, bloquear):
        estado = "disabled" if bloquear else "normal"
        self.comboApuesta.config(state="disabled" if bloquear else "readonly")
        self.spinRondas.config(state=estado)
        self.botonIniciar.config(state=estado)


    def cambiarEscala(self, valor):
        self.escala = float(valor)
        self.cronometro.cambiarEscala(self.escala)

    def iniciarCarrera(self):
        if self.enCarrera:
            return
        if self.vehiculoApostado() is None:
            self.labelEstado.config(text="Debes apostar por un vehiculo antes de iniciar.")
            return
        rondas = self.varRondas.get()
        if not 1 <= rondas <= 20:
            self.labelEstado.config(text="El numero de rondas debe ser un entero entre 1 y 20.")
            return

        self.reiniciarCarrera()
        self.enCarrera = True
        self.bloquearControles(True)
        self.labelEstado.config(text=f"Carrera en curso: {rondas} ronda(s)...")

        self.cronometro.iniciar()
        self.temporizadorReloj.iniciar()
        for vehiculo in self.vehiculos:
            vehiculo.iniciar(rondas)

    def vehiculoTermino(self, vehiculo):
        vehiculo.tiempoFinal = self.cronometro.tiempoTranscurrido()
        self.llegadas.append(vehiculo)
        posicion = len(self.llegadas)
        self.agregarFila(posicion, vehiculo)

        if posicion == 1:
            self.labelEstado.config(text=f"{vehiculo.nombre} cruzo primero la meta!")
        if posicion == len(self.vehiculos):
            self.finalizarCarrera()

    def agregarFila(self, posicion, vehiculo):
        if vehiculo is self.vehiculoApostado():
            etiquetas = ("apuesta",)
        else:
            etiquetas = ()

        self.tabla.insert("", "end", values=(posicion, vehiculo.nombre, f"{vehiculo.tiempoFinal:.2f}"),
                          tags=etiquetas)

    def finalizarCarrera(self):
        self.enCarrera = False
        self.cronometro.detener()
        self.temporizadorReloj.detener()
        self.actualizarReloj()

        ordenados = sorted(self.vehiculos, key=lambda v: v.tiempoFinal)
        self.tabla.delete(*self.tabla.get_children())
        for posicion, vehiculo in enumerate(ordenados, start=1):
            self.agregarFila(posicion, vehiculo)

        ganador = ordenados[0]
        apuesta = self.vehiculoApostado()
        if apuesta is ganador:
            mensaje = f"Ganaste la apuesta! {ganador.nombre} fue el ganador."
        else:
            posicionApuesta = ordenados.index(apuesta) + 1
            mensaje = (f"Perdiste la apuesta. Gano {ganador.nombre}.\n"
                       f"{apuesta.nombre} llego en la posicion {posicionApuesta}.")
        self.labelEstado.config(text=mensaje)
        self.bloquearControles(False)

    def reiniciarCarrera(self):
        for vehiculo in self.vehiculos:
            vehiculo.reiniciar()
        self.temporizadorReloj.detener()
        self.cronometro.reiniciar()
        self.cronometro.cambiarEscala(self.escala)
        self.llegadas = []
        self.enCarrera = False
        self.tabla.delete(*self.tabla.get_children())
        self.actualizarReloj()
        self.bloquearControles(False)
        self.labelEstado.config(text="Elige un vehiculo y presiona Iniciar")

    def actualizarReloj(self):
        self.labelReloj.config(text=f"Tiempo: {self.cronometro.tiempoTranscurrido():.2f} s")


app = InterfazCarrera()
app.mainloop()
