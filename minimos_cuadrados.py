import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def ejecutar():
    ventana_mc = tk.Toplevel()
    ventana_mc.title("Método de Mínimos Cuadrados")
    ventana_mc.geometry("900x700")
    
    # Frame para entrada de datos
    frame_entrada = ttk.LabelFrame(ventana_mc, text="Ingreso de Datos")
    frame_entrada.pack(pady=10, padx=10, fill="x")
    
    # Controles para número de puntos
    ttk.Label(frame_entrada, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5)
    spin_puntos = ttk.Spinbox(frame_entrada, from_=2, to=20, width=5)
    spin_puntos.grid(row=0, column=1, padx=5, pady=5)
    spin_puntos.set(5)
    
    # Tabla para ingresar puntos
    frame_tabla = ttk.Frame(frame_entrada)
    frame_tabla.grid(row=1, column=0, columnspan=2, pady=5)
    
    # Frame para gráfico
    frame_grafico = ttk.LabelFrame(ventana_mc, text="Gráfico de Ajuste")
    frame_grafico.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Crear figura de matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Frame para resultados
    frame_resultados = ttk.LabelFrame(ventana_mc, text="Resultados del Ajuste")
    frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Texto para mostrar resultados
    texto_resultados = scrolledtext.ScrolledText(frame_resultados, width=80, height=6)
    texto_resultados.pack(pady=5, padx=5, fill="both", expand=True)
    
    # Frame para evaluación
    frame_evaluar = ttk.Frame(ventana_mc)
    frame_evaluar.pack(pady=5, fill="x")
    
    ttk.Label(frame_evaluar, text="Evaluar y(x) en x =").pack(side="left", padx=5)
    entry_eval = ttk.Entry(frame_evaluar, width=10)
    entry_eval.pack(side="left", padx=5)
    btn_evaluar = ttk.Button(frame_evaluar, text="Evaluar", command=lambda: evaluar_funcion())
    btn_evaluar.pack(side="left", padx=5)
    
    # Variables para almacenar datos
    entries_x = []
    entries_y = []
    m = None
    b = None
    funcion = None
    
    def crear_tabla():
        # Limpiar tabla anterior
        for widget in frame_tabla.winfo_children():
            widget.destroy()
        
        n = int(spin_puntos.get())
        entries_x.clear()
        entries_y.clear()
        
        # Crear encabezados
        ttk.Label(frame_tabla, text="X", font=('Helvetica', 10, 'bold')).grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(frame_tabla, text="Y", font=('Helvetica', 10, 'bold')).grid(row=0, column=2, padx=5, pady=2)
        
        # Crear entradas
        for i in range(n):
            ttk.Label(frame_tabla, text=f"Punto {i+1}").grid(row=i+1, column=0, padx=5, pady=2)
            
            entry_x = ttk.Entry(frame_tabla, width=10)
            entry_x.grid(row=i+1, column=1, padx=5, pady=2)
            entries_x.append(entry_x)
            
            entry_y = ttk.Entry(frame_tabla, width=10)
            entry_y.grid(row=i+1, column=2, padx=5, pady=2)
            entries_y.append(entry_y)
    
    def calcular_minimos_cuadrados():
        try:
            n = int(spin_puntos.get())
            x = []
            y = []
            
            for i in range(n):
                x_val = float(entries_x[i].get())
                y_val = float(entries_y[i].get())
                x.append(x_val)
                y.append(y_val)
            
            # Calcular sumatorias
            sumx = sum(x)
            sumy = sum(y)
            sumxy = sum(xi*yi for xi, yi in zip(x, y))
            sumx2 = sum(xi**2 for xi in x)
            
            # Calcular pendiente (m) y ordenada al origen (b)
            denominador = n * sumx2 - sumx**2
            m_val = (n * sumxy - sumx * sumy) / denominador
            b_val = (sumy - m_val * sumx) / n
            
            # Generar función simbólica
            x_sym = sp.symbols('x')
            funcion_sym = m_val * x_sym + b_val
            
            # Mostrar resultados
            texto_resultados.delete(1.0, tk.END)
            texto_resultados.insert(tk.END, "Resultados del Ajuste Lineal:\n")
            texto_resultados.insert(tk.END, "----------------------------------\n")
            texto_resultados.insert(tk.END, f"Ecuación de la recta: y = {m_val:.6f}x + {b_val:.6f}\n\n")
            texto_resultados.insert(tk.END, f"Coeficiente de correlación (r): {calcular_coeficiente_correlacion(x, y, m_val, b_val):.6f}\n")
            texto_resultados.insert(tk.END, f"Coeficiente de determinación (r²): {calcular_coeficiente_correlacion(x, y, m_val, b_val)**2:.6f}\n")
            
            # Actualizar gráfico
            actualizar_grafico(x, y, m_val, b_val)
            
            # Guardar valores para evaluación posterior
            nonlocal m, b, funcion
            m = m_val
            b = b_val
            funcion = funcion_sym
            
        except ValueError as e:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los puntos")
    
    def calcular_coeficiente_correlacion(x, y, m, b):
        n = len(x)
        y_prom = sum(y) / n
        ss_tot = sum((yi - y_prom)**2 for yi in y)
        ss_res = sum((yi - (m*xi + b))**2 for xi, yi in zip(x, y))
        return (1 - ss_res/ss_tot)**0.5 if ss_tot != 0 else 0
    
    def actualizar_grafico(x, y, m, b):
        ax.clear()
        
        # Graficar puntos
        ax.scatter(x, y, color='red', label='Datos')
        
        # Graficar línea de ajuste
        x_min, x_max = min(x), max(x)
        x_range = np.linspace(x_min - 0.1*(x_max-x_min), x_max + 0.1*(x_max-x_min), 100)
        y_range = [m*xi + b for xi in x_range]
        ax.plot(x_range, y_range, 'b-', label=f'Ajuste: y = {m:.4f}x + {b:.4f}')
        
        # Configurar gráfico
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Ajuste Lineal por Mínimos Cuadrados')
        ax.legend()
        ax.grid(True)
        
        canvas.draw()
    
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
    
    # Botones
    btn_crear_tabla = ttk.Button(frame_entrada, text="Crear Tabla", command=crear_tabla)
    btn_crear_tabla.grid(row=0, column=2, padx=10)
    
    btn_calcular = ttk.Button(frame_entrada, text="Calcular Ajuste", command=calcular_minimos_cuadrados)
    btn_calcular.grid(row=0, column=3, padx=10)
    
    # Crear tabla inicial
    crear_tabla()