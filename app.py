import streamlit as st
import matplotlib.pyplot as plt
# Importa la función desde tu archivo limpieza.py
from limpieza import cargar_y_limpiar_datos

# Configuración de la página de Streamlit (opcional, pero buena práctica)
st.set_page_config(layout="wide") # Hace que el contenido ocupe todo el ancho disponible

st.title("Análisis de Llamadas del Proyecto Megaline")
st.header("Comparación de Promedio Mensual de Llamadas por Plan")

# --- 1. CARGAR DATOS LIMPIOS ---
# Llama a la función de tu archivo limpieza.py para obtener el DataFrame final_data
final_data = cargar_y_limpiar_datos()

# Verifica si los datos se cargaron correctamente
if final_data is not None:
    # --- 2. VERIFICACIÓN DE COLUMNAS (MUY IMPORTANTE) ---
    # Asegúrate de que las columnas necesarias para tu gráfica existan en final_data
    required_columns = ['type_plan', 'month', 'call_count']
    if not all(col in final_data.columns for col in required_columns):
        st.error(f"Error: No se encontraron una o más de las columnas requeridas ({', '.join(required_columns)}) en tus datos limpios.")
        st.write("Columnas disponibles:", final_data.columns.tolist())
        st.stop() # Detiene la ejecución si faltan columnas críticas
    else:
        # --- 3. CÓDIGO DE GRAFICACIÓN (TU CÓDIGO ORIGINAL ADAPTADO) ---
        # Calcula el promedio mensual de llamadas por plan
        average_calls = final_data.groupby(['type_plan', 'month'])['call_count'].mean().reset_index()

        # Pivotea los datos para el gráfico de barras
        pivot_data = average_calls.pivot(index='month', columns='type_plan', values='call_count')

        # Crea la figura y los ejes de Matplotlib
        fig, ax = plt.subplots(figsize=(12, 7)) # Aumenta un poco el tamaño para mejor visualización
        pivot_data.plot(kind='bar', ax=ax, rot=45) # Gira las etiquetas del eje x si son largas

        # Configura títulos y etiquetas
        ax.set_title("Comparación de Promedio Mensual de llamadas por Plan", fontsize=16)
        ax.set_xlabel("Mes", fontsize=12)
        ax.set_ylabel("Promedio de Llamadas", fontsize=12)
        ax.legend(title="Planes", title_fontsize='13', fontsize='11')
        plt.tight_layout() # Ajusta el diseño para evitar superposiciones

        # Muestra la gráfica en la aplicación Streamlit
        st.pyplot(fig)

        # Cierra la figura para liberar memoria, buena práctica
        plt.close(fig)

        st.write("---")
        st.write("Esta gráfica visualiza el promedio de llamadas realizadas por los usuarios de cada plan (Smart y Ultra) a lo largo de los meses. Permite identificar tendencias estacionales o diferencias consistentes en el uso de llamadas entre los planes.")
        st.write("Datos procesados desde los archivos CSV de Megaline.")

else:
    # Mensaje de error si cargar_y_limpiar_datos() devolvió None
    st.error("No se pudieron cargar o preparar los datos para el análisis. Por favor, revisa el archivo `limpieza.py` y asegúrate de que los archivos de datos estén en la carpeta `datos/` y su lógica de procesamiento sea correcta.")
    st.write("---")
    st.write("Posibles causas:")
    st.write("- Archivos CSV no encontrados en la carpeta `datos/`.")
    st.write("- Errores en la lógica de procesamiento dentro de `limpieza.py`.")
    st.write("- Problemas de permisos o acceso a archivos en el entorno de despliegue.")
    