
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Se importa la función del archivo 'limpieza.py'
from limpieza import procesar_datos_megaline

# --- 
@st.cache_data
def load_data():
    """Carga los datos limpios y procesados."""
    return procesar_datos_megaline()

# --- 
st.set_page_config(
    page_title="📱 Análisis del Uso del Tipo de Plan de Llamadas de MEGALINE ",
    layout="wide"
)

st.title("Visualización Dashboard")
st.markdown("### 📊 Visualización de las diferentes Dashboard del Proyecto")

# 1. Introducción
with st.expander("Introducción", expanded=True):
    st.markdown("""
    Esta aplicación demuestra el análisis del uso de dos tipos de planes de llamadas:
    * El promedio de llamadas 
    * El uso de minutos
    * """)

# --- Llamar a la función CACHEADA para obtener los datos limpios ---
final_data = load_data()

# Si la función devolvió datos (no un error), entonces muestra los gráficos
if final_data is not None:
    st.markdown("---")
    st.title('Análisis de Llamadas por Plan')
    st.markdown("---")

    # Calcula el promedio de llamadas y lo pivota
    average_calls = final_data.groupby(['type_plan', 'month'])['call_count'].mean().reset_index()
    pivot_data = average_calls.pivot(index='month', columns='type_plan', values='call_count')

    # Crea el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_data.plot(kind='bar', ax=ax)

    # Configura el gráfico
    plt.title("Comparación de Promedio Mensual de Llamadas por Plan")
    plt.xlabel("Mes")
    plt.ylabel("Promedio de Llamadas")
    plt.legend(title="Planes")

    # --- Muestra el gráfico en la aplicación de Streamlit ---
    st.pyplot(fig)

    st.subheader("Datos de Promedio de Llamadas")
    st.dataframe(pivot_data)
    