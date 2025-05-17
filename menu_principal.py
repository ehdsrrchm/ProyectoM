import tkinter as tk
from tkinter import messagebox

import punto_fijo
import Newton_raphson
import diferencias_divididas
import lagrange
import minimos_cuadrados
import trapecio
import simpson_1_8

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def abrir_metodo(nombre, funcion):
    ventana = tk.Toplevel(root)
    ventana.title(nombre)
    centrar_ventana(ventana, 450, 150)
    descripcion = {
        "Punto Fijo": "Método iterativo para encontrar raíces mediante x = g(x).",
        "Newton Raphson": "Método iterativo para encontrar raíces usando derivadas.",
        "Diferencias Divididas": "Interpolación con diferencias divididas.",
        "Lagrange": "Polinomio de interpolación de Lagrange.",
        "Mínimos Cuadrados": "Regresión lineal por mínimos cuadrados.",
        "Trapecio": "Integración numérica por trapecio.",
        "Simpson 1/8": "Integración numérica por Simpson 1/8."
    }
    lbl = tk.Label(ventana, text=descripcion.get(nombre, "No disponible."), wraplength=400, justify="left")
    lbl.pack(pady=10)
    btn_sig = tk.Button(ventana, text="Siguiente", command=lambda: [ventana.destroy(), funcion()])
    btn_sig.pack(side="left", padx=20, pady=10)
    btn_reg = tk.Button(ventana, text="Regresar", command=ventana.destroy)
    btn_reg.pack(side="right", padx=20, pady=10)

def mostrar_unidad(unidad):
    # Limpia el frame principal
    for widget in frame.winfo_children():
        widget.destroy()

    metodos_por_unidad = {
        "UNIDAD 1": [
            ("Punto Fijo", punto_fijo.Punto_Fijo),
            ("Newton Raphson", Newton_raphson.Newton_Raphson)
        ],
        "UNIDAD 2": [
            ("Lagrange", lagrange.ejecutar),
            ("Diferencias Divididas", diferencias_divididas.ejecutar),
            ("Mínimos Cuadrados", minimos_cuadrados.ejecutar)
        ],
        "UNIDAD 3": [
            ("Trapecio", trapecio.ejecutar),
            ("Simpson 1/8", simpson_1_8.ejecutar),
            ("Simpson 3/8 (Pendiente)", lambda: messagebox.showinfo("Método","Pendiente"))
        ]
    }

    tk.Label(frame, text=unidad, font=("Helvetica",16,"bold")).pack(pady=10)

    for nombre, funcion in metodos_por_unidad.get(unidad, []):
        btn = tk.Button(frame, text=nombre, width=30, command=lambda n=nombre, f=funcion: abrir_metodo(n, f))
        btn.pack(pady=5)

    # Botón para regresar al menú principal
    btn_regresar = tk.Button(frame, text="Regresar", width=30, command=mostrar_menu_principal)
    btn_regresar.pack(pady=20)

def mostrar_menu_principal():
    # Limpia el frame principal
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Selecciona una Unidad", font=("Helvetica",16,"bold")).pack(pady=20)

    for unidad in ["UNIDAD 1", "UNIDAD 2", "UNIDAD 3"]:
        btn = tk.Button(frame, text=unidad, width=30, command=lambda u=unidad: mostrar_unidad(u))
        btn.pack(pady=10)

# Ventana principal
root = tk.Tk()
root.title("Menú de Métodos Numéricos")
centrar_ventana(root, 500, 400)

frame = tk.Frame(root)
frame.pack(pady=20)

mostrar_menu_principal()

root.mainloop()
