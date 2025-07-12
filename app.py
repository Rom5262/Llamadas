
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Se importa la función del archivo 'limpieza.py'
from limpieza import procesar_datos

# --- 
@st.cache_data
def load_data():
    """Carga los datos limpios y procesados."""
    return procesar_datos()

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

# --- Llamar a la función  para obtener los datos limpios ---
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
    fig, ax = plt.subplots(figsize=(8,6))
    pivot_data.plot(kind='bar', ax=ax)

    # Configura el gráfico
    plt.title("Comparación de Promedio Mensual de Llamadas por Plan")
    plt.xlabel("Mes")
    plt.ylabel("Promedio de Llamadas")
    plt.legend(title="Planes")

    # ---                                       ---
    st.pyplot(fig)


# ---  ---
monthly_minutes = final_data.groupby(['type_plan', 'month'])['total_minutes'].mean().reset_index()
pivot_minutes = monthly_minutes.pivot(index='month', columns='type_plan', values='total_minutes')


# --- Contenedor de Streamlit para los gráficos ---
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico Histograma")
        # "
        
        # Crear la figura para el primer gráfico (Histograma)
        fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
        pivot_minutes.plot(kind='hist', ax=ax_hist)
        
        ax_hist.set_title("Comparación de Minutos Mensuales por Plan")
        ax_hist.set_xlabel("Mes")
        ax_hist.set_ylabel("Total de Minutos")
        ax_hist.legend(title="Planes")
        
        plt.tight_layout()
        st.pyplot(fig_hist) # Mostrar el primer gráfico en la primera columna

    with col2:
        st.subheader("Gráfico de Barras")
        

        # Crear la figura para el segundo gráfico (Barras)
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        pivot_minutes.plot(kind='bar', ax=ax_bar)

        ax_bar.set_title("Comparación de Minutos Mensuales por Plan")
        ax_bar.set_xlabel("Mes")
        ax_bar.set_ylabel("Total de Minutos")
        ax_bar.legend(title="Planes")
        
        plt.tight_layout()
        st.pyplot(fig_bar) # Mostrar el segundo gráfico en la segunda columna



# --- Diseño de la página con Streamlit ---
st.markdown("---")
st.title('Análisis de Media y Varianza de la duración de Llamadas')
st.markdown("---")


mean_calls = final_data['call_count'].mean()
var_calls = final_data['call_count'].var()

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(['Media', 'Varianza'], [mean_calls, var_calls], color=['skyblue', 'lightcoral'])
ax.set_title('Media y Varianza de la Cantidad de Llamadas')
ax.set_ylabel('Valores')
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Etiquetas de valor encima de las barras (opcional pero estético)
for i, v in enumerate([mean_calls, var_calls]):
    ax.text(i, v * 0.5, f'{v:.2f}', ha='center', color='black', fontweight='bold')

plt.tight_layout()

# --- Mostrar en Streamlit ---
st.pyplot(fig)

