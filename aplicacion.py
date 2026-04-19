import streamlit as st
import itertools
import pandas as pd

# --- Funciones de lógica proposicional ---
def evaluar_expresion(expr, valores):
    for var, val in valores.items():
        expr = expr.replace(var, str(val))
    expr = expr.replace("¬", " not ")
    expr = expr.replace("∧", " and ")
    expr = expr.replace("∨", " or ")
    expr = expr.replace("→", "<= ")   # A → B equivale a (not A or B), simplificado con <=
    expr = expr.replace("↔", "==")    # Equivalencia
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

# --- Funciones para callbacks ---
def add_symbol(symbol):
    st.session_state.expr += symbol

def clear_expr():
    st.session_state.expr = ""

def backspace():
    st.session_state.expr = st.session_state.expr[:-1]

def calcular():
    expr = st.session_state.expr
    variables = sorted(set([c for c in expr if c.isalpha()]))
    if not variables:
        st.session_state.resultados = None
        st.session_state.tipo = None
        return
    resultados = generar_tabla(expr, variables)
    tipo = clasificar(resultados)

    # Construir tabla en DataFrame
    filas = []
    for asignacion, resultado in resultados:
        fila = {v: 1 if asignacion[v] else 0 for v in variables}
