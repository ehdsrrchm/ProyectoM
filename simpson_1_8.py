import tkinter as tk
from tkinter import ttk, messagebox
from sympy import sympify, symbols, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

x = symbols('x')

def ejecutar():
    root = tk.Toplevel()
    root.title("Integración por Método de Simpson 1/8")
    root.geometry("800x700")
    
    # Variables
    func_expr = None
    xi_entries = []
    fx_labels = []
    
    # Frame para función
    frame_func = ttk.LabelFrame(root, text="Función f(x)")
    frame_func.pack(padx=10, pady=5, fill="x")
    
    ttk.Label(frame_func, text="f(x) =").pack(side="left")
    func_entry = ttk.Entry(frame_func, width=40)
    func_entry.pack(side="left", padx=5, expand=True, fill="x")
    
    # Frame para datos
    frame_datos = ttk.LabelFrame(root, text="Datos de Entrada")
    frame_datos.pack(padx=10, pady=5, fill="x")
    
    ttk.Label(frame_datos, text="Número de puntos:").pack(side="left")
    n_entry = ttk.Entry(frame_datos, width=5)
    n_entry.pack(side="left", padx=5)
    n_entry.insert(0, "5")
    
    btn_crear_tabla = ttk.Button(frame_datos, text="Crear tabla", command=lambda: crear_tabla())
    btn_crear_tabla.pack(side="left", padx=5)
    
    # Frame para tabla
    tabla_frame = ttk.Frame(root)
    tabla_frame.pack(pady=10)
    
    # Frame para gráfico
    frame_grafico = ttk.LabelFrame(root, text="Gráfico de la Función")
    frame_grafico.pack(padx=10, pady=5, fill="both", expand=True)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Frame para resultados
    frame_resultado = ttk.LabelFrame(root, text="Resultado")
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
            if n < 3:
                raise ValueError("Debe haber al menos 3 puntos.")
            if (n-1) % 2 != 0:
                raise ValueError("Para Simpson 1/8, n-1 debe ser par (número de segmentos par).")
            
            # Encabezados
            ttk.Label(tabla_frame, text="x_i", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
            ttk.Label(tabla_frame, text="f(x_i)", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
            
            # Filas de datos
            for i in range(n):
                ttk.Label(tabla_frame, text=f"Punto {i+1}").grid(row=i+1, column=0, padx=5, pady=2, sticky="e")
                
                entry = ttk.Entry(tabla_frame, width=10)
                entry.grid(row=i+1, column=1, padx=5, pady=2)
                xi_entries.append(entry)
                
                fx_label = ttk.Label(tabla_frame, text="?", width=12)
                fx_label.grid(row=i+1, column=2, padx=5, pady=2)
                fx_labels.append(fx_label)
            
            btn_calcular = ttk.Button(tabla_frame, text="Calcular Integral", command=calcular_integral)
            btn_calcular.grid(row=n+1, column=0, columnspan=3, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
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
            
            # Verificar equidistancia
            h = xs[1] - xs[0]
            if not np.allclose(np.diff(xs), h):
                raise ValueError("Los puntos x_i deben ser equidistantes.")
            
            # Actualizar tabla con f(x_i)
            for i, label in enumerate(fx_labels):
                label.config(text=f"{ys[i]:.6f}")
            
            # Calcular integral (Simpson 1/8)
            suma = ys[0] + ys[-1]
            for i in range(1, len(ys)-1):
                suma += 4 * ys[i] if i % 2 == 1 else 2 * ys[i]
            integral = (h / 3) * suma
            
            # Mostrar resultado
            resultado_label.config(text=f"Resultado de la integral: {integral:.8f}")
            
            # Graficar
            actualizar_grafico(xs, ys, f)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def actualizar_grafico(xs, ys, f):
        ax.clear()
        
        # Graficar función real
        x_min, x_max = min(xs), max(xs)
        x_range = np.linspace(x_min, x_max, 100)
        y_range = f(x_range)
        ax.plot(x_range, y_range, 'b-', label='Función')
        
        # Graficar parábolas de Simpson
        for i in range(0, len(xs)-1, 2):
            if i+2 < len(xs):
                x_parabola = np.linspace(xs[i], xs[i+2], 20)
                # Coeficientes para la parábola que pasa por los 3 puntos
                A = np.array([
                    [xs[i]**2, xs[i], 1],
                    [xs[i+1]**2, xs[i+1], 1],
                    [xs[i+2]**2, xs[i+2], 1]
                ])
                b = np.array([ys[i], ys[i+1], ys[i+2]])
                coeffs = np.linalg.solve(A, b)
                y_parabola = coeffs[0]*x_parabola**2 + coeffs[1]*x_parabola + coeffs[2]
                ax.fill_between(x_parabola, y_parabola, alpha=0.3, color='green')
        
        # Graficar puntos
        ax.plot(xs, ys, 'ro', label='Puntos')
        
        # Configurar gráfico
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Método de Simpson 1/8')
        ax.legend()
        ax.grid(True)
        
        canvas.draw()
    
    # Crear tabla inicial
    crear_tabla()