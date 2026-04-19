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

# --- Interfaz Streamlit ---
st.title("🧮 Calculadora de Tablas de Verdad")

# Estado de la expresión
if "expr" not in st.session_state:
    st.session_state.expr = ""

# Display grande arriba (solo lectura, como calculadora)
st.markdown(f"## 📟 Expresión actual:\n`{st.session_state.expr}`")

# Botones estilo calculadora
col1, col2, col3, col4 = st.columns(4)
with col1: 
    if st.button("p"): st.session_state.expr += "p"
with col2: 
    if st.button("q"): st.session_state.expr += "q"
with col3: 
    if st.button("a"): st.session_state.expr += "a"
with col4: 
    if st.button("b"): st.session_state.expr += "b"

col5, col6, col7, col8 = st.columns(4)
with col5: 
    if st.button("¬"): st.session_state.expr += "¬"
with col6: 
    if st.button("∧"): st.session_state.expr += "∧"
with col7: 
    if st.button("∨"): st.session_state.expr += "∨"
with col8: 
    if st.button("→"): st.session_state.expr += "→"

col9, col10, col11, col12 = st.columns(4)
with col9: 
    if st.button("↔"): st.session_state.expr += "↔"
with col10: 
    if st.button("("): st.session_state.expr += "("
with col11: 
    if st.button(")"): st.session_state.expr += ")"
with col12: 
    if st.button("Borrar"): st.session_state.expr = ""

col13, col14 = st.columns(2)
with col13: 
    if st.button("←"): st.session_state.expr = st.session_state.expr[:-1]
with col14: 
    if st.button("Calcular"):
        expr = st.session_state.expr
        variables = sorted(set([c for c in expr if c.isalpha()]))
        if not variables:
            st.error("Debe ingresar al menos una variable.")
        else:
            resultados = generar_tabla(expr, variables)
            tipo = clasificar(resultados)

            # Construir tabla en DataFrame
            filas = []
            for asignacion, resultado in resultados:
                fila = {v: 1 if asignacion[v] else 0 for v in variables}
                fila["Resultado"] = 1 if resultado else 0
                filas.append(fila)

            df = pd.DataFrame(filas)

            st.subheader("Tabla de Verdad")
            st.dataframe(df)  # más rápido que st.table

            st.success(f"Clasificación: {tipo}")

            # Crear archivo CSV
            csv_bytes = df.to_csv(index=False).encode("utf-8")

            # Botón para descargar CSV
            st.download_button(
                label="📥 Descargar tabla en CSV",
                data=csv_bytes,
                file_name="tabla_verdad.csv",
                mime="text/csv"
            )
