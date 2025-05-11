import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext

def ejecutar():
    ventana_lagrange = tk.Toplevel()
    ventana_lagrange.title("Método de Lagrange")
    ventana_lagrange.geometry("800x600")
    
    # Frame para entrada de datos
    frame_entrada = ttk.LabelFrame(ventana_lagrange, text="Ingreso de Datos")
    frame_entrada.pack(pady=10, padx=10, fill="x")
    
    # Controles para número de puntos
    ttk.Label(frame_entrada, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5)
    spin_puntos = ttk.Spinbox(frame_entrada, from_=2, to=10, width=5)
    spin_puntos.grid(row=0, column=1, padx=5, pady=5)
    spin_puntos.set(3)
    
    # Tabla para ingresar puntos
    frame_tabla = ttk.Frame(frame_entrada)
    frame_tabla.grid(row=1, column=0, columnspan=2, pady=5)
    
    # Frame para resultados
    frame_resultados = ttk.LabelFrame(ventana_lagrange, text="Resultados")
    frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Texto para mostrar resultados
    texto_resultados = scrolledtext.ScrolledText(frame_resultados, width=80, height=20)
    texto_resultados.pack(pady=5, padx=5, fill="both", expand=True)
    
    # Frame para evaluación
    frame_evaluar = ttk.Frame(ventana_lagrange)
    frame_evaluar.pack(pady=5, fill="x")
    
    ttk.Label(frame_evaluar, text="Evaluar P(x) en x =").pack(side="left", padx=5)
    entry_eval = ttk.Entry(frame_evaluar, width=10)
    entry_eval.pack(side="left", padx=5)
    btn_evaluar = ttk.Button(frame_evaluar, text="Evaluar", command=lambda: evaluar_polinomio(entry_eval.get(), polinomio, texto_resultados))
    btn_evaluar.pack(side="left", padx=5)
    
    # Variables para almacenar datos
    entries_x = []
    entries_y = []
    polinomio = None
    
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
    
    def calcular_lagrange():
        try:
            n = int(spin_puntos.get())
            x = []
            y = []
            
            for i in range(n):
                x_val = float(entries_x[i].get())
                y_val = float(entries_y[i].get())
                x.append(x_val)
                y.append(y_val)
            
            # Calcular denominadores * f(x)
            denominador = np.zeros(n)
            for i in range(n):
                denom = 1.0
                for j in range(n):
                    if j != i:
                        denom *= (x[i] - x[j])
                denominador[i] = y[i] / denom
            
            # Generar polinomio simbólico
            x_sym = sp.symbols('x')
            polinomio_sym = 0
            
            texto_resultados.delete(1.0, tk.END)
            texto_resultados.insert(tk.END, "Polinomio de Lagrange P(x):\n")
            texto_resultados.insert(tk.END, "----------------------------\n")
            texto_resultados.insert(tk.END, "P(x) =\n")
            
            for i in range(n):
                termino = denominador[i]
                texto_resultados.insert(tk.END, f"  + ({denominador[i]:.6f}) * ")
                
                # Construir el término simbólico
                for j in range(n):
                    if j != i:
                        termino *= (x_sym - x[j])
                        texto_resultados.insert(tk.END, f"(x - {x[j]:.3f})")
                        if j < n - 1 and (j + 1 != i or j + 1 < n):
                            texto_resultados.insert(tk.END, " * ")
                texto_resultados.insert(tk.END, "\n")
                
                polinomio_sym += termino
            
            # Simplificar el polinomio
            polinomio_simplificado = sp.simplify(polinomio_sym)
            
            texto_resultados.insert(tk.END, "\nPolinomio simplificado:\n")
            texto_resultados.insert(tk.END, "----------------------\n")
            texto_resultados.insert(tk.END, f"P(x) = {polinomio_simplificado}\n")
            
            nonlocal polinomio
            polinomio = polinomio_simplificado
            
        except ValueError as e:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los puntos")
    
    def evaluar_polinomio(x_eval, polinomio, texto_widget):
        if polinomio is None:
            messagebox.showerror("Error", "Primero debe calcular el polinomio")
            return
        
        try:
            x_val = float(x_eval)
            x_sym = sp.symbols('x')
            resultado = polinomio.subs(x_sym, x_val)
            
            texto_widget.insert(tk.END, f"\nEvaluación en x = {x_val}:\n")
            texto_widget.insert(tk.END, f"P({x_val}) = {resultado.evalf():.8f}\n")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido para x")
    
    # Botones
    btn_crear_tabla = ttk.Button(frame_entrada, text="Crear Tabla", command=crear_tabla)
    btn_crear_tabla.grid(row=0, column=2, padx=10)
    
    btn_calcular = ttk.Button(frame_entrada, text="Calcular Polinomio", command=calcular_lagrange)
    btn_calcular.grid(row=0, column=3, padx=10)
    
    # Crear tabla inicial
    crear_tabla()