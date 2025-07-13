
import pandas as pd
import numpy as np

def procesar_datos():
    """
    Carga, limpia y fusiona todos los DataFrames para el análisis.
    Retorna el DataFrame final procesado.
    """
    try:
        
        calls    = pd.read_csv('datos/megaline_calls.csv')
        internet = pd.read_csv('datos/megaline_internet.csv')
        messages = pd.read_csv('datos/megaline_messages.csv')
        plans    = pd.read_csv('datos/megaline_plans.csv') 
        users    = pd.read_csv('datos/megaline_users.csv')

        
        calls['call_date'] = pd.to_datetime(calls['call_date'])
        calls['month'] = calls['call_date'].dt.to_period('M') 

        messages['message_date'] = pd.to_datetime(messages['message_date'])
        messages['month'] = messages['message_date'].dt.to_period('M')

        internet['session_date'] = pd.to_datetime(internet['session_date'])
        internet['month'] = internet['session_date'].dt.to_period('M')

        users['reg_date'] = pd.to_datetime(users['reg_date'])
        users['churn_date'] = pd.to_datetime(users['churn_date'])
        users['period'] = users['reg_date'].dt.to_period('M')

        
        data_group = users.groupby(['user_id', 'period']).agg({'first_name':'first','last_name': 'first','age': 'first', 'plan': 'first',}).reset_index()

        group_calls = calls.groupby(['user_id', 'month']).agg(call_count=('call_date','count')).reset_index()
        group_minutes = calls.groupby(['user_id', 'month']).agg(total_minutes=('duration', 'sum')).reset_index()
        merged_data = pd.merge(group_calls, group_minutes, on=['user_id', 'month'],how='outer')

        group_messages = messages.groupby(['user_id', 'month']).agg(message_count=('message_date', 'count')).reset_index()
        merged_data_1 = pd.merge(merged_data, group_messages, on=['user_id', 'month'],how='outer')

        group_internet = internet.groupby(['user_id', 'month']).agg(compil_internet = ('mb_used', 'sum')).reset_index()
        merged_data_2 = pd.merge(merged_data_1, group_internet, on=['user_id','month'],how='outer')

        merged_data_2 = merged_data_2.fillna(0)
        new_columns = ['call_count', 'total_minutes', 'message_count', 'compil_internet']
        for col in new_columns:
            merged_data_2[col] = np.ceil(merged_data_2[col]).astype(int)

        
        user_1 = users[['user_id','plan']]
        union_data = pd.merge(merged_data_2, user_1, on='user_id', how='outer')

        final_data = pd.merge(union_data, plans, left_on='plan', right_on='plan_name', how='left')

        
        final_data['type_plan'] = final_data.apply(lambda row: row['plan']
                                                 if pd.notnull(row['plan']) else row['plan_name'], axis=1)

        final_data.drop(columns=['plan', 'plan_name'], inplace=True)

        
        final_data['extra_calls'] = (final_data['total_minutes'] - final_data['minutes_included']).clip(lower=0)
        final_data['extra_texts'] = (final_data['message_count'] - final_data['messages_included']).clip(lower=0)
        final_data['extra_dates'] = (final_data['compil_internet'] - final_data['mb_per_month_included']).clip(lower=0)

        final_data['extra_charges'] = (final_data['extra_calls'] * final_data['usd_per_minute'] +
                                       final_data['extra_texts'] * final_data['usd_per_message'] +
                                       final_data['extra_dates'] * final_data['usd_per_gb'])

        print("¡Datos de datos procesados con éxito!")
        return final_data

    except FileNotFoundError as e:
        print(f"ERROR en limpieza.py: Archivo no encontrado. Detalles: {e}")
        return None
    except Exception as e:
        print(f"ERROR en limpieza.py: Ocurrió un error inesperado durante el procesamiento. Detalles: {e}")
        return None
    