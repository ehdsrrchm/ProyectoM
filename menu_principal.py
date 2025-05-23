import tkinter as tk
from tkinter import messagebox

import punto_fijo
import Newton_raphson
import diferencias_divididas
import lagrange
import minimos_cuadrados
import trapecio
import simpson_1_3
import simpson_3_8

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# VENTANAS

def mostrar_portada():
    limpiar_frame()
    tk.Label(frame, text="UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO", font=("Helvetica", 12, "bold"), wraplength=450, justify="center").pack(pady=5)
    tk.Label(frame, text="FACULTAD DE ESTUDIOS SUPERIORES DE ACATLÁN", font=("Helvetica", 12, "bold"), wraplength=450, justify="center").pack(pady=5)
    tk.Label(frame, text="LICENCIATURA EN MATEMÁTICAS APLICADAS Y COMPUTACIÓN", font=("Helvetica", 12,"bold"), wraplength=450, justify="center").pack(pady=10)

    tk.Label(frame, text="Proyecto Final", font=("Helvetica", 16, "bold")).pack(pady=20)

    tk.Label(frame, text="Nombre de los integrantes del equipo", font=("Helvetica", 12, "bold")).pack()
    tk.Label(frame, text="Alonso Lopez Guillermo\nPichu Tellez Diego Yahir\nRojas Hernández Diego Alonso\nVenegas Reyes Emilio", font=("Helvetica", 11), justify="center").pack(pady=10)
    
    tk.Label(frame, text="Materia", font=("Helvetica", 12, "bold")).pack()
    tk.Label(frame, text="Metodos Numericos II", font=("Helvetica", 11)).pack(pady=2)
    tk.Label(frame, text="Grupo", font=("Helvetica", 12, "bold")).pack()
    tk.Label(frame, text="2454", font=("Helvetica", 11)).pack(pady=5)

    tk.Button(frame, text="Siguiente", width=20, command=mostrar_introduccion).pack(pady=10)
    tk.Button(frame, text="Cerrar aplicación", width=20, command=root.destroy).pack(pady=5)

def mostrar_introduccion():
    limpiar_frame()
    tk.Label(frame, text="Introducción", font=("Helvetica", 18, "bold")).pack(pady=20)
    intro = ("Los métodos numéricos son herramientas esenciales en diversas áreas de la ciencia, "
            "la ingeniería y la tecnología. Nos permiten obtener soluciones aproximadas a problemas "
            "matemáticos complejos que, en muchos casos, no tienen una solución analítica sencilla o exacta.\n\n"
            "Este programa te guiará a través de diversos métodos numéricos, organizados por temas para "
            "facilitar tu aprendizaje. Explorarás técnicas para:\n\n"
            "* Resolver ecuaciones no lineales: Encontrar las raíces de funciones complejas.\n"
            "* Resolver sistemas de ecuaciones lineales: Hallar los valores que satisfacen múltiples ecuaciones simultáneamente.\n"
            "* Interpolación: Estimar valores desconocidos a partir de un conjunto de datos conocidos.\n"
            "* Integración numérica: Calcular el valor aproximado de integrales definidas.\n\n"
            "A través de la visualización y la aplicación práctica, este programa te ayudará a comprender "
            "la lógica y el funcionamiento de estos poderosos métodos. ¡Prepárate para explorar el fascinante "
            "mundo de la aproximación numérica!")
    tk.Label(frame, text=intro, wraplength=400, justify="left").pack(pady=20)
    tk.Button(frame, text="Regresar", width=15, command=mostrar_portada).pack(side="left", padx=40, pady=20)
    tk.Button(frame, text="Siguiente", width=15, command=mostrar_menu_principal).pack(side="right", padx=40, pady=20)
    tk.Button(frame, text="Cerrar aplicación", width=30, command=root.destroy).pack(pady=10)

def mostrar_menu_principal():
    limpiar_frame()
    tk.Label(frame, text="Selecciona una Unidad", font=("Helvetica",16,"bold")).pack(pady=20)
    for unidad in ["UNIDAD 1", "UNIDAD 2", "UNIDAD 3"]:
        btn = tk.Button(frame, text=unidad, width=30, command=lambda u=unidad: mostrar_unidad(u))
        btn.pack(pady=10)
    tk.Button(frame, text="Regresar a Introducción", width=30, command=mostrar_introduccion).pack(pady=10)
    tk.Button(frame, text="Cerrar aplicación", width=30, command=root.destroy).pack(pady=10)

def mostrar_unidad(unidad):
    limpiar_frame()
    metodos_por_unidad = {
        "UNIDAD 1": [
            ("Punto Fijo", punto_fijo.Punto_Fijo),
            ("Newton Raphson", Newton_raphson.Newton_Raphson)
        ],
        "UNIDAD 2": [
            ("Lagrange", lagrange.ejecutar),
            ("Diferencias Divididas", diferencias_divididas.ejecutar),
            ("Mínimos Cuadrados", minimos_cuadrados.ejecutar)
        ],
        "UNIDAD 3": [
            ("Trapecio", trapecio.ejecutar),
            ("Simpson 1/3", simpson_1_3.ejecutar),
            ("Simpson 3/8", simpson_3_8.ejecutar)
        ]
    }

    tk.Label(frame, text=unidad, font=("Helvetica",16,"bold")).pack(pady=10)
    for nombre, funcion in metodos_por_unidad.get(unidad, []):
        btn = tk.Button(frame, text=nombre, width=30, command=lambda n=nombre, f=funcion: abrir_metodo(n, f))
        btn.pack(pady=5)

    tk.Button(frame, text="Regresar", width=30, command=mostrar_menu_principal).pack(pady=20)

def abrir_metodo(nombre, funcion):
    ventana = tk.Toplevel(root)
    ventana.title(nombre)
    centrar_ventana(ventana, 500, 600)
    descripcion = {
        "Punto Fijo": (
            "Método iterativo para encontrar raíces resolviendo x = g(x). "
            "Para funciones escalares, se usa la iteración directa. "
            "En sistemas no lineales, el método se extiende aplicando iterativamente "
            "las funciones vectoriales para cada variable, buscando convergencia "
            "del vector solución."
        ),
        "Newton Raphson": (
            "Método iterativo que encuentra raíces mediante aproximaciones usando "
            "la función y su derivada. Para funciones escalares se usa la derivada, "
            "y para sistemas no lineales se emplea la matriz Jacobiana para resolver "
            "un sistema lineal que actualiza el vector solución en cada iteración, "
            "logrando una convergencia rápida si la estimación inicial es adecuada."
        ),
        "Diferencias Divididas": (
            "El método de diferencias divididas es una técnica para construir un polinomio interpolador "
            "que pasa exactamente por un conjunto de puntos dados. Se basa en calcular incrementos de la función "
            "en puntos cercanos, organizándolos en una tabla de diferencias divididas que facilita el cálculo "
            "de los coeficientes del polinomio."
        ),
        "Lagrange": (
            "El método de interpolación de Lagrange es una forma directa de construir un polinomio que pasa por un "
            "conjunto de puntos sin necesidad de resolver sistemas de ecuaciones. Utiliza funciones base llamadas "
            "polinomios de Lagrange, cada uno de los cuales es cero en todos los puntos excepto en uno."
        ),
        "Mínimos Cuadrados": (
            "El método de mínimos cuadrados es una técnica estadística usada para ajustar una curva o línea a un conjunto "
            "de datos experimentales minimizando la suma de los cuadrados de las diferencias entre los valores observados "
            "y los valores predichos por el modelo."
        ),
        "Trapecio": (
            "El método del trapecio es una técnica sencilla para la integración numérica que aproxima el área bajo una curva "
            "dividiendo el intervalo en segmentos pequeños y calculando el área de trapecios entre los puntos."
        ),
        "Simpson 1/3": (
            "El método de Simpson 1/3 mejora la precisión respecto al método del trapecio al aproximar la función mediante "
            "polinomios cuadráticos. Usa coeficientes específicos que permiten calcular la integral con mayor exactitud."
        ),
        "Simpson 3/8": (
            "El método de Simpson 3/8 es una variante que utiliza polinomios cúbicos para aproximar la función "
            "en segmentos de tres subintervalos. Es útil cuando el número de puntos no es múltiplo de dos."
        )
    }
    tk.Label(ventana, text=descripcion.get(nombre, "No disponible."), wraplength=400, justify="left").pack(pady=10)
    tk.Button(ventana, text="Siguiente", command=lambda: [ventana.destroy(), funcion()]).pack(side="right", padx=20, pady=10)
    tk.Button(ventana, text="Regresar", command=ventana.destroy).pack(side="left", padx=20, pady=10)

def limpiar_frame():
    for widget in frame.winfo_children():
        widget.destroy()

# VENTANA PRINCIPAL

root = tk.Tk()
root.title("Portada - Métodos Numéricos")
centrar_ventana(root, 500, 600)

frame = tk.Frame(root)
frame.pack(pady=20)

mostrar_portada()

root.mainloop()
