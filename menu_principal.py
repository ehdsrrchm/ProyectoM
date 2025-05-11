
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import diferencias_divididas
import lagrange
import minimos_cuadrados
import trapecio
import simpson_1_8

def abrir_metodo(nombre, funcion):
    ventana_metodo = tk.Toplevel(root)
    ventana_metodo.title(nombre)

    descripcion = {
        "Diferencias Divididas": "Este método construye un polinomio de interpolación usando diferencias divididas.",
        "Lagrange": "El método de Lagrange permite construir un polinomio de interpolación basado en puntos dados.",
        "Mínimos Cuadrados": "Este método encuentra la recta que mejor se ajusta a un conjunto de puntos (regresión lineal).",
        "Trapecio": "Método de integración numérica basado en aproximar el área bajo la curva como un trapecio.",
        "Simpson 1/8": "Método de integración que usa parábolas para aproximar el área bajo la curva (1/8)."
    }

    tk.Label(ventana_metodo, text=descripcion.get(nombre, "Descripción no disponible."),
             wraplength=400, justify="left").pack(pady=10)

    btn_siguiente = tk.Button(ventana_metodo, text="Siguiente", command=lambda: [ventana_metodo.destroy(), funcion()])
    btn_siguiente.pack(side="left", padx=20, pady=10)

    btn_regresar = tk.Button(ventana_metodo, text="Regresar", command=ventana_metodo.destroy)
    btn_regresar.pack(side="right", padx=20, pady=10)

def crear_menu(marco):
    def crear_boton(nombre, funcion):
        return tk.Button(marco, text=nombre, width=30, command=lambda: abrir_metodo(nombre, funcion))

    tk.Label(marco, text="UNIDAD 1", font=("Helvetica", 14, "bold")).pack(pady=5)
    crear_boton("Método 1 (Pendiente)", lambda: messagebox.showinfo("Método", "Método 1 aún no implementado")).pack(pady=2)
    crear_boton("Método 2 (Pendiente)", lambda: messagebox.showinfo("Método", "Método 2 aún no implementado")).pack(pady=2)

    tk.Label(marco, text="UNIDAD 2", font=("Helvetica", 14, "bold")).pack(pady=5)
    crear_boton("Lagrange", lagrange.ejecutar).pack(pady=2)
    crear_boton("Diferencias Divididas", diferencias_divididas.ejecutar).pack(pady=2)
    crear_boton("Mínimos Cuadrados", minimos_cuadrados.ejecutar).pack(pady=2)

    tk.Label(marco, text="UNIDAD 3", font=("Helvetica", 14, "bold")).pack(pady=5)
    crear_boton("Trapecio", trapecio.ejecutar).pack(pady=2)
    crear_boton("Simpson 1/8", simpson_1_8.ejecutar).pack(pady=2)
    crear_boton("Simpson 3/8 (Pendiente)", lambda: messagebox.showinfo("Método", "Simpson 3/8 aún no implementado")).pack(pady=2)

# Ventana principal
root = tk.Tk()
root.title("Menú de Métodos Numéricos")
root.geometry("500x600")
tk.Label(root, text="Selecciona un Método", font=("Helvetica", 16, "bold")).pack(pady=20)

frame = tk.Frame(root)
frame.pack()
crear_menu(frame)

root.mainloop()
