
import pandas as pd
import numpy as np

def procesar_datos_megaline():
    """
    Carga, limpia y fusiona todos los DataFrames para el análisis.
    Retorna el DataFrame final procesado.
    """
    try:
        calls = pd.read_csv('datos/megaline_calls.csv')
        internet = pd.read_csv('datos/megaline_internet.csv')
        messages = pd.read_csv('datos/megaline_messages.csv')
        plans    = pd.read_csv('datos/megaline_plans.csv') 
        users    = pd.read_csv('datos/megaline_users.csv')

        # --- PREPROCESAMIENTO DE FECHAS Y EXTRACCIÓN DE MESES ---
        calls['call_date'] = pd.to_datetime(calls['call_date'])
        calls['month'] = calls['call_date'].dt.to_period('M') 

        messages['message_date'] = pd.to_datetime(messages['message_date'])
        messages['month'] = messages['message_date'].dt.to_period('M')

        internet['session_date'] = pd.to_datetime(internet['session_date'])
        internet['month'] = internet['session_date'].dt.to_period('M')

        
        # --- AGRUPACIONES Y UNIONES ---
        group_calls = calls.groupby(['user_id', 'month']).agg(
            call_count=('call_date', 'count'),
            total_minutes=('duration', 'sum')
        ).reset_index()

        group_messages = messages.groupby(['user_id', 'month']).agg(
            message_count=('message_date', 'count')
        ).reset_index()
        
        group_internet = internet.groupby(['user_id', 'month']).agg(
            compil_internet=('mb_used', 'sum')
        ).reset_index()

        # Fusionar datos de llamadas, mensajes e internet en un solo DataFrame
        monthly_data = pd.merge(group_calls, group_messages, on=['user_id', 'month'], how='outer')
        monthly_data = pd.merge(monthly_data, group_internet, on=['user_id', 'month'], how='outer')

        # --- APLICACIÓN DE fillna y astype(int) de forma más eficiente ---
        monthly_data = monthly_data.fillna(0)
        
        # Redondea y convierte a entero en un solo paso para las columnas relevantes
        monthly_data['total_minutes'] = np.ceil(monthly_data['total_minutes']).astype(int)
        monthly_data['compil_internet'] = np.ceil(monthly_data['compil_internet']).astype(int)
        monthly_data['call_count'] = monthly_data['call_count'].astype(int)
        monthly_data['message_count'] = monthly_data['message_count'].astype(int)
        
        # --- CONSTRUCCIÓN DE 'final_data' y cálculos extras ---
        union_data = pd.merge(monthly_data, users, on='user_id', how='outer')
        final_data = pd.merge(union_data, plans, left_on='plan_name', right_on='plan_name', how='left')
        
        # Renombrar columna para mayor claridad
        final_data = final_data.rename(columns={'plan_name': 'type_plan'})
        
        # Calcular extra_charges
        final_data['extra_minutes'] = (final_data['total_minutes'] - final_data['minutes_included']).clip(lower=0)
        final_data['extra_texts'] = (final_data['message_count'] - final_data['messages_included']).clip(lower=0)
        final_data['extra_data'] = (final_data['compil_internet'] - final_data['mb_per_month_included']).clip(lower=0)
        
        final_data['extra_charges'] = (final_data['extra_minutes'] * final_data['usd_per_minute'] +
                                       final_data['extra_texts'] * final_data['usd_per_message'] +
                                       final_data['extra_data'] * final_data['usd_per_gb'])

        final_data['month'] = final_data['month'].astype(str)

        print("¡Datos de Megaline procesados con éxito!")
        return final_data

    except FileNotFoundError as e:
        print(f"ERROR en limpieza.py: Archivo no encontrado. Detalles: {e}")
        return None
    except Exception as e:
        print(f"ERROR en limpieza.py: Ocurrió un error inesperado durante el procesamiento. Detalles: {e}")
        return None
    