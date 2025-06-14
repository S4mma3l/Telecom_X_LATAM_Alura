import pandas as pd
import numpy as np

# URL de la base de datos de Telecom X
url_data = 'https://raw.githubusercontent.com/alura-cursos/challenge2-data-science-LATAM/refs/heads/main/TelecomX_Data.json'

print("--- Cargando la base de datos para análisis de columnas ---")
try:
    # Cargar el archivo JSON directamente con pd.read_json()
    # Para esta estructura de JSON (lista de objetos), pd.read_json() ya es suficiente
    # y convierte cada clave de los objetos de nivel superior en una columna.
    df = pd.read_json(url_data)
    print("Base de datos cargada exitosamente con pd.read_json().")
except Exception as e:
    print(f"Error al cargar la base de datos desde {url_data}: {e}")
    print("Por favor, verifica la URL y la accesibilidad del archivo.")
    # Crear un DataFrame de ejemplo si la carga falla para no detener la demostración
    print("Creando un DataFrame de ejemplo para la demostración del análisis de columnas...")
    data_mock = {
        'customerID': [f'C{i:04d}' for i in range(1, 3)],
        'gender': ['Male', 'Female'],
        'SeniorCitizen': [0, 1],
        'Partner': ['Yes', 'No'],
        'Dependents': ['No', 'Yes'],
        'MonthlyCharges': [70.70, 29.85],
        'TotalCharges': ['1755.25', '29.85'],
        'Churn': ['No', 'Yes']
    }
    df = pd.DataFrame(data_mock)

print("\n--- Nombres de todas las columnas (después de pd.read_json) ---")
print(df.columns.tolist())

print("\n--- Información detallada de las columnas (df.info()) ---")
df.info()

print("\n--- Conteo de valores nulos por columna ---")
print(df.isnull().sum())

print("\n--- Aplicando pd.json_normalize() (para demostración de archivos JSON anidados) ---")
# Para este archivo específico, pd.read_json() ya hizo la normalización,
# pero si tuvieras un JSON con una clave raíz que contiene la lista de clientes
# o si hubiera diccionarios anidados dentro de una columna, usarías json_normalize.

# Ejemplo: Si el JSON fuera {"Clientes": [{"customerID": ...}, {"customerID": ...}]}
# temp_data = pd.read_json(url_data)
# df_normalized = pd.json_normalize(temp_data['Clientes']) # Si 'Clientes' fuera la clave principal

# En nuestro caso, el JSON es directamente una lista de objetos,
# así que podemos normalizar los registros directamente si quisiéramos forzarlo,
# pero resultará en el mismo DataFrame ya que no hay anidación profunda.
try:
    df_normalized = pd.json_normalize(df.to_dict(orient='records'))
    print("\nDataFrame después de aplicar pd.json_normalize (resultado similar para este archivo):")
    print(df_normalized.head())
    print("\n--- Nombres de columnas después de pd.json_normalize ---")
    print(df_normalized.columns.tolist())
    print("\n--- Información detallada de las columnas después de pd.json_normalize ---")
    df_normalized.info()
except Exception as e:
    print(f"No fue posible aplicar pd.json_normalize de esta forma: {e}")
    print("Esto podría deberse a la estructura del DataFrame si ya está completamente plano.")