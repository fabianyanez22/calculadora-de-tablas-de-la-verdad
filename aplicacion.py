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
        fila["Resultado"] = 1 if resultado else 0
        filas.append(fila)

    st.session_state.resultados = pd.DataFrame(filas)
    st.session_state.tipo = tipo

# --- Interfaz Streamlit ---
st.title("🧮 Calculadora de Tablas de Verdad")

if "expr" not in st.session_state:
    st.session_state.expr = ""
if "resultados" not in st.session_state:
    st.session_state.resultados = None
if "tipo" not in st.session_state:
    st.session_state.tipo = None

# Display grande arriba
st.markdown(f"## 📟 Expresión actual:\n`{st.session_state.expr}`")

# Botones con callbacks
col1, col2, col3, col4 = st.columns(4)
with col1: st.button("p", on_click=add_symbol, args=("p",))
with col2: st.button("q", on_click=add_symbol, args=("q",))
with col3: st.button("a", on_click=add_symbol, args=("a",))
with col4: st.button("b", on_click=add_symbol, args=("b",))

col5, col6, col7, col8 = st.columns(4)
with col5: st.button("¬", on_click=add_symbol, args=("¬",))
with col6: st.button("∧", on_click=add_symbol, args=("∧",))
with col7: st.button("∨", on_click=add_symbol, args=("∨",))
with col8: st.button("→", on_click=add_symbol, args=("→",))

col9, col10, col11, col12 = st.columns(4)
with col9: st.button("↔", on_click=add_symbol, args=("↔",))
with col10: st.button("(", on_click=add_symbol, args=("(",))
with col11: st.button(")", on_click=add_symbol, args=(")",))
with col12: st.button("Borrar", on_click=clear_expr)

col13, col14 = st.columns(2)
with col13: st.button("←", on_click=backspace)
with col14: st.button("Calcular", on_click=calcular)

# --- Mostrar resultados al final ---
if st.session_state.resultados is not None:
    st.subheader("Tabla de Verdad")
    st.dataframe(st.session_state.resultados)

    st.success(f"Clasificación: {st.session_state.tipo}")

    # Crear archivo CSV
    csv_bytes = st.session_state.resultados.to_csv(index=False).encode("utf-8")

    # Botón para descargar CSV
    st.download_button(
        label="📥 Descargar tabla en CSV",
        data=csv_bytes,
        file_name="tabla_verdad.csv",
        mime="text/csv"
    )
