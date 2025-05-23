import tkinter as tk
from tkinter import ttk, messagebox
from sympy import sympify, symbols, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

x = symbols('x')

def ejecutar():
    root = tk.Toplevel()
    root.title("Integración por Método del Trapecio")

    ancho_ventana = 600
    alto_ventana = 600  # un poco menos para scroll

    pantalla_ancho = root.winfo_screenwidth()
    pantalla_alto = root.winfo_screenheight()

    x_centro = (pantalla_ancho // 2) - (ancho_ventana // 2)
    y_centro = (pantalla_alto // 2) - (alto_ventana // 2)

    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x_centro}+{y_centro}")
    root.minsize(600, 400)

    # Frame principal con scroll
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Aquí dentro va todo el contenido que antes iba directo en root
    xi_entries = []
    fx_labels = []

    frame_func = ttk.LabelFrame(scrollable_frame, text="Función f(x)")
    frame_func.pack(padx=10, pady=5, fill="x")

    ttk.Label(frame_func, text="f(x) =").pack(side="left")
    func_entry = ttk.Entry(frame_func, width=40)
    func_entry.pack(side="left", padx=5, expand=True, fill="x")

    frame_datos = ttk.LabelFrame(scrollable_frame, text="Datos de Entrada")
    frame_datos.pack(padx=10, pady=5, fill="x")

    ttk.Label(frame_datos, text="Número de puntos:").pack(side="left")
    n_entry = ttk.Entry(frame_datos, width=5)
    n_entry.pack(side="left", padx=5)
    n_entry.insert(0, "5")

    btn_crear_tabla = ttk.Button(frame_datos, text="Crear tabla", command=lambda: crear_tabla())
    btn_crear_tabla.pack(side="left", padx=5)

    btn_cerrar = ttk.Button(frame_datos, text="Cerrar Método", command=root.destroy)
    btn_cerrar.pack(side="left", padx=5)

    tabla_frame = ttk.Frame(scrollable_frame)
    tabla_frame.pack(pady=10)

    frame_grafico = ttk.LabelFrame(scrollable_frame, text="Gráfico de la Función")
    frame_grafico.pack(padx=10, pady=5, fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    canvas_fig = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas_fig.get_tk_widget().pack(fill="both", expand=True)

    frame_resultado = ttk.LabelFrame(scrollable_frame, text="Resultado")
    frame_resultado.pack(padx=10, pady=5, fill="x")

    resultado_label = ttk.Label(frame_resultado, text="", font=("Arial", 12))
    resultado_label.pack()

    def crear_tabla():
        nonlocal xi_entries, fx_labels
        for widget in tabla_frame.winfo_children():
            widget.destroy()
        xi_entries.clear()
        fx_labels.clear()

        try:
            n = int(n_entry.get())
            if n < 2:
                raise ValueError("Debe haber al menos 2 puntos.")

            ttk.Label(tabla_frame, text="n", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
            ttk.Label(tabla_frame, text="x_i", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
            ttk.Label(tabla_frame, text="f(x_i)", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)

            for i in range(n):
                ttk.Label(tabla_frame, text=f"{i+1}").grid(row=i+1, column=0, padx=5, pady=2, sticky="e")

                entry = ttk.Entry(tabla_frame, width=10)
                entry.grid(row=i+1, column=1, padx=5, pady=2)
                xi_entries.append(entry)

                fx_label = ttk.Label(tabla_frame, text="?", width=12)
                fx_label.grid(row=i+1, column=2, padx=5, pady=2)
                fx_labels.append(fx_label)

            btn_calcular = ttk.Button(tabla_frame, text="Calcular Integral", command=calcular_integral)
            btn_calcular.grid(row=n+1, column=0, columnspan=3, pady=10)

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=root)

    def calcular_integral():
        try:
            expr = sympify(func_entry.get())
            f = lambdify(x, expr, modules=["numpy"])

            xs = [float(entry.get()) for entry in xi_entries]
            xs = np.array(xs)

            if not np.all(np.diff(xs) > 0):
                raise ValueError("Los puntos x_i deben estar en orden ascendente.")

            h = xs[1] - xs[0]
            if not np.allclose(np.diff(xs), h):
                raise ValueError("Los puntos x_i deben ser equidistantes.")

            ys = f(xs)

            for i, label in enumerate(fx_labels):
                label.config(text=f"{ys[i]:.6f}")

            integral = (h/2) * (ys[0] + 2*np.sum(ys[1:-1]) + ys[-1])

            resultado_label.config(text=f"Resultado de la integral: {integral:.8f}")

            actualizar_grafico(xs, ys, f)

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=root)

    def actualizar_grafico(xs, ys, f):
        ax.clear()

        x_min, x_max = min(xs), max(xs)
        x_range = np.linspace(x_min, x_max, 200)
        y_range = f(x_range)
        ax.plot(x_range, y_range, 'b-', label='Función')

        for i in range(len(xs)-1):
            ax.fill([xs[i], xs[i], xs[i+1], xs[i+1]],
                    [0, ys[i], ys[i+1], 0], 'r', alpha=0.3)

        ax.plot(xs, ys, 'ro', label='Puntos')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Método del Trapecio')
        ax.legend()
        ax.grid(True)

        canvas_fig.draw()

    crear_tabla()


