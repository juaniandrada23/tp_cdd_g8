import pandas as pd
import chardet
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# Detectar la codificación del archivo CSV
with open('emision_CO2_autos2.csv', 'rb') as f:
    result = chardet.detect(f.read())

# Cargar el archivo CSV con la codificación detectada || Eliminar columnas con muy pocos datos o que son irrelevantes
green = pd.read_csv('emision_CO2_autos2.csv', encoding=result['encoding'], on_bad_lines='skip')
green_clean = green.drop(columns=['VFN', 'Mt', 'Ewltp (g/km)', 'Erwltp (g/km)', 'De', 'Vf', 'It', 'Ernedc (g/km)', 'z (Wh/km)', 'ID', 'Mp', 'TAN', 'Va', 'Ve', 'Mk', 'Cr', 'r'])

# Resumen de los datos
print("Resumir los datos")
print(green_clean.info())
print("-------------------")
print("Análisis Descriptivo")
print(green_clean.describe())
print("-------------------")

#--------Inicio---------
st.markdown("<h1 style='text-align: center; color: #EAEBED;'>Ciencia de datos | Entrega 2 | Grupo 8 5K3</h1>", unsafe_allow_html=True)

st.title("Primeros datos del dataset sin columnas eliminadas")
st.write(green.head())

st.title("Primeros datos del dataset con columnas eliminadas")
st.write(green_clean.head())

col1, col2 = st.columns(2)
with col1:
    #Valores faltantes
    missing_values = green_clean.isnull().sum()
    st.write("Valores faltantes por columna:")
    st.write(missing_values)

with col2:
    # Análisis de datos duplicados
    st.title("Análisis de datos duplicados")
    duplicates = green_clean.duplicated(keep=False).sum()
    total_rows = green_clean.shape[0]
    duplicate_percentage = (duplicates / total_rows) * 100
    st.write(f"Número de filas duplicadas: {duplicates}")
    st.write(f"Porcentaje de filas duplicadas: {duplicate_percentage:.2f}%")
    
    # Mostrar algunas filas duplicadas
    duplicated_rows = green_clean[green_clean.duplicated(keep=False)]
    st.write("Filas duplicadas (primeras 5):")
    st.write(duplicated_rows.head())

# Eliminar filas duplicadas | Guardar el nuevo DataFrame sin duplicados en un archivo CSV
green_clean_no_duplicates = green_clean.drop_duplicates()
green_clean_no_duplicates.to_csv('emision_CO2_sin_duplicados.csv', index=False)

#Analisis de correlacion
st.title("Mapa de correlación entre variables")
green_clean_numeric = green_clean.select_dtypes(include=['float64', 'int64'])
corr_matrix = green_clean_numeric.corr()
plt.figure(figsize=(6, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
st.pyplot(plt)

#Graficos
col3, col4 = st.columns(2)
with col3:
    st.title("Distribución de la masa (m kg)")
    plt.figure(figsize=(10, 6))
    plt.hist(green_clean['m (kg)'], bins=30, color='skyblue')
    st.pyplot(plt)

with col4:
    st.title("Distribución por tipo de combustible")
    green_clean['Ft'] = green_clean['Ft'].str.lower().str.strip()
    fuel_distribution = green_clean['Ft'].value_counts()
    st.bar_chart(fuel_distribution)

col5, col6 = st.columns(2)
with col5:
    st.title("Relación entre masa del vehículo y emisiones de CO2")
    plt.figure(figsize=(10, 6))
    plt.scatter(green_clean['m (kg)'], green_clean['Enedc (g/km)'], alpha=0.5, color='green')
    plt.xlabel('Masa (kg)')
    plt.ylabel('Emisiones de CO2 (g/km)')
    st.pyplot(plt)

with col6:
    st.title("Emisiones promedio por fabricante")
    avg_emissions_by_manufacturer = green_clean.groupby('Man')['Enedc (g/km)'].mean()
    avg_emissions_by_manufacturer = avg_emissions_by_manufacturer[avg_emissions_by_manufacturer > 0]
    st.bar_chart(avg_emissions_by_manufacturer)
