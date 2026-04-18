import streamlit as st
import itertools
import pandas as pd

# Función para evaluar expresiones lógicas
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

# --- Interfaz Streamlit estilo calculadora ---
st.title("🧮 Calculadora de Tablas de Verdad")

# Estado de la expresión
if "expr" not in st.session_state:
    st.session_state.expr = ""

st.text_input("Expresión lógica", st.session_state.expr, key="expr_box")

# Botones estilo calculadora
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: 
    if st.button("A"): st.session_state.expr += "A"
with col2: 
    if st.button("B"): st.session_state.expr += "B"
with col3: 
    if st.button("C"): st.session_state.expr += "C"
with col4: 
    if st.button("¬"): st.session_state.expr += "¬"
with col5: 
    if st.button("∧"): st.session_state.expr += "∧"
with col6: 
    if st.button("∨"): st.session_state.expr += "∨"

col7, col8, col9, col10, col11, col12 = st.columns(6)
with col7: 
    if st.button("→"): st.session_state.expr += "→"
with col8: 
    if st.button("↔"): st.session_state.expr += "↔"
with col9: 
    if st.button("("): st.session_state.expr += "("
with col10: 
    if st.button(")"): st.session_state.expr += ")"
with col11: 
    if st.button("Borrar"): st.session_state.expr = ""
with col12: 
    if st.button("←"): st.session_state.expr = st.session_state.expr[:-1]

# Mostrar expresión actual
st.write("Expresión actual:", st.session_state.expr)

# Botón calcular
if st.button("Calcular"):
    expr = st.session_state.expr
    variables = sorted(set([c for c in expr if c.isalpha()]))
    if not variables:
        st.error("Debe ingresar al menos una variable.")
    else:
        resultados = generar_tabla(expr, variables)
        tipo = clasificar(resultados)

        # Construir tabla en formato DataFrame
        filas = []
        for asignacion, resultado in resultados:
            fila = {v: 1 if asignacion[v] else 0 for v in variables}
            fila["Resultado"] = 1 if resultado else 0
            filas.append(fila)

        df = pd.DataFrame(filas)

        st.subheader("Tabla de Verdad")
        st.table(df)

        st.success(f"Clasificación: {tipo}")

        # Botón para descargar como Excel
        excel_bytes = df.to_excel(index=False, engine="openpyxl")
        st.download_button(
            label="📥 Descargar tabla en Excel",
            data=excel_bytes,
            file_name="tabla_verdad.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
