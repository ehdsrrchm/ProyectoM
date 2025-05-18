import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def ejecutar():
    ventana_newton = tk.Toplevel()
    ventana_newton.title("Método de Diferencias Divididas de Newton")

    w, h = 600, 600
    ws, hs = ventana_newton.winfo_screenwidth(), ventana_newton.winfo_screenheight()
    x, y = (ws // 2 - w // 2), (hs // 2 - h // 2)
    ventana_newton.geometry(f"{w}x{h}+{x}+{y}")

    ventana_newton.resizable(True, True)  # permitir redimensionar

    # --- Scroll setup ---
    canvas = tk.Canvas(ventana_newton)
    scrollbar = ttk.Scrollbar(ventana_newton, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_scrollable = ttk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")

    def on_configure(event):
        # actualizar área scrollable
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame_scrollable.bind("<Configure>", on_configure)

    def on_canvas_configure(event):
        # hacer que frame_scrollable ajuste su ancho al canvas
        canvas.itemconfig(window_id, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    frame_entrada = ttk.LabelFrame(frame_scrollable, text="Ingreso de Datos")
    frame_entrada.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_entrada, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5)
    spin_puntos = ttk.Spinbox(frame_entrada, from_=2, to=10, width=5)
    spin_puntos.grid(row=0, column=1, padx=5, pady=5)
    spin_puntos.set(3)

    frame_tabla = ttk.Frame(frame_entrada)
    frame_tabla.grid(row=1, column=0, columnspan=4, pady=5)

    frame_diferencias = ttk.LabelFrame(frame_scrollable, text="Tabla de Diferencias Divididas")
    frame_diferencias.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame_diferencias, height=12)
    tree.pack(pady=5, padx=5, fill="both", expand=True)

    frame_resultados = ttk.LabelFrame(frame_scrollable, text="Polinomio de Newton")
    frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)

    texto_polinomio = scrolledtext.ScrolledText(frame_resultados, width=80, height=10)
    texto_polinomio.pack(pady=5, padx=5, fill="both", expand=True)

    frame_evaluar = ttk.Frame(frame_scrollable)
    frame_evaluar.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_evaluar, text="Evaluar P(x) en x =").pack(side="left", padx=5)
    entry_eval = ttk.Entry(frame_evaluar, width=10)
    entry_eval.pack(side="left", padx=5)
    btn_evaluar = ttk.Button(frame_evaluar, text="Evaluar", command=lambda: evaluar_polinomio())
    btn_evaluar.pack(side="left", padx=5)

    btn_cerrar = ttk.Button(frame_evaluar, text="Cerrar Método", command=ventana_newton.destroy)
    btn_cerrar.pack(side="right", padx=5)

    entries_x = []
    entries_y = []
    diferencias = None
    x_vals = []
    polinomio = None

    def crear_tabla():
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        n = int(spin_puntos.get())
        entries_x.clear()
        entries_y.clear()

        ttk.Label(frame_tabla, text="X", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(frame_tabla, text="Y", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, padx=5, pady=2)

        for i in range(n):
            ttk.Label(frame_tabla, text=f"Punto {i+1}").grid(row=i+1, column=0, padx=5, pady=2)
            entry_x = ttk.Entry(frame_tabla, width=10)
            entry_x.grid(row=i+1, column=1, padx=5, pady=2)
            entries_x.append(entry_x)

            entry_y = ttk.Entry(frame_tabla, width=10)
            entry_y.grid(row=i+1, column=2, padx=5, pady=2)
            entries_y.append(entry_y)

    def calcular_diferencias():
        nonlocal diferencias, x_vals
        try:
            n = int(spin_puntos.get())
            x = []
            y = []

            for i in range(n):
                x_val = float(entries_x[i].get())
                y_val = float(entries_y[i].get())
                x.append(x_val)
                y.append(y_val)

            dd = np.zeros((n, n))
            for i in range(n):
                dd[i][0] = y[i]

            for j in range(1, n):
                for i in range(n - j):
                    dd[i][j] = (dd[i+1][j-1] - dd[i][j-1]) / (x[i+j] - x[i])

            mostrar_tabla_diferencias(x, dd, n)
            generar_polinomio(x, dd, n)

            diferencias = dd
            x_vals = x

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los puntos", parent=ventana_newton)

    def mostrar_tabla_diferencias(x, dd, n):
        tree.delete(*tree.get_children())

        tree["columns"] = ["orden"] + [f"DD{i}" for i in range(n)]
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("orden", width=100, anchor=tk.W)

        for i in range(n):
            tree.column(f"DD{i}", width=100, anchor=tk.CENTER)

        tree.heading("orden", text="Puntos", anchor=tk.W)
        for i in range(n):
            tree.heading(f"DD{i}", text=f"Orden {i}")

        for i in range(n):
            puntos = ",".join([f"{x[j]:.2f}" for j in range(i+1)])
            valores = [dd[0][j] if j <= i else "" for j in range(n)]
            tree.insert("", tk.END, values=[f"[{puntos}]"] + valores)

    def generar_polinomio(x, dd, n):
        nonlocal polinomio
        x_sym = sp.symbols('x')
        polinomio_sym = 0
        producto = 1

        texto_polinomio.delete(1.0, tk.END)
        texto_polinomio.insert(tk.END, "Polinomio de Newton:\n")
        texto_polinomio.insert(tk.END, "----------------------------------\n")
        texto_polinomio.insert(tk.END, "P(x) = ")

        for i in range(n):
            if i > 0:
                producto *= (x_sym - x[i-1])

            termino = dd[0][i] * producto
            polinomio_sym += termino

            if i > 0 and dd[0][i] >= 0:
                texto_polinomio.insert(tk.END, " + ")

            texto_polinomio.insert(tk.END, f"{dd[0][i]:.6f}")

            if i > 0:
                texto_polinomio.insert(tk.END, " * ")
                for j in range(i):
                    texto_polinomio.insert(tk.END, f"(x - {x[j]:.3f})")
                    if j < i-1:
                        texto_polinomio.insert(tk.END, " * ")

        polinomio_simplificado = sp.simplify(polinomio_sym)
        texto_polinomio.insert(tk.END, "\n\nPolinomio simplificado:\n")
        texto_polinomio.insert(tk.END, "----------------------------------\n")
        texto_polinomio.insert(tk.END, f"P(x) = {polinomio_simplificado}\n")

        polinomio = polinomio_simplificado

    def evaluar_polinomio():
        if polinomio is None:
            messagebox.showerror("Error", "Primero debe calcular el polinomio", parent=ventana_newton)
            return

        try:
            x_eval = float(entry_eval.get())
            x_sym = sp.symbols('x')
            resultado = polinomio.subs(x_sym, x_eval)

            texto_polinomio.insert(tk.END, f"\nEvaluación en x = {x_eval}:\n")
            texto_polinomio.insert(tk.END, f"P({x_eval}) = {resultado.evalf():.8f}\n")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido para x", parent=ventana_newton)

    btn_crear_tabla = ttk.Button(frame_entrada, text="Crear Tabla", command=crear_tabla)
    btn_crear_tabla.grid(row=0, column=2, padx=10)

    btn_calcular = ttk.Button(frame_entrada, text="Calcular Diferencias", command=calcular_diferencias)
    btn_calcular.grid(row=0, column=3, padx=10)

    crear_tabla()


