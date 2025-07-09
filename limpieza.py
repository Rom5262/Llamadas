import pandas as pd
import numpy as np # Importa numpy si lo usas en tu limpieza o transformaciones

def cargar_y_limpiar_datos():
    """
    Carga los archivos CSV de Megaline desde la carpeta 'datos/',
    realiza las uniones y el preprocesamiento necesario
    para obtener el DataFrame final_data.
    """
    try:
        # --- 1. CARGAR LOS DATASET INDIVIDUALES ---
        # Asegúrate de que las rutas a los CSVs sean correctas: 'datos/nombre_del_archivo.csv'
        calls_df = pd.read_csv('datos/megaline_calls.csv')
        internet_df = pd.read_csv('datos/megaline_internet.csv')
        messages_df = pd.read_csv('datos/megaline_messages.csv')
        plans_df = pd.read_csv('datos/megaline_plans.csv')
        users_df = pd.read_csv('datos/megaline_users.csv')

        

        # Convertir la columna 'churn_date' en users_df a datetime y llenar NaN para usuarios activos
        users_df['churn_date'] = pd.to_datetime(users_df['churn_date'], errors='coerce')

        # Convertir 'reg_date' a datetime
        users_df['reg_date'] = pd.to_datetime(users_df['reg_date'])

        # Asegurar que 'call_date' y 'session_date' sean datetime y extraer el mes
        calls_df['call_date'] = pd.to_datetime(calls_df['call_date'])
        calls_df['month'] = calls_df['call_date'].dt.month

        internet_df['session_date'] = pd.to_datetime(internet_df['session_date'])
        internet_df['month'] = internet_df['session_date'].dt.month

        messages_df['message_date'] = pd.to_datetime(messages_df['message_date'])
        messages_df['month'] = messages_df['message_date'].dt.month

        # Renombrar columnas para evitar conflictos en las uniones y tener nombres más claros
        plans_df = plans_df.rename(columns={'messages_included': 'plan_messages_included',
                                            'mb_per_month_included': 'plan_mb_per_month_included',
                                            'usd_per_gb': 'plan_usd_per_gb',
                                            'usd_per_message': 'plan_usd_per_message',
                                            'usd_per_minute': 'plan_usd_per_minute'})

        # Unir los DataFrames
        df_merged = pd.merge(users_df, plans_df, on='plan_name', how='left')
        df_merged = pd.merge(df_merged, calls_df.groupby(['user_id', 'month'])['call_duration'].sum().reset_index(),
                             on=['user_id', 'month'], how='left')
        df_merged = pd.merge(df_merged, internet_df.groupby(['user_id', 'month'])['mb_used'].sum().reset_index(),
                             on=['user_id', 'month'], how='left')
        df_merged = pd.merge(df_merged, messages_df.groupby(['user_id', 'month']).size().reset_index(name='message_count'),
                             on=['user_id', 'month'], how='left')

        # Manejar NaN después de las uniones (rellenar con 0 donde no hubo actividad)
        df_merged['call_duration'] = df_merged['call_duration'].fillna(0)
        df_merged['mb_used'] = df_merged['mb_used'].fillna(0)
        df_merged['message_count'] = df_merged['message_count'].fillna(0)

       
        calls_per_month = calls_df.groupby(['user_id', 'month']).agg(call_count=('id', 'count')).reset_index()
        df_merged = pd.merge(df_merged, calls_per_month, on=['user_id', 'month'], how='left')
        df_merged['call_count'] = df_merged['call_count'].fillna(0)


        # Renombrar 'plan_name' a 'type_plan' si tu gráfica usa 'type_plan'
        df_merged = df_merged.rename(columns={'plan_name': 'type_plan'})

       

        final_data = df_merged # Este es tu DataFrame final_data

        return final_data

    except FileNotFoundError as e:
        # Este error se imprimirá en los logs de Render o en tu terminal local si un archivo no se encuentra
        print(f"Error: Uno o más archivos de datos no se encontraron en 'datos/'. Detalles: {e}")
        return None # Devuelve None si no se pudieron cargar los datos
    except Exception as e:
        # Captura cualquier otro error durante el preprocesamiento
        print(f"Error inesperado durante la carga y limpieza de datos: {e}")
        return None
    