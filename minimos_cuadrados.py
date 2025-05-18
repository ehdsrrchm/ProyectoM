import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def ejecutar():
    ventana_mc = tk.Toplevel()
    ventana_mc.title("Método de Mínimos Cuadrados")
    ventana_mc.geometry("700x600")  # tamaño inicial
    ventana_mc.minsize(500, 400)  # tamaño mínimo

    # Centrar ventana
    ventana_mc.update_idletasks()  # Actualiza para obtener dimensiones correctas
    ancho_ventana = ventana_mc.winfo_width()
    alto_ventana = ventana_mc.winfo_height()
    ancho_pantalla = ventana_mc.winfo_screenwidth()
    alto_pantalla = ventana_mc.winfo_screenheight()

    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_mc.geometry(f"+{x}+{y}")

    ventana_mc.rowconfigure(0, weight=1)
    ventana_mc.columnconfigure(0, weight=1)

    # Canvas con scrollbar vertical
    canvas = tk.Canvas(ventana_mc)
    scrollbar = ttk.Scrollbar(ventana_mc, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Frame dentro del canvas
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configuración del frame scrollable para que expanda
    scrollable_frame.columnconfigure(0, weight=1)

    # Frame entrada datos
    frame_entrada = ttk.LabelFrame(scrollable_frame, text="Ingreso de Datos")
    frame_entrada.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
    frame_entrada.columnconfigure(1, weight=1)
    frame_entrada.columnconfigure(2, weight=1)
    frame_entrada.columnconfigure(3, weight=1)

    ttk.Label(frame_entrada, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    spin_puntos = ttk.Spinbox(frame_entrada, from_=2, to=20, width=5)
    spin_puntos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    spin_puntos.set(5)

    frame_tabla = ttk.Frame(frame_entrada)
    frame_tabla.grid(row=1, column=0, columnspan=4, pady=5, sticky="ew")
    for i in range(4):
        frame_tabla.columnconfigure(i, weight=1)

    # Frame gráfico
    frame_grafico = ttk.LabelFrame(scrollable_frame, text="Gráfico de Ajuste")
    frame_grafico.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
    scrollable_frame.rowconfigure(1, weight=1)  # para que crezca verticalmente
    frame_grafico.rowconfigure(0, weight=1)
    frame_grafico.columnconfigure(0, weight=1)

    fig, ax = plt.subplots()
    canvas_grafico = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas_grafico.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # Frame resultados
    frame_resultados = ttk.LabelFrame(scrollable_frame, text="Resultados del Ajuste")
    frame_resultados.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
    scrollable_frame.rowconfigure(2, weight=1)
    frame_resultados.rowconfigure(0, weight=1)
    frame_resultados.columnconfigure(0, weight=1)

    texto_resultados = scrolledtext.ScrolledText(frame_resultados)
    texto_resultados.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # Frame evaluar y botones
    frame_evaluar = ttk.Frame(scrollable_frame)
    frame_evaluar.grid(row=3, column=0, pady=5, padx=10, sticky="ew")
    scrollable_frame.rowconfigure(3, weight=0)
    frame_evaluar.columnconfigure(1, weight=1)

    ttk.Label(frame_evaluar, text="Evaluar y(x) en x =").pack(side="left", padx=5)
    entry_eval = ttk.Entry(frame_evaluar, width=10)
    entry_eval.pack(side="left", padx=5, fill="x", expand=True)

    def evaluar_funcion():
        if funcion is None:
            messagebox.showerror("Error", "Primero debe calcular el ajuste lineal")
            return
        try:
            x_eval = float(entry_eval.get())
            x_sym = sp.symbols('x')
            resultado = funcion.subs(x_sym, x_eval)
            texto_resultados.insert(tk.END, f"\nEvaluación en x = {x_eval}:\n")
            texto_resultados.insert(tk.END, f"y({x_eval}) = {resultado.evalf():.8f}\n")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido para x")

    btn_evaluar = ttk.Button(frame_evaluar, text="Evaluar", command=evaluar_funcion)
    btn_evaluar.pack(side="left", padx=5)

    btn_cerrar = ttk.Button(frame_evaluar, text="Cerrar Método", command=ventana_mc.destroy)
    btn_cerrar.pack(side="right", padx=5)

    # Variables y funciones internas
    entries_x = []
    entries_y = []
    m = None
    b = None
    funcion = None

    def crear_tabla():
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        n = int(spin_puntos.get())
        entries_x.clear()
        entries_y.clear()

        ttk.Label(frame_tabla, text="X", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(frame_tabla, text="Y", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, padx=5, pady=2, sticky="ew")

        for i in range(n):
            ttk.Label(frame_tabla, text=f"Punto {i+1}").grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
            entry_x = ttk.Entry(frame_tabla)
            entry_x.grid(row=i+1, column=1, padx=5, pady=2, sticky="ew")
            entries_x.append(entry_x)

            entry_y = ttk.Entry(frame_tabla)
            entry_y.grid(row=i+1, column=2, padx=5, pady=2, sticky="ew")
            entries_y.append(entry_y)

    def calcular_minimos_cuadrados():
        nonlocal m, b, funcion
        try:
            n = int(spin_puntos.get())
            x = []
            y = []

            for i in range(n):
                x_val = float(entries_x[i].get())
                y_val = float(entries_y[i].get())
                x.append(x_val)
                y.append(y_val)

            sumx = sum(x)
            sumy = sum(y)
            sumxy = sum(xi*yi for xi, yi in zip(x, y))
            sumx2 = sum(xi**2 for xi in x)

            denominador = n * sumx2 - sumx**2
            if denominador == 0:
                messagebox.showerror("Error", "Denominador cero: No se puede calcular el ajuste")
                return

            m_val = (n * sumxy - sumx * sumy) / denominador
            b_val = (sumy - m_val * sumx) / n

            x_sym = sp.symbols('x')
            funcion_sym = m_val * x_sym + b_val

            texto_resultados.delete(1.0, tk.END)
            texto_resultados.insert(tk.END, "Resultados del Ajuste Lineal:\n")
            texto_resultados.insert(tk.END, "----------------------------------\n")
            texto_resultados.insert(tk.END, f"Ecuación de la recta: y = {m_val:.6f}x + {b_val:.6f}\n\n")
            r = calcular_coeficiente_correlacion(x, y, m_val, b_val)
            texto_resultados.insert(tk.END, f"Coeficiente de correlación (r): {r:.6f}\n")
            texto_resultados.insert(tk.END, f"Coeficiente de determinación (r²): {r**2:.6f}\n")

            actualizar_grafico(x, y, m_val, b_val)

            m = m_val
            b = b_val
            funcion = funcion_sym

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los puntos")

    def calcular_coeficiente_correlacion(x, y, m, b):
        n = len(x)
        y_prom = sum(y) / n
        ss_tot = sum((yi - y_prom)**2 for yi in y)
        ss_res = sum((yi - (m*xi + b))**2 for xi, yi in zip(x, y))
        return (1 - ss_res/ss_tot)**0.5 if ss_tot != 0 else 0

    def actualizar_grafico(x, y, m, b):
        ax.clear()
        ax.scatter(x, y, color='red', label='Datos')
        x_min, x_max = min(x), max(x)
        x_range = np.linspace(x_min - 0.1*(x_max-x_min), x_max + 0.1*(x_max-x_min), 100)
        y_range = [m*xi + b for xi in x_range]
        ax.plot(x_range, y_range, 'b-', label=f'Ajuste: y = {m:.4f}x + {b:.4f}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Ajuste Lineal por Mínimos Cuadrados')
        ax.legend()
        ax.grid(True)
        canvas_grafico.draw()

    btn_crear_tabla = ttk.Button(frame_entrada, text="Crear Tabla", command=crear_tabla)
    btn_crear_tabla.grid(row=0, column=2, padx=10, sticky="ew")

    btn_calcular = ttk.Button(frame_entrada, text="Calcular Ajuste", command=calcular_minimos_cuadrados)
    btn_calcular.grid(row=0, column=3, padx=10, sticky="ew")

    crear_tabla()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ejecutar()
    root.mainloop()
