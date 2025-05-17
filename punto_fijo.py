import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd

#FUNCIONES COMUNES 

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

#VENTANA DE SELECCIONAR 

def Punto_Fijo():
    root = tk.Tk()
    root.title("Método de Punto Fijo")
    centrar_ventana(root, 400, 200)

    ttk.Label(root, text="Seleccione qué desea resolver:", font=("Arial", 12)).pack(pady=20)

    def abrir_ecuacion():
        root.withdraw()
        resolver_ecuacion(root)

    def abrir_sistema():
        root.withdraw()
        resolver_sistema(root)

    ttk.Button(root, text="Ecuación No Lineal", command=abrir_ecuacion).pack(pady=5)
    ttk.Button(root, text="Sistema de Ecuaciones", command=abrir_sistema).pack(pady=5)
    ttk.Button(root, text="Cerrar", command=root.destroy).pack(pady=15)

    root.mainloop()

#VENTANA ECUACIÓN 

def resolver_ecuacion(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Punto Fijo - Ecuación")
    centrar_ventana(ventana, 700, 450) # El ancho de la ventana ahora es 700

    frame_ecuacion = ttk.LabelFrame(ventana, text="Ecuación")
    frame_ecuacion.pack(padx=10, pady=10, fill="x")

    # Mostrar la ecuación f(x) = 0
    ttk.Label(frame_ecuacion, text="f(x) = x³ + x - 6 = 0").pack(anchor="w", padx=10)

    frame_g = ttk.LabelFrame(ventana, text="Función de Iteración")
    frame_g.pack(padx=10, pady=10, fill="x")
    # Mostrar g(x)
    ttk.Label(frame_g, text="g(x) = ∛(6 − x)").pack(anchor="w", padx=10)
    
    frame_datos = ttk.LabelFrame(ventana, text="Datos de Entrada")
    frame_datos.pack(padx=10, pady=10, fill="x")

    ttk.Label(frame_datos, text="x0:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entrada_x0 = ttk.Entry(frame_datos)
    entrada_x0.grid(row=0, column=1)
    
    ttk.Label(frame_datos, text="Tolerancia:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entrada_tol = ttk.Entry(frame_datos)
    entrada_tol.grid(row=1, column=1)
    entrada_tol.insert(0, "1e-6")

    ttk.Label(frame_datos, text="Iter. Máx:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entrada_iter = ttk.Entry(frame_datos)
    entrada_iter.grid(row=2, column=1)
    entrada_iter.insert(0, "100")

    text_res = tk.Text(ventana, width=70, height=15)
    text_res.pack(padx=10, pady=10, fill="both", expand=True) 
    text_res.pack(padx=10, pady=10, fill="both", expand=True)
    scroll = ttk.Scrollbar(ventana, command=text_res.yview)
    scroll.pack(side="right", fill="y")
    text_res.config(yscrollcommand=scroll.set)


    def calcular():
        try:
            # Usamos la función fija g(x) = (6 - x)**(1/3)
            g = lambda x: (6 - x)**(1/3)
            x0 = float(entrada_x0.get())
            tol = float(entrada_tol.get())
            max_iter = int(entrada_iter.get())
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return

        x = x0
        datos = []
        for i in range(max_iter):
            try:
                x_new = g(x)
                err = abs(x_new - x)
                datos.append([i, round(x, 6), round(x_new, 6), round(err, 6)])
                if err < tol:
                    break
                x = x_new
            except Exception as e:
                messagebox.showerror("Error", f"Error en la iteración: {e}")
                return

        df = pd.DataFrame(datos, columns=["n", "x_n", "x_n+1", "Error"])
        text_res.delete("1.0", tk.END)
        text_res.insert(tk.END, df.to_string(index=False))
        if err < tol:
            text_res.insert(tk.END, f"\n\nConvergió en {i+1} iteraciones. Solución aproximada: x = {x_new:.6f}")
        else:
            text_res.insert(tk.END, "\n\nNo convergió en las iteraciones dadas.")

    calcular_button = ttk.Button(frame_datos, text="Calcular", command=calcular)
    calcular_button.grid(row=3, column=0, columnspan=2, pady=10)
    cerrar_button = ttk.Button(frame_datos, text="Cerrar", command=lambda: cerrar_ecuacion(ventana, parent))
    cerrar_button.grid(row=3, column=2, padx=10, pady=10)

    def al_cerrar():
        cerrar_ecuacion(ventana, parent)

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

def cerrar_ecuacion(ventana, parent): # Función para cerrar la ventana Ecuacion
    ventana.destroy()
    parent.deiconify()  # Mostrar ventana de selección otra vez


# VENTANA SISTEMA 

def resolver_sistema(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Métodos Iterativos - Sistema No Lineal")
    centrar_ventana(ventana, 700, 600)

    frame_sys = ttk.LabelFrame(ventana, text="Sistema de Ecuaciones")
    frame_sys.pack(padx=10, pady=10, fill="x")
    ttk.Label(frame_sys, text="x² -10x + y² + 8 = 0").pack(anchor="w", padx=10)
    ttk.Label(frame_sys, text="xy² + x - 10y + 8 = 0").pack(anchor="w", padx=10)

    frame_in = ttk.LabelFrame(ventana, text="Datos de Entrada")
    frame_in.pack(padx=10, pady=10, fill="x")
    labels = ["x0", "y0", "Tolerancia", "Iter. Máx"]
    entries = {}
    for i, lbl in enumerate(labels):
        ttk.Label(frame_in, text=lbl+":").grid(row=i, column=0, padx=5, pady=5, sticky='e')
        ent = ttk.Entry(frame_in)
        ent.grid(row=i, column=1)
        entries[lbl] = ent
    entries["Tolerancia"].insert(0, "1e-6")
    entries["Iter. Máx"].insert(0, "100")

    ttk.Label(frame_in, text="Método:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    metodo_combo = ttk.Combobox(frame_in, values=["Jacobi", "Gauss-Seidel", "Ambos"], state="readonly")
    metodo_combo.current(0)
    metodo_combo.grid(row=4, column=1, padx=5, pady=5)

    text_res = tk.Text(ventana, width=90, height=25)
    text_res.pack(padx=10, pady=10, fill="both", expand=True)
    scroll = ttk.Scrollbar(ventana, command=text_res.yview)
    scroll.pack(side="right", fill="y")
    text_res.config(yscrollcommand=scroll.set)

    def g1(x, y): return (8 + y**2 + x**2) / 10
    def g2(x, y): return (8 + x + x * y**2) / 10
    def jacobi_iter(x, y): return g1(x, y), g2(x, y)
    def gauss_seidel_iter(x, y): x1 = g1(x, y); return x1, g2(x1, y)

    def iterar_metodo(x0, y0, tol, max_iter, metodo):
        data = []
        x, y = x0, y0
        for i in range(max_iter):
            if metodo == "Jacobi": x_new, y_new = jacobi_iter(x, y)
            elif metodo == "Gauss-Seidel": x_new, y_new = gauss_seidel_iter(x, y)
            else: return None
            err = np.linalg.norm([x_new - x, y_new - y])
            data.append([i, round(x,6), round(y,6), round(x_new,6), round(y_new,6), round(err,6)])
            if err < tol: return data, i+1, x_new, y_new
            x, y = x_new, y_new
        return data, max_iter, x, y

    def calcular():
        try:
            x0 = float(entries["x0"].get())
            y0 = float(entries["y0"].get())
            tol = float(entries["Tolerancia"].get())
            max_iter = int(entries["Iter. Máx"].get())
        except:
            messagebox.showerror("Error", "Valores inválidos.")
            return
        text_res.delete("1.0", tk.END)
        metodo = metodo_combo.get()
        if metodo == "Ambos":
            for met in ["Jacobi", "Gauss-Seidel"]:
                res = iterar_metodo(x0, y0, tol, max_iter, met)
                if res is None:
                    text_res.insert(tk.END, f"\n{met}: Error en iteración.\n\n")
                    continue
                data, iter_count, x_sol, y_sol = res
                df = pd.DataFrame(data, columns=["n", "x_n", "y_n", "x_n+1", "y_n+1", "Error"]).round(4)
                text_res.insert(tk.END, f"{met}:\n")
                text_res.insert(tk.END, df.to_string(index=False))
                text_res.insert(tk.END, f"\nConvergió en {iter_count} iteraciones. Solución aproximada: x={x_sol:.4f}, y={y_sol:.4f}\n\n" if iter_count < max_iter else "\nNo convergió.\n\n")
        else:
            res = iterar_metodo(x0, y0, tol, max_iter, metodo)
            if res is None:
                messagebox.showerror("Error", "Error en iteración.")
                return
            data, iter_count, x_sol, y_sol = res
            df = pd.DataFrame(data, columns=["n", "x_n", "y_n", "x_n+1", "y_n+1", "Error"]).round(4)
            text_res.insert(tk.END, df.to_string(index=False))
            text_res.insert(tk.END, f"\nConvergió en {iter_count} iteraciones. Solución aproximada: x={x_sol:.4f}, y={y_sol:.4f}" if iter_count < max_iter else "\nNo convergió.")

    btn_calc = ttk.Button(frame_in, text="Calcular", command=calcular)
    btn_calc.grid(row=5, column=0, columnspan=2, pady=10)
    btn_cerrar = ttk.Button(frame_in, text="Cerrar", command=lambda: cerrar_sistema(ventana, parent))
    btn_cerrar.grid(row=5, column=2, padx=10)

    def al_cerrar():
        cerrar_sistema(ventana, parent)

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

def cerrar_sistema(ventana, parent):
    ventana.destroy()
    parent.deiconify()  # Volver a mostrar la ventana de selección


