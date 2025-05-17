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

def crear_menu(marco):
    def btn(nombre, func): return tk.Button(marco, text=nombre, width=30, command=lambda: abrir_metodo(nombre, func))

    tk.Label(marco, text="UNIDAD 1", font=("Helvetica",14,"bold")).pack(pady=5)
    btn("Punto Fijo", punto_fijo.Punto_Fijo).pack(pady=2)
    btn("Newton Raphson", Newton_raphson.Newton_Raphson).pack(pady=2)

    tk.Label(marco, text="UNIDAD 2", font=("Helvetica",14,"bold")).pack(pady=5)
    btn("Lagrange", lagrange.ejecutar).pack(pady=2)
    btn("Diferencias Divididas", diferencias_divididas.ejecutar).pack(pady=2)
    btn("Mínimos Cuadrados", minimos_cuadrados.ejecutar).pack(pady=2)

    tk.Label(marco, text="UNIDAD 3", font=("Helvetica",14,"bold")).pack(pady=5)
    btn("Trapecio", trapecio.ejecutar).pack(pady=2)
    btn("Simpson 1/8", simpson_1_8.ejecutar).pack(pady=2)
    btn("Simpson 3/8 (Pendiente)", lambda: messagebox.showinfo("Método","Pendiente")).pack(pady=2)

# Ventana principal
root = tk.Tk()
root.title("Menú de Métodos Numéricos")
centrar_ventana(root, 500, 600)

lbl = tk.Label(root, text="Selecciona un Método", font=("Helvetica",16,"bold"))
lbl.pack(pady=20)
frame = tk.Frame(root)
frame.pack()
crear_menu(frame)
root.mainloop()
# Fin del código