import tkinter as tk
from tkinter import messagebox
import itertools

# Operadores soportados: ¬ (not), ∧ (and), ∨ (or), → (implica), ↔ (equivalencia)

def evaluar_expresion(expr, valores):
    # Reemplazar variables con sus valores
    for var, val in valores.items():
        expr = expr.replace(var, str(val))
    # Reemplazar operadores lógicos por sintaxis Python
    expr = expr.replace("¬", " not ")
    expr = expr.replace("∧", " and ")
    expr = expr.replace("∨", " or ")
    expr = expr.replace("→", "<= ")  # A → B equivale a (not A or B), simplificado con <=
    expr = expr.replace("↔", "==")   # Equivalencia
    try:
        return eval(expr)
    except Exception:
        return None

def generar_tabla(expr, variables):
    resultados = []
    for valores in itertools.product([False, True], repeat=len(variables)):
        asignacion = dict(zip(variables, valores))
        resultado = evaluar_expresion(expr, asignacion)
        resultados.append((asignacion, resultado))
    return resultados

def clasificar(resultados):
    valores = [res for _, res in resultados]
    if all(valores):
        return "Tautología"
    elif not any(valores):
        return "Contradicción"
    else:
        return "Contingencia"

def mostrar_tabla(expr, variables):
    resultados = generar_tabla(expr, variables)
    tipo = clasificar(resultados)

    tabla = f"Expresión: {expr}\n\n"
    tabla += " | ".join(variables) + " | Resultado\n"
    tabla += "-" * (len(variables) * 4 + 12) + "\n"
    for asignacion, resultado in resultados:
        fila = " | ".join("1" if asignacion[v] else "0" for v in variables)
        fila += " | " + ("1" if resultado else "0")
        tabla += fila + "\n"

    tabla += f"\nClasificación: {tipo}"
    messagebox.showinfo("Tabla de Verdad", tabla)

def agregar_simbolo(simbolo):
    entrada.insert(tk.END, simbolo)

def calcular():
    expr = entrada.get()
    variables = sorted(set([c for c in expr if c.isalpha()]))
    if not variables:
        messagebox.showerror("Error", "Debe ingresar al menos una variable.")
        return
    mostrar_tabla(expr, variables)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Calculadora de Tablas de Verdad")

entrada = tk.Entry(ventana, width=40, font=("Arial", 14))
entrada.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

botones = [
    ("A", "A"), ("B", "B"), ("C", "C"),
    ("¬", "¬"), ("∧", "∧"), ("∨", "∨"),
    ("→", "→"), ("↔", "↔"),
    ("(", "("), (")", ")"),
]

row, col = 1, 0
for texto, simbolo in botones:
    tk.Button(ventana, text=texto, width=5, height=2,
              command=lambda s=simbolo: agregar_simbolo(s)).grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 5:
        col = 0
        row += 1

tk.Button(ventana, text="Calcular", width=20, height=2, command=calcular).grid(row=row+1, column=0, columnspan=6, pady=10)

ventana.mainloop()

