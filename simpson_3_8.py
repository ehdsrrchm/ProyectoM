import tkinter as tk
from tkinter import ttk, messagebox
from sympy import sympify, symbols, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

x = symbols('x')

def ejecutar():
    root = tk.Toplevel()
    root.title("Integración por Método de Simpson 3/8")

    # --- Función para centrar la ventana ---
    def centrar_ventana(win, ancho=600, alto=600):
        win.update_idletasks()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (ancho // 2)
        y = (hs // 2) - (alto // 2)
        win.geometry(f'{ancho}x{alto}+{x}+{y}')

    centrar_ventana(root, 600, 600)

    xi_entries = []
    fx_labels = []

    frame_func = ttk.LabelFrame(root, text="Función f(x)")
    frame_func.pack(padx=10, pady=5, fill="x")

    ttk.Label(frame_func, text="f(x) =").pack(side="left")
    func_entry = ttk.Entry(frame_func, width=30)
    func_entry.pack(side="left", padx=5, expand=True, fill="x")

    frame_datos = ttk.LabelFrame(root, text="Datos de Entrada")
    frame_datos.pack(padx=10, pady=5, fill="x")

    ttk.Label(frame_datos, text="Número de puntos:").pack(side="left")
    n_entry = ttk.Entry(frame_datos, width=5)
    n_entry.pack(side="left", padx=5)

    btn_crear_tabla = ttk.Button(frame_datos, text="Crear tabla", command=lambda: crear_tabla())
    btn_crear_tabla.pack(side="left", padx=5)

    btn_cerrar_ventana = ttk.Button(frame_datos, text="Cerrar Metodo", command=root.destroy)
    btn_cerrar_ventana.pack(side="left", padx=5)

    # --- Frame para la tabla con scroll vertical ---
    tabla_container = ttk.Frame(root)
    tabla_container.pack(padx=10, pady=5, fill="both", expand=False)

    canvas_tabla = tk.Canvas(tabla_container, height=180)
    scrollbar = ttk.Scrollbar(tabla_container, orient="vertical", command=canvas_tabla.yview)
    tabla_frame = ttk.Frame(canvas_tabla)

    tabla_frame.bind(
        "<Configure>",
        lambda e: canvas_tabla.configure(
            scrollregion=canvas_tabla.bbox("all")
        )
    )

    canvas_tabla.create_window((0, 0), window=tabla_frame, anchor="nw")
    canvas_tabla.configure(yscrollcommand=scrollbar.set)

    canvas_tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_grafico = ttk.LabelFrame(root, text="Gráfico de la Función")
    frame_grafico.pack(padx=10, pady=5, fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(4.5, 3))
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    frame_resultado = ttk.LabelFrame(root, text="Resultado")
    frame_resultado.pack(padx=10, pady=5, fill="both", expand=True)

    resultado_label = ttk.Label(frame_resultado, text="", font=("Arial", 12), wraplength=550)
    resultado_label.pack(fill="both", expand=True)

    def crear_tabla():
        nonlocal xi_entries, fx_labels
        for widget in tabla_frame.winfo_children():
            widget.destroy()
        xi_entries.clear()
        fx_labels.clear()

        try:
            n_puntos = int(n_entry.get())
            if n_puntos < 4:
                raise ValueError("Debe haber al menos 4 puntos.")
            if (n_puntos - 1) % 3 != 0:
                raise ValueError("Para Simpson 3/8, n-1 debe ser divisible entre 3.")

            ttk.Label(tabla_frame, text="n", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
            ttk.Label(tabla_frame, text="x_i", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
            ttk.Label(tabla_frame, text="f(x_i)", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)

            for i in range(n_puntos):
                ttk.Label(tabla_frame, text=f"{i + 1}").grid(row=i + 1, column=0, padx=5, pady=2, sticky="e")

                entry = ttk.Entry(tabla_frame, width=10)
                entry.grid(row=i + 1, column=1, padx=5, pady=2)
                xi_entries.append(entry)

                fx_label = ttk.Label(tabla_frame, text="?", width=12)
                fx_label.grid(row=i + 1, column=2, padx=5, pady=2, sticky="w")
                fx_labels.append(fx_label)

            btn_calcular = ttk.Button(tabla_frame, text="Calcular Integral", command=calcular_integral)
            btn_calcular.grid(row=n_puntos + 1, column=0, columnspan=3, pady=10)

        except Exception as e:
            # Mensaje de error en primer plano y foco a ventana método
            messagebox.showerror("Error", str(e), parent=root)
            root.lift()
            root.focus_force()

    def calcular_integral():
        try:
            expr = sympify(func_entry.get())
            f = lambdify(x, expr, modules=["numpy"])
            xs = []

            for entry in xi_entries:
                val = float(entry.get())
                xs.append(val)

            xs = np.array(xs)
            ys = f(xs)

            h = xs[1] - xs[0]
            if not np.allclose(np.diff(xs), h):
                raise ValueError("Los puntos x_i deben ser equidistantes.")

            for i, label in enumerate(fx_labels):
                label.config(text=f"{ys[i]:.6f}", anchor="center")

            suma = ys[0] + ys[-1]
            for i in range(1, len(ys) - 1):
                suma += 3 * ys[i] if i % 3 != 0 else 2 * ys[i]
            integral = (3 * h / 8) * suma

            resultado_label.config(text=f"Resultado de la integral: {integral:.8f}")

            actualizar_grafico(xs, ys, f)

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=root)
            root.lift()
            root.focus_force()

    def actualizar_grafico(xs, ys, f):
        ax.clear()

        x_min, x_max = min(xs), max(xs)
        x_range = np.linspace(x_min, x_max, 100)
        y_range = f(x_range)
        ax.plot(x_range, y_range, 'b-', label='Función')

        for i in range(0, len(xs) - 1, 3):
            if i + 3 < len(xs):
                x_cubica = np.linspace(xs[i], xs[i + 3], 30)
                A = np.array([
                    [xs[i]**3, xs[i]**2, xs[i], 1],
                    [xs[i + 1]**3, xs[i + 1]**2, xs[i + 1], 1],
                    [xs[i + 2]**3, xs[i + 2]**2, xs[i + 2], 1],
                    [xs[i + 3]**3, xs[i + 3]**2, xs[i + 3], 1]
                ])
                b = np.array([ys[i], ys[i + 1], ys[i + 2], ys[i + 3]])
                coeffs = np.linalg.solve(A, b)
                y_cubica = coeffs[0] * x_cubica**3 + coeffs[1] * x_cubica**2 + coeffs[2] * x_cubica + coeffs[3]
                ax.fill_between(x_cubica, y_cubica, alpha=0.3, color='purple')

        ax.plot(xs, ys, 'ro', label='Puntos')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Método de Simpson 3/8')
        ax.legend()
        ax.grid(True)
        canvas.draw()

