import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import sympy as sp

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def Newton_Raphson():
    ventana = tk.Toplevel()
    ventana.title("Newton-Raphson")
    centrar_ventana(ventana, 500, 600)  # Tamaño igual al menú principal

    # Mostrar sistema textual
    frame_sys = ttk.LabelFrame(ventana, text="Sistema de Ecuaciones")
    frame_sys.pack(padx=10, pady=10, fill="x")
    ttk.Label(frame_sys, text="x²+xy-10 = 0").pack(anchor="w", padx=10, pady=2)
    ttk.Label(frame_sys, text="y+3xy²-57 = 0").pack(anchor="w", padx=10, pady=2)

    # Definiciones
    def f1(x, y): return x**2 + x*y - 10
    def f2(x, y): return y + 3*x*y**2 - 57

    def jacobian(x, y):
        return np.array([[2*x+y, x], [3*y**2, 1+6*x*y]], dtype=float)

    # Datos de entrada
    frame_in = ttk.LabelFrame(ventana, text="Datos de Entrada")
    frame_in.pack(padx=10, pady=10, fill="x")
    labels = ["x0", "y0", "Tolerancia", "Iter. Máx"]
    entries = {}
    for i, lbl in enumerate(labels):
        ttk.Label(frame_in, text=lbl+":").grid(row=i, column=0, padx=5, pady=5, sticky='e')
        ent = ttk.Entry(frame_in); ent.grid(row=i, column=1)
        entries[lbl] = ent
    entries["Tolerancia"].insert(0, "1e-6")
    entries["Iter. Máx"].insert(0, "100")

    btn_calc = ttk.Button(frame_in, text="Calcular", command=lambda: calcular(entries, text_res))
    btn_calc.grid(row=4, column=0, columnspan=2, pady=10)
    btn_reg = ttk.Button(frame_in, text="Cerrar Metodo", command=ventana.destroy)
    btn_reg.grid(row=4, column=2, padx=10)

    # Resultados
    text_res = tk.Text(ventana, width=80, height=20)
    text_res.pack(padx=10, pady=10, fill="both", expand=True)
    scroll = ttk.Scrollbar(ventana, command=text_res.yview)
    scroll.pack(side="right", fill="y")
    text_res.config(yscrollcommand=scroll.set)

    def calcular(entries, text_widget):
        try:
            x0 = float(entries["x0"].get())
            y0 = float(entries["y0"].get())
            tol = float(entries["Tolerancia"].get())
            max_iter = int(entries["Iter. Máx"].get())
        except:
            messagebox.showerror("Error", "Valores inválidos.")
            return

        data = []
        xy = np.array([x0, y0], dtype=float)
        for i in range(max_iter):
            x_n, y_n = xy
            F = np.array([f1(x_n, y_n), f2(x_n, y_n)])
            J = jacobian(x_n, y_n)
            try:
                delta = -np.linalg.inv(J).dot(F)
            except np.linalg.LinAlgError:
                messagebox.showerror("Error", "Jacobiana singular.")
                return
            xy = xy + delta
            err = np.linalg.norm(delta)
            data.append([
                i,
                round(x_n,4),
                round(y_n,4),
                round(F[0],4),
                round(F[1],4),
                round(xy[0],4),
                round(xy[1],4),
                round(err,4)
            ])
            if err < tol:
                break

        df = pd.DataFrame(data, columns=["n", "x_n", "y_n", "F_1", "F_2", "x_n+1", "y_n+1", "Error"])
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, df.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
        if err < tol:
            text_widget.insert(tk.END, f"\nConvergencia en {i+1} iteraciones. Sol: x={xy[0]:.4f}, y={xy[1]:.4f}")
        else:
            text_widget.insert(tk.END, "\nNo convergió en las iteraciones dadas.")
