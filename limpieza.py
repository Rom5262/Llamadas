
import pandas as pd
import numpy as np

def cargar_y_limpiar_datos():
    """
    Carga los archivos CSV de Megaline desde la carpeta 'datos/',
    realiza las uniones y el preprocesamiento necesario
    para obtener el DataFrame final_data.
    """
    try:
        print("DEBUG: Iniciando cargar_y_limpiar_datos()")

        # --- 1. CARGAR LOS DATASET INDIVIDUALES ---
        calls_df = pd.read_csv('datos/megaline_calls.csv')
        internet_df = pd.read_csv('datos/megaline_internet.csv')
        messages_df = pd.read_csv('datos/megaline_messages.csv')
        plans_df = pd.read_csv('datos/megaline_plans.csv') # plans_df original
        users_df = pd.read_csv('datos/megaline_users.csv') # users_df original

        print("DEBUG: CSVs cargados.")
        print(f"DEBUG: calls_df shape: {calls_df.shape}")
        print(f"DEBUG: users_df shape: {users_df.shape}")
        print(f"DEBUG: plans_df shape: {plans_df.shape}")


        # --- 2. PREPROCESAMIENTO DE FECHAS Y EXTRACCIÓN DE MESES (como en tu Jupyter) ---
        calls_df['call_date'] = pd.to_datetime(calls_df['call_date'])
        calls_df['month'] = calls_df['call_date'].dt.to_period('M') # Usando to_period('M') como tú

        messages_df['message_date'] = pd.to_datetime(messages_df['message_date'])
        messages_df['month'] = messages_df['message_date'].dt.to_period('M')

        internet_df['session_date'] = pd.to_datetime(internet_df['session_date'])
        internet_df['month'] = internet_df['session_date'].dt.to_period('M')

        print("DEBUG: Fechas procesadas y meses extraídos con to_period('M').")


        # --- 3. AGRUPACIONES Y UNIONES PARA CONSTRUIR 'merged_data_2' (como en tu Jupyter) ---

        group_calls = calls_df.groupby(['user_id', 'month']).agg(call_count=('call_date', 'count')).reset_index()
        print(f"DEBUG: group_calls head:\n{group_calls.head()}")

        group_minutes = calls_df.groupby(['user_id', 'month']).agg(total_minutes=('duration', 'sum')).reset_index()
        print(f"DEBUG: group_minutes head:\n{group_minutes.head()}")

        merged_data = pd.merge(group_calls, group_minutes, on=['user_id', 'month'], how='outer')
        print(f"DEBUG: merged_data head:\n{merged_data.head()}")


        group_messages = messages_df.groupby(['user_id', 'month']).agg(message_count=('message_date', 'count')).reset_index()
        print(f"DEBUG: group_messages head:\n{group_messages.head()}")

        merged_data_1 = pd.merge(merged_data, group_messages, on=['user_id', 'month'], how='outer')
        print(f"DEBUG: merged_data_1 head:\n{merged_data_1.head()}")


        group_internet = internet_df.groupby(['user_id', 'month']).agg(compil_internet =('mb_used', 'sum')).reset_index()
        print(f"DEBUG: group_internet head:\n{group_internet.head()}")

        merged_data_2 = pd.merge(merged_data_1, group_internet, on=['user_id','month'], how='outer')
        print(f"DEBUG: merged_data_2 head:\n{merged_data_2.head()}")
        print(f"DEBUG: Columnas de merged_data_2: {merged_data_2.columns.tolist()}")

        # --- 3.1 APLICACIÓN DE fillna, ceil, astype(int) como tú lo indicaste ---
        new_columns = ['call_count', 'total_minutes', 'message_count', 'compil_internet']
        for col in new_columns:
            if col in merged_data_2.columns: # Aseguramos que la columna exista antes de procesarla
                merged_data_2[col] = merged_data_2[col].fillna(0).apply(np.ceil).astype(int)
            else:
                print(f"WARNING: Columna '{col}' no encontrada en merged_data_2 para fillna/ceil/astype. Puede ser un problema.")
        print("DEBUG: NaNs rellenados, redondeados hacia arriba y convertidos a int en merged_data_2.")
        merged_data_2_filled = merged_data_2 # Ahora merged_data_2 ya tiene los valores procesados


        # --- 4. CONSTRUCCIÓN DE 'union_data' (como en tu Jupyter) ---
        user_1 = users_df[['user_id','plan_name']].rename(columns={'plan_name': 'plan'})
        print(f"DEBUG: user_1 head:\n{user_1.head()}")

        union_data = pd.merge(merged_data_2_filled, user_1, on='user_id', how='outer')
        print(f"DEBUG: union_data head:\n{union_data.head()}")
        print(f"DEBUG: Columnas de union_data: {union_data.columns.tolist()}")

        # --- 5. TU CÓDIGO PROPORCIONADO PARA CONSTRUIR 'final_data' y cálculos extras ---
        plans_for_merge = plans_df.copy()

        final_data = pd.merge(union_data, plans_for_merge, left_on='plan', right_on='plan_name', how='left')
        print(f"DEBUG: Después de merge union_data y plans_for_merge. Columnas: {final_data.columns.tolist()}")

        # final_data['type_plan'] = final_data.apply(lambda row: row['plan']
        #                                                         if pd.notnull(row['plan']) else row['plan_name'], axis=1)
        # Reemplazo con una lógica más directa para 'type_plan' que coincide con 'plan_name' original del usuario
        # y que es la que se usa en el merge.
        # Asumiendo que quieres el nombre del plan ('Smart', 'Ultra') como 'type_plan'.
        final_data['type_plan'] = final_data['plan']
        print("DEBUG: 'type_plan' creada.")


        final_data.drop(columns=['plan_name'], inplace=True, errors='ignore') # Eliminar 'plan_name' de plans_df después del merge
        final_data = final_data.rename(columns={'plan': 'plan_id_from_user_df'}) # Renombramos para evitar cualquier confusión si 'plan' era temporal
        print("DEBUG: Columna 'plan_name' eliminada y 'plan' renombrada.")
        print(f"DEBUG: Columnas finales antes de extras: {final_data.columns.tolist()}")


        final_data['extra_calls'] = (final_data['total_minutes'] - final_data['minutes_included']).clip(lower=0)
        final_data['extra_texts'] = (final_data['message_count'] - final_data['messages_included']).clip(lower=0)
        final_data['extra_dates'] = (final_data['compil_internet'] - final_data['mb_per_month_included']).clip(lower=0)
        print("DEBUG: Extras calculados (calls, texts, dates).")

        final_data['extra_charges'] = (final_data['extra_calls'] * final_data['usd_per_minute'] +
                                       final_data['extra_texts'] * final_data['usd_per_message'] +
                                       final_data['extra_dates'] * final_data['usd_per_gb'])
        print("DEBUG: 'extra_charges' calculados.")

        # --- VERIFICACIÓN FINAL PARA LA GRÁFICA ---
        # La gráfica necesita 'type_plan', 'month', 'call_count'.
        # 'type_plan' se crea arriba.
        # 'month' viene de las agrupaciones iniciales (de calls_df, messages_df, internet_df).
        # 'call_count' viene de group_calls.
        # ¡Todo parece estar en su lugar!

        # Asegúrate de que 'month' esté como categoría o string para la gráfica si es to_period
        # Puede que necesites convertir final_data['month'] a string o a un formato ordinal si Matplotlib lo requiere para el eje X
        final_data['month'] = final_data['month'].astype(str) # Convertir Period a String para compatibilidad en gráfica

        print(f"DEBUG: final_data head antes de return:\n{final_data[['user_id', 'type_plan', 'month', 'call_count', 'extra_charges']].head(10)}")
        print(f"DEBUG: Columnas finales de final_data: {final_data.columns.tolist()}")
        print("DEBUG: Carga y limpieza de datos finalizada con éxito.")
        return final_data

    except FileNotFoundError as e:
        print(f"ERROR en limpieza.py: Archivo no encontrado. Detalles: {e}")
        import traceback
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"ERROR en limpieza.py: Ocurrió un error inesperado durante el procesamiento. Detalles: {e}")
        import traceback
        traceback.print_exc()
        return None
    