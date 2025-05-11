import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def ejecutar():
    ventana_newton = tk.Toplevel()
    ventana_newton.title("Método de Diferencias Divididas de Newton")
    ventana_newton.geometry("900x700")
    
    # Frame para entrada de datos
    frame_entrada = ttk.LabelFrame(ventana_newton, text="Ingreso de Datos")
    frame_entrada.pack(pady=10, padx=10, fill="x")
    
    # Controles para número de puntos
    ttk.Label(frame_entrada, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5)
    spin_puntos = ttk.Spinbox(frame_entrada, from_=2, to=10, width=5)
    spin_puntos.grid(row=0, column=1, padx=5, pady=5)
    spin_puntos.set(3)
    
    # Tabla para ingresar puntos
    frame_tabla = ttk.Frame(frame_entrada)
    frame_tabla.grid(row=1, column=0, columnspan=2, pady=5)
    
    # Frame para tabla de diferencias divididas
    frame_diferencias = ttk.LabelFrame(ventana_newton, text="Tabla de Diferencias Divididas")
    frame_diferencias.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Treeview para mostrar la tabla de diferencias
    tree = ttk.Treeview(frame_diferencias)
    tree.pack(pady=5, padx=5, fill="both", expand=True)
    
    # Frame para resultados del polinomio
    frame_resultados = ttk.LabelFrame(ventana_newton, text="Polinomio de Newton")
    frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Texto para mostrar el polinomio
    texto_polinomio = scrolledtext.ScrolledText(frame_resultados, width=80, height=8)
    texto_polinomio.pack(pady=5, padx=5, fill="both", expand=True)
    
    # Frame para evaluación
    frame_evaluar = ttk.Frame(ventana_newton)
    frame_evaluar.pack(pady=5, fill="x")
    
    ttk.Label(frame_evaluar, text="Evaluar P(x) en x =").pack(side="left", padx=5)
    entry_eval = ttk.Entry(frame_evaluar, width=10)
    entry_eval.pack(side="left", padx=5)
    btn_evaluar = ttk.Button(frame_evaluar, text="Evaluar", command=lambda: evaluar_polinomio())
    btn_evaluar.pack(side="left", padx=5)
    
    # Variables para almacenar datos
    entries_x = []
    entries_y = []
    diferencias = None
    x_vals = []
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
    
    def calcular_diferencias():
        try:
            n = int(spin_puntos.get())
            x = []
            y = []
            
            for i in range(n):
                x_val = float(entries_x[i].get())
                y_val = float(entries_y[i].get())
                x.append(x_val)
                y.append(y_val)
            
            # Inicializar matriz de diferencias divididas
            dd = np.zeros((n, n))
            for i in range(n):
                dd[i][0] = y[i]
            
            # Calcular diferencias divididas
            for j in range(1, n):
                for i in range(n - j):
                    dd[i][j] = (dd[i+1][j-1] - dd[i][j-1]) / (x[i+j] - x[i])
            
            # Mostrar tabla de diferencias en el Treeview
            mostrar_tabla_diferencias(x, dd, n)
            
            # Generar y mostrar polinomio
            generar_polinomio(x, dd, n)
            
            # Guardar datos para evaluación posterior
            nonlocal diferencias, x_vals, polinomio
            diferencias = dd
            x_vals = x
            
        except ValueError as e:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los puntos")
    
    def mostrar_tabla_diferencias(x, dd, n):
        # Limpiar treeview
        tree.delete(*tree.get_children())
        
        # Configurar columnas
        tree["columns"] = ["orden"] + [f"DD{i}" for i in range(n)]
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("orden", width=100, anchor=tk.W)
        
        for i in range(n):
            tree.column(f"DD{i}", width=100, anchor=tk.CENTER)
        
        # Crear encabezados
        tree.heading("orden", text="Puntos", anchor=tk.W)
        for i in range(n):
            tree.heading(f"DD{i}", text=f"Orden {i}")
        
        # Insertar datos
        for i in range(n):
            puntos = ",".join([f"{x[j]:.2f}" for j in range(i+1)])
            valores = [dd[0][j] if j <= i else "" for j in range(n)]
            tree.insert("", tk.END, values=[f"[{puntos}]"] + valores)
    
    def generar_polinomio(x, dd, n):
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
            
            # Mostrar término en el texto
            if i > 0 and dd[0][i] >= 0:
                texto_polinomio.insert(tk.END, " + ")
            
            texto_polinomio.insert(tk.END, f"{dd[0][i]:.6f}")
            
            if i > 0:
                texto_polinomio.insert(tk.END, " * ")
                for j in range(i):
                    texto_polinomio.insert(tk.END, f"(x - {x[j]:.3f})")
                    if j < i-1:
                        texto_polinomio.insert(tk.END, " * ")
        
        # Simplificar el polinomio
        polinomio_simplificado = sp.simplify(polinomio_sym)
        
        texto_polinomio.insert(tk.END, "\n\nPolinomio simplificado:\n")
        texto_polinomio.insert(tk.END, "----------------------------------\n")
        texto_polinomio.insert(tk.END, f"P(x) = {polinomio_simplificado}\n")
        
        nonlocal polinomio
        polinomio = polinomio_simplificado
    
    def evaluar_polinomio():
        if polinomio is None:
            messagebox.showerror("Error", "Primero debe calcular el polinomio")
            return
        
        try:
            x_eval = float(entry_eval.get())
            x_sym = sp.symbols('x')
            resultado = polinomio.subs(x_sym, x_eval)
            
            texto_polinomio.insert(tk.END, f"\nEvaluación en x = {x_eval}:\n")
            texto_polinomio.insert(tk.END, f"P({x_eval}) = {resultado.evalf():.8f}\n")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido para x")
    
    # Botones
    btn_crear_tabla = ttk.Button(frame_entrada, text="Crear Tabla", command=crear_tabla)
    btn_crear_tabla.grid(row=0, column=2, padx=10)
    
    btn_calcular = ttk.Button(frame_entrada, text="Calcular Diferencias", command=calcular_diferencias)
    btn_calcular.grid(row=0, column=3, padx=10)
    
    # Crear tabla inicial
    crear_tabla()