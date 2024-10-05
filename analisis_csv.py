import pandas as pd
import chardet
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(layout="wide")

# Cargar el CSV y detectar la codificación
def load_data(filepath):
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(filepath, encoding=result['encoding'], on_bad_lines='skip', low_memory=False)

# Limpiar los datos y eliminar columnas irrelevantes
def clean_data(df):
    columns_to_drop = ['VFN', 'MMS', 'Mh', 'Mt', 'Ewltp (g/km)', 'Erwltp (g/km)', 
                       'De', 'Vf', 'It', 'Ernedc (g/km)', 'z (Wh/km)', 'ID', 'Mp', 
                       'TAN', 'Va', 'Ve', 'Mk', 'Cr', 'r']
    return df.drop(columns=columns_to_drop)

# Convertir valores a mayúsculas y eliminar espacios en blanco
def normalize_column_values(df, column_name):
    df[column_name] = df[column_name].str.upper().str.strip()
    return df

# Generar mapa de correlación entre variables
def plot_correlation(df):
    st.title("Mapa de correlación entre variables")
    df_numeric = df.select_dtypes(include=['float64', 'int64'])
    corr_matrix = df_numeric.corr()
    plt.figure(figsize=(6, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    st.pyplot(plt)

# Detectar y tratar outliers basados en el Z-score
def detect_and_remove_outliers_zscore(df, threshold=3):
    st.title("Proceso de detección y tratamiento de outliers con Z-score")

    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Crear DataFrame para almacenar los datos sin outliers
    df_without_outliers = df.copy()

    for column in numeric_columns:
        st.subheader(f"Tratamiento de outliers para: {column}")

        # Calcular la media y desviación estándar de la columna
        mean = df[column].mean()
        std = df[column].std()

        # Calcular el Z-score para cada valor
        z_scores = (df[column] - mean) / std

        # Detectar outliers con un umbral de Z-score (por defecto, 3 desviaciones estándar)
        outliers = df[np.abs(z_scores) > threshold]
        non_outliers = df[np.abs(z_scores) <= threshold]
        
        st.write(f"Outliers detectados en {column}: {len(outliers)}")

        # Gráfico de dispersión con outliers en rojo y no-outliers en verde
        plt.figure(figsize=(10, 6))
        plt.scatter(non_outliers.index, non_outliers[column], color='green', label='Dentro del rango', alpha=0.5)
        plt.scatter(outliers.index, outliers[column], color='red', label='Outliers', alpha=0.5)
        plt.title(f'Diagrama de dispersión para {column}')
        plt.xlabel('Índice')
        plt.ylabel(column)
        plt.legend()
        st.pyplot(plt)

        # Gráfico de boxplot horizontal (como el ejemplo que me diste)
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=column, orient='h')  # Orientación horizontal
        plt.title(f'Boxplot de {column}')
        plt.xlabel(f'{column}')
        st.pyplot(plt)

        # Eliminar los outliers del DataFrame original
        df_without_outliers = df_without_outliers[np.abs(z_scores) <= threshold]

    st.write("Datos después de eliminar outliers")
    st.write(df_without_outliers.head())

    return df_without_outliers

# Mostrar gráficos de distribución y relaciones simples
def plot_simple_charts(df):
    col3, col4 = st.columns(2)
    with col3:
        st.title("Distribución de la masa (m kg)")
        plt.figure(figsize=(10, 6))
        plt.hist(df['m (kg)'], bins=30, color='skyblue')
        st.pyplot(plt)
    with col4:
        st.title("Distribución por tipo de combustible")
        fuel_distribution = df['Ft'].value_counts().sort_values(ascending=False)
        st.bar_chart(fuel_distribution)

    col5, col6 = st.columns(2)
    with col5:
        st.title("Relación entre masa del vehículo y emisiones de CO2")
        plt.figure(figsize=(10, 6))
        plt.scatter(df['m (kg)'], df['Enedc (g/km)'], alpha=0.5, color='green')
        plt.xlabel('Masa (kg)')
        plt.ylabel('Emisiones de CO2 (g/km)')
        st.pyplot(plt)
    with col6:
        st.title("Emisiones totales por fabricante")
        total_emissions_by_manufacturer = df.groupby('Man')['Enedc (g/km)'].sum().sort_values(ascending=False)
        st.bar_chart(total_emissions_by_manufacturer)

# Análisis de datos duplicados
def analyze_duplicates(df):
    st.title("Análisis de datos duplicados")
    duplicates = df.duplicated(keep=False).sum()
    total_rows = df.shape[0]
    duplicate_percentage = (duplicates / total_rows) * 100
    st.write(f"Número de filas duplicadas: {duplicates}")
    st.write(f"Porcentaje de filas duplicadas: {duplicate_percentage:.2f}%")

# Mostrar gráficos de conteo de valores
def plot_value_counts(df):
    col1, col2 = st.columns(2)
    with col1:
        st.title("Conteo de capacidades del motor (ec cm3)")
        value_counts_ec = df['ec (cm3)'].value_counts().sort_values(ascending=False)
        st.bar_chart(value_counts_ec)
    with col2:
        st.title("Conteo de masa de los vehículos (m kg)")
        value_counts_m = df['m (kg)'].value_counts().sort_values(ascending=False)
        st.bar_chart(value_counts_m)

    col3, col4 = st.columns(2)
    with col3:
        st.title("Conteo de distancia entre ejes (W mm)")
        value_counts_w = df['W (mm)'].value_counts().sort_values(ascending=False)
        st.bar_chart(value_counts_w)

    with col4:
        st.title("Conteo de ancho del eje delantero (At1 mm)")
        value_counts_at1 = df['At1 (mm)'].value_counts().sort_values(ascending=False)
        st.bar_chart(value_counts_at1)

    col5, col6 = st.columns(2)
    with col5:
        st.title("Conteo de ancho del eje trasero (At2 mm)")
        value_counts_at2 = df['At2 (mm)'].value_counts().sort_values(ascending=False)
        st.bar_chart(value_counts_at2)
    with col6:
        st.title("Conteo de emisiones CO₂ (Enedc g/km)")
        value_counts_co2 = df['Enedc (g/km)'].value_counts().sort_values(ascending=False)
        st.bar_chart(value_counts_co2)

# Mostrar gráficos de frecuencias
def plot_frequencies_ct(df):
    col1, col2 = st.columns(2)
    df = normalize_column_values(df, 'Ct')
    df = normalize_column_values(df, 'T')
    df = normalize_column_values(df, 'Ft')
    df = normalize_column_values(df, 'Fm')


    with col1:
        st.title("Frecuencia por categoría de vehículo (Ct)")
        st.bar_chart(df['Ct'].value_counts())
    with col2:
        st.title("Frecuencia por tipo de vehículo (T)")
        st.bar_chart(df['T'].value_counts())

    col3, col4 = st.columns(2)
    with col3:
        st.title("Frecuencia por tipo de combustible (Ft)")
        st.bar_chart(df['Ft'].value_counts())
    with col4:
        st.title("Frecuencia por modo de combustible (Fm)")
        st.bar_chart(df['Fm'].value_counts())

def plot_histograms(df):
    st.title("Histogramas de variables numéricas")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    for column in numeric_columns:
        st.subheader(f"Distribución de {column}")
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column], bins=30, kde=True, color='skyblue')
        plt.xlabel(column)
        plt.ylabel('Frecuencia')
        plt.title(f'Histograma de {column}')
        st.pyplot(plt)
        plt.clf()

# Ejecución principal
green = load_data('emision_CO2_autos2.csv')
green_clean = clean_data(green)

st.markdown("<h1 style='text-align: center; color: #EAEBED;'>Ciencia de Datos | Entrega 2 | Grupo 8 5K3</h1>", unsafe_allow_html=True)

st.title("Primeros datos del dataset original")
st.write(green.head())

st.title("Primeros datos del dataset limpio")
st.write(green_clean.head())

st.title("Valores faltantes por columna")
missing_values = green_clean.isnull().sum()
st.write(missing_values)

# Eliminar duplicados antes de hacer el análisis de outliers
green_clean_no_duplicates1 = green_clean.drop_duplicates()
green_clean_no_duplicates = detect_and_remove_outliers_zscore(green_clean_no_duplicates1)
green_clean_no_duplicates.to_csv('emision_CO2_sin_duplicados_sin_outliers.csv', index=False)

plot_histograms(green_clean_no_duplicates)
plot_correlation(green_clean_no_duplicates)
analyze_duplicates(green_clean)
plot_simple_charts(green_clean_no_duplicates)
plot_value_counts(green_clean_no_duplicates)
plot_frequencies_ct(green_clean_no_duplicates)
