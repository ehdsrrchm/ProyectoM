import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext

def ejecutar():
    ventana_lagrange = tk.Toplevel()
    ventana_lagrange.title("Método de Lagrange")
    ventana_lagrange.geometry("725x600")
    ventana_lagrange.resizable(True, True)

    # Frame con canvas y scrollbar para scroll vertical en toda la ventana
    frame_con_scroll = ttk.Frame(ventana_lagrange)
    frame_con_scroll.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_con_scroll)
    scrollbar = ttk.Scrollbar(frame_con_scroll, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_configure)

    # Función para centrar ventana
    def centrar_ventana(win):
        win.update_idletasks()
        ancho_ventana = win.winfo_width()
        alto_ventana = win.winfo_height()
        ancho_pantalla = win.winfo_screenwidth()
        alto_pantalla = win.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        win.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    # Centrar ventana inicial
    centrar_ventana(ventana_lagrange)

    frame_entrada = ttk.LabelFrame(scrollable_frame, text="Ingreso de Datos")
    frame_entrada.pack(pady=10, padx=10, fill="x")

    ttk.Label(frame_entrada, text="Número de puntos:").grid(row=0, column=0, padx=5, pady=5)
    spin_puntos = ttk.Spinbox(frame_entrada, from_=2, to=10, width=5)
    spin_puntos.grid(row=0, column=1, padx=5, pady=5)
    spin_puntos.set(3)

    frame_tabla = ttk.Frame(frame_entrada)
    frame_tabla.grid(row=1, column=0, columnspan=4, pady=5)

    frame_resultados = ttk.LabelFrame(scrollable_frame, text="Resultados")
    frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)

    texto_resultados = scrolledtext.ScrolledText(frame_resultados, width=80, height=20)
    texto_resultados.pack(pady=5, padx=5, fill="both", expand=True)

    frame_evaluar = ttk.Frame(scrollable_frame)
    frame_evaluar.pack(pady=5, fill="x")

    ttk.Label(frame_evaluar, text="Evaluar P(x) en x =").pack(side="left", padx=5)
    entry_eval = ttk.Entry(frame_evaluar, width=10)
    entry_eval.pack(side="left", padx=5)

    polinomio = None

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

    btn_evaluar = ttk.Button(frame_evaluar, text="Evaluar", command=lambda: evaluar_polinomio(entry_eval.get(), polinomio, texto_resultados))
    btn_evaluar.pack(side="left", padx=5)

    btn_cerrar = ttk.Button(frame_evaluar, text="Cerrar Metodo", command=ventana_lagrange.destroy)
    btn_cerrar.pack(side="right", padx=5)

    entries_x = []
    entries_y = []

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

            denominador = np.zeros(n)
            for i in range(n):
                denom = 1.0
                for j in range(n):
                    if j != i:
                        denom *= (x[i] - x[j])
                denominador[i] = y[i] / denom

            x_sym = sp.symbols('x')
            polinomio_sym = 0

            texto_resultados.delete(1.0, tk.END)
            texto_resultados.insert(tk.END, "Polinomio de Lagrange P(x):\n")
            texto_resultados.insert(tk.END, "----------------------------\n")
            texto_resultados.insert(tk.END, "P(x) =\n")

            for i in range(n):
                termino = denominador[i]
                texto_resultados.insert(tk.END, f"  + ({denominador[i]:.6f}) * ")
                for j in range(n):
                    if j != i:
                        termino *= (x_sym - x[j])
                        texto_resultados.insert(tk.END, f"(x - {x[j]:.3f})")
                        if j < n - 1 and (j + 1 != i or j + 1 < n):
                            texto_resultados.insert(tk.END, " * ")
                texto_resultados.insert(tk.END, "\n")
                polinomio_sym += termino

            polinomio_simplificado = sp.simplify(polinomio_sym)

            texto_resultados.insert(tk.END, "\nPolinomio simplificado:\n")
            texto_resultados.insert(tk.END, "----------------------\n")
            texto_resultados.insert(tk.END, f"P(x) = {polinomio_simplificado}\n")

            nonlocal polinomio
            polinomio = polinomio_simplificado

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para todos los puntos")

    btn_crear_tabla = ttk.Button(frame_entrada, text="Crear Tabla", command=crear_tabla)
    btn_crear_tabla.grid(row=0, column=2, padx=10)

    btn_calcular = ttk.Button(frame_entrada, text="Calcular Polinomio", command=calcular_lagrange)
    btn_calcular.grid(row=0, column=3, padx=10)

    crear_tabla()
    ventana_lagrange.update_idletasks()
    ventana_lagrange.minsize(ventana_lagrange.winfo_width(), ventana_lagrange.winfo_height())
    centrar_ventana(ventana_lagrange)  # Volver a centrar después de actualizar tamaño
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ejecutar()
    root.mainloop()