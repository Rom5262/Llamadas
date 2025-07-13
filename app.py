
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza import procesar_datos

@st.cache_data
def load_data():
    """Carga los datos limpios y procesados."""
    return procesar_datos()

st.set_page_config(
    page_title="📱 Análisis del Uso del Tipo de Servicio de Plan de Llamadas de MEGALINE ",
    layout="wide")

st.title("Visualización Dashboard")
st.markdown("### 📊 Visualización de las diferentes Dashboard del Proyecto")


with st.expander("Introducción", expanded=True):
    st.markdown("""
    Esta aplicación demuestra el análisis del uso de dos tipos de planes de Servicio Otorgado por MEGALINE:
    * El promedio de llamadas 
    * El uso de minutos
    * El Analisis de la Media,la Varianza y la Desviación Estandar de La Duración de las Llamadas 
    * El Analisis de Llamadas por Plan
    * El Analisis de Mensajes por Cada Plan
    * El Analisis de La Cantidad de Trafico de Internet Consumido por Cada Plan
    * """)

final_data = load_data()

st.markdown("---")
st.title('LLAMADAS')    
st.markdown("---")

if final_data is not None:
    st.markdown("---")
    st.title('Análisis de Llamadas por Plan')
    st.markdown("---")

    average_calls = final_data.groupby(['type_plan', 'month'])['call_count'].mean().reset_index()
    pivot_data = average_calls.pivot(index='month', columns='type_plan', values='call_count')

    fig, ax = plt.subplots(figsize=(8,6))
    pivot_data.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)

    plt.title("Comparación de Promedio Mensual de Llamadas por Plan")
    plt.xlabel("Mes")
    plt.ylabel("Promedio de Llamadas")
    plt.legend(title="Planes")

    # ---                                       ---
    st.pyplot(fig)


st.markdown("---")
st.title('Análisis de Minutos Mensuales Para Cada Plan')
st.markdown("---")

monthly_minutes = final_data.groupby(['type_plan', 'month'])['total_minutes'].mean().reset_index()
pivot_minutes = monthly_minutes.pivot(index='month', columns='type_plan', values='total_minutes')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico Histograma")
        # "
        
        # Crear la figura para el primer gráfico (Histograma)
        fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
        pivot_minutes.plot(kind='hist', ax=ax_hist)
        plt.xticks(rotation=45)
        
        ax_hist.set_title("Comparación de Minutos Mensuales por Plan")
        ax_hist.set_xlabel("Mes")
        ax_hist.set_ylabel("Total de Minutos")
        ax_hist.legend(title="Planes")
        
        plt.tight_layout()
        st.pyplot(fig_hist) 

    with col2:
        st.subheader("Gráfico de Barras")
        

        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        pivot_minutes.plot(kind='bar', ax=ax_bar)
        plt.xticks(rotation=45)

        ax_bar.set_title("Comparación de Minutos Mensuales por Plan")
        ax_bar.set_xlabel("Mes")
        ax_bar.set_ylabel("Total de Minutos")
        ax_bar.legend(title="Planes")
        
        plt.tight_layout()
        st.pyplot(fig_bar) 


st.markdown("---")
st.title('Análisis de Media, Varianza y Desviación Estandar de la duración de Llamadas')
st.markdown("---")

mean_calls = final_data['call_count'].mean()
var_calls = final_data['call_count'].var()
std_dev_calls = final_data['call_count'].std() 

valores = [mean_calls, var_calls, std_dev_calls]
etiquetas = ['Media', 'Varianza', 'Desv. Estándar']
colores = ['skyblue', 'lightcoral', 'lightgreen']

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(etiquetas, valores, color=colores)
plt.xticks(rotation=0)
ax.set_title('Media, Varianza y Desviación Estándar de las Llamadas')
ax.set_ylabel('Valores')
ax.grid(axis='y', linestyle='--', alpha=0.5)

for i, v in enumerate(valores):
    ax.text(i, v + 0.5, f'{v:.2f}', ha='center', color='black', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)

st.title("Análisis de Llamadas por Plan")
st.write("Comparación de la distribución de llamadas mensuales.")

with st.container():
    col1, col2 = st.columns(2)
    
     
with col1:
        st.subheader("Diagrama de Caja")

        
        fig_box, ax_box = plt.subplots(figsize=(8, 6))

        final_data.plot(
            kind='box',
            column='call_count',
            by='type_plan',
            grid=False,
            ax=ax_box  
        )

        ax_box.set_title("Distribución de Llamadas Mensual por Tipo de Plan")
        ax_box.set_xlabel("Tipo de Plan")
        ax_box.set_ylabel("Llamadas por Mes")
        ax_box.legend(title="Planes")
        
        plt.tight_layout()
        st.pyplot(fig_box)

with col2:
        st.subheader("Diagrama Tipo Violín")
        fig_violin, ax_violin = plt.subplots(figsize=(8, 6))

        sns.violinplot(
            x='type_plan',
            y='call_count',
            data=final_data,
            ax=ax_violin  
        )
        ax_violin.set_title("Distribución de Llamadas Mensual por Tipo de Plan")
        ax_violin.set_xlabel("Tipo de Plan")
        ax_violin.set_ylabel("Llamadas por Mes")
        
        plt.tight_layout()
        st.pyplot(fig_violin) 

        st.markdown("---")
        st.title('MENSAJES')    
        st.markdown("---")

number_messages = final_data.groupby(['type_plan', 'month'])['message_count'].mean().reset_index()
pivot_messages = number_messages.pivot(index='month', columns='type_plan', values='message_count')

st.title("Análisis de Mensajes por Plan")
st.write("Comparación de Mensajes por Mes.")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gráfico de Barras")
        
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        pivot_messages.plot(kind='bar', ax=ax_bar)
        
        plt.xticks(rotation=45)
        ax_bar.set_title("Comparación de Mensajes por Mes")
        ax_bar.set_xlabel("Mes")
        ax_bar.set_ylabel("Número de Mensajes")
        ax_bar.legend(title="Planes")
        plt.tight_layout()
        
        st.pyplot(fig_bar)

    with col2:
        st.subheader("Gráfico de Líneas")
        
        fig_lin, ax_lin = plt.subplots(figsize=(10, 6))
        
        pivot_messages.plot(kind='line', ax=ax_lin, marker='o') 
        
        plt.xticks(rotation=45)
        
        ax_lin.set_title("Comparación de Mensajes por Mes")
        ax_lin.set_xlabel("Mes")
        ax_lin.set_ylabel("Número de Mensajes")
        ax_lin.legend(title="Planes")
        plt.tight_layout()
        
        st.pyplot(fig_lin)

        st.markdown("---")
        st.title('INTERNET')    
        st.markdown("---")

internet_traffic = final_data.groupby(['type_plan', 'month'])['compil_internet'].mean().reset_index()
pivot_internet = internet_traffic.pivot(index='month', columns='type_plan', values='compil_internet')

st.title("Análisis de Internet Consumido por Cada Plan")
st.write("Comparación de Internet Consumido por Mes.")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gráfico de Líneas")
        
        fig_lin, ax_lin = plt.subplots(figsize=(10, 6))
        
        pivot_internet.plot(kind='line', ax=ax_lin, marker='o') 
        
        plt.xticks(rotation=45)
        
        ax_lin.set_title("Comparación de Internet Consumido por Mes")
        ax_lin.set_xlabel("Mes")
        ax_lin.set_ylabel("Internet")
        ax_lin.legend(title="Planes")
        plt.tight_layout()
        
        st.pyplot(fig_lin)

    with col2:
        st.subheader("Gráfico de Barras")
        
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        pivot_internet.plot(kind='bar', ax=ax_bar)
        
        plt.xticks(rotation=45)
        ax_bar.set_title("Comparación de Internet Consumido por Mes")
        ax_bar.set_xlabel("Mes")
        ax_bar.set_ylabel("Internet")
        ax_bar.legend(title="Planes")
        plt.tight_layout()
        
        st.pyplot(fig_bar)

average_internet_use = final_data.groupby(['type_plan', 'month'])['compil_internet'].sum().reset_index()
pivot_internet_sum = average_internet_use.pivot(index='month', columns='type_plan', values='compil_internet')

st.title("Análisis del Promedio Mensual de Uso del Internet por Cada Plan")
st.write("Comparación del Promedio Mensual.")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gráfico de Líneas")
        
        fig_lin, ax_lin = plt.subplots(figsize=(10, 6))
        
        pivot_internet_sum.plot(kind='line', ax=ax_lin, marker='o') 
        
        plt.xticks(rotation=45)
        
        ax_lin.set_title("Comparación de Promedio Mensual de Uso Internet")
        ax_lin.set_xlabel("Mes")
        ax_lin.set_ylabel("Promedio del Uso de Internet")
        ax_lin.legend(title="Planes")
        plt.tight_layout()
        
        st.pyplot(fig_lin)

    with col2:
        st.subheader("Gráfico de Barras")
        
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        pivot_internet_sum.plot(kind='bar', ax=ax_bar)
        
        plt.xticks(rotation=45)
        ax_bar.set_title("Comparación de Promedio Mensual de Uso Internet")
        ax_bar.set_xlabel("Mes")
        ax_bar.set_ylabel("Promedio del Uso de Internet")
        ax_bar.legend(title="Planes")
        plt.tight_layout()
        
        st.pyplot(fig_bar)

       


