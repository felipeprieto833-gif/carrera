# Laboratorio 4 – Carrera de vehículos con temporizadores

Ejecutar:

```
python interfaz_carrera.py
```

Solo usa la librería estándar (tkinter).

## Archivos

| Archivo | Clase | Responsabilidad |
|---|---|---|
| `Temporizador.py` | `Temporizador` | Timer periódico con `widget.after()`; cada vehículo tiene uno propio (10 timers independientes). El intervalo se divide por la escala del slider. |
| `Cronometro.py` | `Cronometro` | Mide el tiempo del juego con `time.perf_counter()`, escalado por el slider, para que los tiempos no dependan de la velocidad elegida. |
| `Vehiculo.py` | `Vehiculo` | Dibujo del carro (imagen `car.png`) en el canvas, movimiento, conteo de rondas y velocidad aleatoria que cambia en cada extremo. |
| `interfaz_carrera.py` | `InterfazCarrera` | Ventana principal: pista, apuesta, rondas, slider, botones, reloj y tabla de resultados. |

## Cómo cumple cada requisito

- **GUI con tkinter**: `InterfazCarrera` hereda de `tk.Tk`.
- **Etiqueta con dibujo**: cada carro se dibuja en el canvas con la imagen `car.png` (`Vehiculo.dibujar`), identificado por su nombre, y la imagen se refleja para mirar hacia donde avanza.
- **Apuesta**: Combobox; el carril apostado se resalta y al final se anuncia si se ganó o no.
- **Rondas**: Spinbox (1 ronda = ida + vuelta).
- **Velocidad aleatoria**: `Vehiculo.cambiarVelocidad()` asigna un intervalo aleatorio al timer en cada extremo.
- **10 timers independientes**: un `Temporizador` por vehículo (más uno extra para el reloj en pantalla).
- **Slider**: escala de 0.25x a 4x; afecta a todos los timers y al cronómetro.
- **Iniciar / Reiniciar**: botones; la carrera se reinicia sin cerrar la ventana.
- **Tabla ordenada**: `ttk.Treeview` ordenada de menor a mayor tiempo, empezando por el ganador.

## ¿Por qué `after()` y no `threading.Timer`?

tkinter no es seguro para hilos: solo el hilo principal debe modificar los widgets. `after()` programa la función en el mismo bucle de eventos de la ventana, así que funciona como un timer sin bloquear la interfaz y sin riesgo de errores de concurrencia.
