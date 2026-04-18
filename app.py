import streamlit as st
import itertools

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

# Interfaz Streamlit
st.title("🧮 Calculadora de Tablas de Verdad")

st.write("Ingresa una expresión lógica usando las variables y operadores disponibles:")

# Entrada de expresión
expr = st.text_input("Expresión lógica", "(A ∨ B) → C")

if st.button("Calcular"):
    variables = sorted(set([c for c in expr if c.isalpha()]))
    if not variables:
        st.error("Debe ingresar al menos una variable.")
    else:
        resultados = generar_tabla(expr, variables)
        tipo = clasificar(resultados)

        # Mostrar tabla
        st.subheader("Tabla de Verdad")
        tabla = []
        for asignacion, resultado in resultados:
            fila = [1 if asignacion[v] else 0 for v in variables]
            fila.append(1 if resultado else 0)
            tabla.append(fila)

        st.table([variables + ["Resultado"]] + tabla)

        # Mostrar clasificación
        st.success(f"Clasificación: {tipo}")
