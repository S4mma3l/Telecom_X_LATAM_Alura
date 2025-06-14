import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests # Importa la biblioteca requests para obtener datos de URLs
import json     # Importa la biblioteca json para parsear contenido JSON

# --- PASO 1: EXTRACCIÓN DE DATOS ---
# Descripción: Cargar los datos directamente desde la API y convertirlos a un DataFrame de Pandas.
url_data = 'https://raw.githubusercontent.com/alura-cursos/challenge2-data-science-LATAM/refs/heads/main/TelecomX_Data.json'

print("--- Iniciando la fase de Extracción de Datos (Paso 1) ---")
try:
    # Obtener el contenido JSON directamente usando requests
    response = requests.get(url_data)
    response.raise_for_status() # Lanza un HTTPError para respuestas malas (4xx o 5xx)
    data_list_of_dicts = response.json() # Parsear JSON a una lista de diccionarios de Python

    # Normalizar la estructura JSON para aplanar las columnas anidadas.
    # pd.json_normalize espera una lista de diccionarios, que es lo que obtenemos de response.json().
    df = pd.json_normalize(data_list_of_dicts)
    print("Datos cargados y normalizados exitosamente desde la URL.")
except requests.exceptions.RequestException as req_err:
    print(f"Error de red o HTTP al cargar los datos desde la URL {url_data}: {req_err}")
    print("Asegúrate de que la URL es correcta y el archivo es accesible.")
    # Fallback: Creando un DataFrame de ejemplo para la demostración si la carga falla
    print("Creando un DataFrame de ejemplo para la demostración...")
    data_mock = {
        'customerID': [f'C{i:04d}' for i in range(1, 11)],
        'customer.gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
        'customer.SeniorCitizen': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        'customer.Partner': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'customer.Dependents': ['No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes'],
        'customer.tenure': [24, 1, 8, 45, 2, 72, 11, 10, 67, 7],
        'phone.PhoneService': ['Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes'],
        'phone.MultipleLines': ['No', 'No phone service', 'No', 'No', 'No', 'Yes', 'No', 'No phone service', 'Yes', 'No'],
        'internet.InternetService': ['DSL', 'DSL', 'Fiber optic', 'DSL', 'Fiber optic', 'Fiber optic', 'Fiber optic', 'DSL', 'DSL', 'Fiber optic'],
        'internet.OnlineSecurity': ['Yes', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No'],
        'internet.OnlineBackup': ['Yes', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.DeviceProtection': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.TechSupport': ['No', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'No'],
        'internet.StreamingTV': ['No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.StreamingMovies': ['No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'account.Contract': ['One year', 'Month-to-month', 'Month-to-month', 'One year', 'Month-to-month', 'Two year', 'Month-to-month', 'Month-to-month', 'Two year', 'Month-to-month'],
        'account.PaperlessBilling': ['Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'account.PaymentMethod': ['Mailed check', 'Electronic check', 'Electronic check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check', 'Mailed check', 'Credit card (automatic)', 'Electronic check'],
        'account.Charges.Monthly': [70.70, 29.85, 99.65, 30.60, 78.90, 115.80, 70.35, 20.25, 99.80, 84.10],
        'account.Charges.Total': ['1755.25', '29.85', '700.75', '1397.60', '135.40', '8647.25', '733.20', '216.75', '6874.00', '586.15'],
        'Churn': ['No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes']
    }
    df = pd.DataFrame(data_mock)
except json.JSONDecodeError as json_err:
    print(f"Error al decodificar el JSON desde la URL {url_data}: {json_err}")
    print("El contenido de la URL podría no ser un JSON válido.")
    print("Creando un DataFrame de ejemplo para la demostración...")
    data_mock = {
        'customerID': [f'C{i:04d}' for i in range(1, 11)],
        'customer.gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
        'customer.SeniorCitizen': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        'customer.Partner': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'customer.Dependents': ['No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes'],
        'customer.tenure': [24, 1, 8, 45, 2, 72, 11, 10, 67, 7],
        'phone.PhoneService': ['Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes'],
        'phone.MultipleLines': ['No', 'No phone service', 'No', 'No', 'No', 'Yes', 'No', 'No phone service', 'Yes', 'No'],
        'internet.InternetService': ['DSL', 'DSL', 'Fiber optic', 'DSL', 'Fiber optic', 'Fiber optic', 'Fiber optic', 'DSL', 'DSL', 'Fiber optic'],
        'internet.OnlineSecurity': ['Yes', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No'],
        'internet.OnlineBackup': ['Yes', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.DeviceProtection': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.TechSupport': ['No', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'No'],
        'internet.StreamingTV': ['No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.StreamingMovies': ['No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'account.Contract': ['One year', 'Month-to-month', 'Month-to-month', 'One year', 'Month-to-month', 'Two year', 'Month-to-month', 'Month-to-month', 'Two year', 'Month-to-month'],
        'account.PaperlessBilling': ['Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'account.PaymentMethod': ['Mailed check', 'Electronic check', 'Electronic check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check', 'Mailed check', 'Credit card (automatic)', 'Electronic check'],
        'account.Charges.Monthly': [70.70, 29.85, 99.65, 30.60, 78.90, 115.80, 70.35, 20.25, 99.80, 84.10],
        'account.Charges.Total': ['1755.25', '29.85', '700.75', '1397.60', '135.40', '8647.25', '733.20', '216.75', '6874.00', '586.15'],
        'Churn': ['No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes']
    }
    df = pd.DataFrame(data_mock)
except Exception as e:
    print(f"Ocurrió un error inesperado al procesar los datos: {e}")
    print("Creando un DataFrame de ejemplo para la demostración...")
    data_mock = {
        'customerID': [f'C{i:04d}' for i in range(1, 11)],
        'customer.gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
        'customer.SeniorCitizen': [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        'customer.Partner': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'customer.Dependents': ['No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Yes'],
        'customer.tenure': [24, 1, 8, 45, 2, 72, 11, 10, 67, 7],
        'phone.PhoneService': ['Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes'],
        'phone.MultipleLines': ['No', 'No phone service', 'No', 'No', 'No', 'Yes', 'No', 'No phone service', 'Yes', 'No'],
        'internet.InternetService': ['DSL', 'DSL', 'Fiber optic', 'DSL', 'Fiber optic', 'Fiber optic', 'Fiber optic', 'DSL', 'DSL', 'Fiber optic'],
        'internet.OnlineSecurity': ['Yes', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No'],
        'internet.OnlineBackup': ['Yes', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.DeviceProtection': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.TechSupport': ['No', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'No'],
        'internet.StreamingTV': ['No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'internet.StreamingMovies': ['No', 'No', 'No', 'No', 'No', 'Yes', 'No', 'No', 'Yes', 'No'],
        'account.Contract': ['One year', 'Month-to-month', 'Month-to-month', 'One year', 'Month-to-month', 'Two year', 'Month-to-month', 'Month-to-month', 'Two year', 'Month-to-month'],
        'account.PaperlessBilling': ['Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        'account.PaymentMethod': ['Mailed check', 'Electronic check', 'Electronic check', 'Bank transfer (automatic)', 'Electronic check', 'Credit card (automatic)', 'Mailed check', 'Mailed check', 'Credit card (automatic)', 'Electronic check'],
        'account.Charges.Monthly': [70.70, 29.85, 99.65, 30.60, 78.90, 115.80, 70.35, 20.25, 99.80, 84.10],
        'account.Charges.Total': ['1755.25', '29.85', '700.75', '1397.60', '135.40', '8647.25', '733.20', '216.75', '6874.00', '586.15'],
        'Churn': ['No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Yes']
    }
    df = pd.DataFrame(data_mock)


print("\n--- Vista Previa de los Datos (Primeras 5 filas) ---")
print(df.head())

# --- PASO 2: TRANSFORMACIÓN DE LOS DATOS (Explorar columnas y tipos) ---
# Descripción: Comprender la estructura del dataset y el significado de sus columnas.
print("\n--- Información General del DataFrame (Paso 2) ---")
print(df.info())

print("\n--- Estadísticas Descriptivas (Paso 7 - Análisis Descriptivo Inicial) ---")
print(df.describe(include='all'))


# --- PASO 3: COMPROBACIÓN DE INCOHERENCIAS EN LOS DATOS ---
# Descripción: Verificar valores ausentes, duplicados, errores de formato e inconsistencias.
print("\n--- Conteo de valores nulos por columna (Paso 3) ---")
print(df.isnull().sum())

print("\n--- Conteo de filas duplicadas (Paso 3) ---")
print(f"Filas duplicadas antes de la eliminación: {df.duplicated().sum()}")


# --- PASO 4: MANEJO DE INCONSISTENCIAS ---
# Descripción: Aplicar las correcciones necesarias para asegurar datos completos y coherentes.
print("\n--- Iniciando la fase de Manejo de Inconsistencias (Paso 4) ---")

# Manejo de filas duplicadas
df.drop_duplicates(inplace=True)
print(f"Filas duplicadas después de la eliminación: {df.duplicated().sum()}")

# 1. Corrección del tipo de dato para 'account.Charges.Total'
# 'account.Charges.Total' a menudo se carga como objeto (string) debido a valores vacíos.
# Convertimos los espacios vacíos a NaN y luego a numérico.
print("\n--- Limpieza y conversión de 'account.Charges.Total' ---")
df['account.Charges.Total'] = pd.to_numeric(df['account.Charges.Total'], errors='coerce')
print(f"Valores nulos en 'account.Charges.Total' después de la conversión: {df['account.Charges.Total'].isnull().sum()}")

# Manejo de valores nulos en 'account.Charges.Total' (suele ocurrir para clientes nuevos con tenure 0)
# Para fines de este análisis, los rellenaremos con 0.
df['account.Charges.Total'].fillna(0, inplace=True)
print(f"Valores nulos en 'account.Charges.Total' después de rellenar: {df['account.Charges.Total'].isnull().sum()}")

# Verificar si 'customer.tenure' es numérico; si no, convertirlo.
if not pd.api.types.is_numeric_dtype(df['customer.tenure']):
    df['customer.tenure'] = pd.to_numeric(df['customer.tenure'], errors='coerce')
    df['customer.tenure'].fillna(0, inplace=True) # Rellenar NaNs si aparecen
    df['customer.tenure'] = df['customer.tenure'].astype(int) # Convertir a entero si es necesario
print("\n--- Verificación de 'customer.tenure' ---")
print(df['customer.tenure'].dtype)


# --- PASO 6: ESTANDARIZACIÓN Y TRANSFORMACIÓN DE DATOS (Adicional) ---
# Descripción: Hacer la información más consistente, comprensible y adecuada para el análisis.
print("\n--- Iniciando Estandarización y Transformación de Datos (Paso 6) ---")

# Renombrar columnas para facilitar el acceso (reemplazar '.' por '_')
df.columns = df.columns.str.replace('.', '_', regex=False)
print("\n--- Nombres de columnas después de la estandarización ---")
print(df.columns.tolist())

# 2. Convertir 'customer_SeniorCitizen' a tipo booleano o categórico para mejor interpretación
# Originalmente es 0 o 1
df['customer_SeniorCitizen'] = df['customer_SeniorCitizen'].map({0: 'No', 1: 'Yes'})
print("\n--- Transformación de 'customer_SeniorCitizen' ---")
print(df['customer_SeniorCitizen'].value_counts())

# 3. Convertir la variable objetivo 'Churn' a numérica (0 y 1)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
print("\n--- Transformación de 'Churn' (0=No, 1=Yes) ---")
print(df['Churn'].value_counts())

# 4. Manejo de columnas categóricas con valores 'No service' o similares
# Unificaremos estos valores a 'No' para simplificar la categorización.
cols_to_normalize_service = [
    'phone_MultipleLines', 'internet_OnlineSecurity', 'internet_OnlineBackup',
    'internet_DeviceProtection', 'internet_TechSupport', 'internet_StreamingTV', 'internet_StreamingMovies'
]
for col in cols_to_normalize_service:
    if col in df.columns:
        df[col] = df[col].replace({'No phone service': 'No', 'No internet service': 'No'})
print("\n--- Normalización de 'No service' en columnas categóricas ---")
# Ejemplo de una columna después de la normalización
print(df['phone_MultipleLines'].value_counts())

# 5. Eliminar columnas que no son relevantes para el análisis de churn
# Por ejemplo, 'customerID' no es una característica predictiva.
if 'customerID' in df.columns:
    df.drop('customerID', axis=1, inplace=True)
    print("\n--- Columna 'customerID' eliminada ---")

# --- PASO 5: COLUMNA DE CUENTAS DIARIAS ---
# Descripción: Crear la columna "Cuentas_Diarias" utilizando la facturación mensual para calcular el valor diario.
if 'account_Charges_Monthly' in df.columns:
    df['Cuentas_Diarias'] = df['account_Charges_Monthly'] / 30
    print("\n--- Columna 'Cuentas_Diarias' creada exitosamente (Paso 5) ---")
    print(df[['account_Charges_Monthly', 'Cuentas_Diarias']].head())
else:
    print("\nAdvertencia: 'account_Charges_Monthly' no se encontró para crear 'Cuentas_Diarias'.")


# Verificación final de tipos de datos y nulos después de todas las transformaciones
print("\n--- Información final del DataFrame después de Transformación ---")
print(df.info())
print("\n--- Conteo de valores nulos después de Transformación ---")
print(df.isnull().sum())

# --- PASO 7: ANÁLISIS DESCRIPTIVO ---
# Descripción: Realizar un análisis descriptivo de los datos, calculando métricas como media, mediana, desviación estándar.
print("\n--- Análisis Descriptivo del DataFrame Completo (Paso 7) ---")
print(df.describe(include='all'))

# --- FASE 3: CARGA DE DATOS (Load) y ANÁLISIS EXPLORATORIO DE DATOS (EDA) ---
print("\n--- Iniciando la fase de Análisis Exploratorio de Datos (EDA) ---")

# Opcional: Guardar el DataFrame transformado para uso futuro
df.to_csv('Datos\\telecom_churn_clean.csv', index=False)
print("\nDataFrame transformado guardado como 'telecom_churn_clean.csv'")

# --- PASO 8: DISTRIBUCIÓN DE EVASIÓN ---
# Descripción: Comprender cómo está distribuida la variable "churn" (evasión) entre los clientes.
print("\n--- Tasa de Evasión (Churn) (Paso 8) ---")
churn_rate = df['Churn'].value_counts(normalize=True) * 100
print(f"Clientes que evadieron (Churn): {churn_rate[1]:.2f}%")
print(f"Clientes que no evadieron (No Churn): {churn_rate[0]:.2f}%")

plt.figure(figsize=(7, 5))
sns.countplot(x='Churn', data=df, palette='viridis')
plt.title('Distribución de Evasión de Clientes (Churn)', fontsize=14)
plt.xlabel('Evasión (0=No Churn, 1=Churn)', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.xticks(ticks=[0, 1], labels=['No Evasión', 'Evasión'])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- PASO 10: CONTEO DE EVASIÓN POR VARIABLES NUMÉRICAS ---
# Descripción: Explorar cómo las variables numéricas se distribuyen entre clientes que cancelaron y los que no.
print("\n--- Análisis de Variables Numéricas vs. Churn (Paso 10) ---")

# Comparación de 'customer_tenure' (antigüedad) por Churn
plt.figure(figsize=(12, 5))
sns.histplot(data=df, x='customer_tenure', hue='Churn', kde=True, palette='coolwarm', alpha=0.6)
plt.title('Distribución de Antigüedad (customer_tenure) por Evasión', fontsize=14)
plt.xlabel('Antigüedad del Cliente (Meses)', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Comparación de 'account_Charges_Monthly' (cargos mensuales) por Churn
plt.figure(figsize=(12, 5))
sns.histplot(data=df, x='account_Charges_Monthly', hue='Churn', kde=True, palette='coolwarm', alpha=0.6)
plt.title('Distribución de Cargos Mensuales (account_Charges_Monthly) por Evasión', fontsize=14)
plt.xlabel('Cargos Mensuales', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Comparación de 'account_Charges_Total' (cargos totales) por Churn
plt.figure(figsize=(12, 5))
sns.histplot(data=df, x='account_Charges_Total', hue='Churn', kde=True, palette='coolwarm', alpha=0.6)
plt.title('Distribución de Cargos Totales (account_Charges_Total) por Evasión', fontsize=14)
plt.xlabel('Cargos Totales', fontsize=12)
plt.ylabel('Número de Clientes', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Comparación de 'Cuentas_Diarias' por Churn
if 'Cuentas_Diarias' in df.columns:
    plt.figure(figsize=(12, 5))
    sns.histplot(data=df, x='Cuentas_Diarias', hue='Churn', kde=True, palette='coolwarm', alpha=0.6)
    plt.title('Distribución de Cuentas Diarias por Evasión', fontsize=14)
    plt.xlabel('Cargos Diarios', fontsize=12)
    plt.ylabel('Número de Clientes', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


# --- PASO 9: RECUENTO DE EVASIÓN POR VARIABLES CATEGÓRICAS ---
# Descripción: Explorar cómo se distribuye la evasión según variables categóricas.
print("\n--- Análisis de Variables Categóricas vs. Churn (Paso 9) ---")

# Función para graficar la tasa de churn para variables categóricas
def plot_churn_rate_by_category(dataframe, column, figsize=(8, 5)):
    churn_by_col = dataframe.groupby(column)['Churn'].mean().reset_index()
    churn_by_col['Churn_Rate_Percent'] = churn_by_col['Churn'] * 100
    
    plt.figure(figsize=figsize)
    sns.barplot(x=column, y='Churn_Rate_Percent', data=churn_by_col.sort_values('Churn_Rate_Percent', ascending=False), palette='magma')
    plt.title(f'Tasa de Evasión por {column}', fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Tasa de Evasión (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)
    # Añadir valores a las barras
    for index, row in churn_by_col.sort_values('Churn_Rate_Percent', ascending=False).iterrows():
        plt.text(index, row['Churn_Rate_Percent'] + 1, f"{row['Churn_Rate_Percent']:.2f}%", color='black', ha='center')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Se han actualizado los nombres de las columnas categóricas según la normalización (reemplazando '.' por '_')
categorical_cols = [
    'customer_gender', 'customer_SeniorCitizen', 'customer_Partner', 'customer_Dependents',
    'phone_PhoneService', 'phone_MultipleLines', 'internet_InternetService',
    'internet_OnlineSecurity', 'internet_OnlineBackup', 'internet_DeviceProtection',
    'internet_TechSupport', 'internet_StreamingTV', 'internet_StreamingMovies',
    'account_Contract', 'account_PaperlessBilling', 'account_PaymentMethod'
]

for col in categorical_cols:
    if col in df.columns:
        plot_churn_rate_by_category(df, col)

# --- PASO 12 (EXTRA): ANÁLISIS DE CORRELACIÓN ENTRE VARIABLES ---
# Descripción: Explorar la correlación entre diferentes variables del dataset.
print("\n--- Matriz de Correlación de Variables Numéricas (Paso 12 - Extra) ---")
numerical_df = df.select_dtypes(include=np.number)
# Asegurarse de que 'Churn' esté en la matriz de correlación (ya es numérico)
if 'Churn' not in numerical_df.columns:
    numerical_df['Churn'] = df['Churn'] # Añadir Churn si no fue seleccionado como numérico

corr_matrix = numerical_df.corr()

fig_corr = px.imshow(corr_matrix,
                     text_auto=True,
                     aspect="auto",
                     color_continuous_scale='Viridis',
                     title='Matriz de Correlación de Variables Numéricas')
fig_corr.update_layout(width=800, height=700)
fig_corr.show()