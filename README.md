# Ciencia de Datos | UTN FRC | Grupo 8 | Trabajo Práctico

## Entrega 2 - Análisis de Emisiones de CO₂ en Vehículos

Este proyecto forma parte del Trabajo Práctico de la materia **Ciencia de Datos** de la UTN FRC, Grupo 8. El objetivo del análisis es explorar y visualizar las emisiones de CO₂ de vehículos utilizando un dataset que contiene datos de fabricantes, características de los vehículos y sus emisiones.

### Código

1. **Carga y limpieza del dataset**:
   El código carga el archivo CSV que contiene los datos de emisiones de CO₂ de vehículos. Utiliza `pandas` para eliminar columnas irrelevantes o con demasiados datos faltantes, manteniendo solo aquellas que aportan al análisis de las características físicas y emisiones de los vehículos.

2. **Resumen del dataset**:
   Se imprime un resumen del contenido del dataset, incluyendo información sobre los tipos de datos de las columnas y un análisis descriptivo de las variables numéricas.

3. **Visualización interactiva**:
   Utilizando **Streamlit**, el código genera una serie de gráficos que permiten explorar los datos de manera interactiva:
   
   - **Distribución de la masa (m kg)**: Histograma que muestra cómo varía el peso de los vehículos en el dataset.
   - **Distribución por tipo de combustible**: Gráfico de barras que visualiza la cantidad de vehículos según el tipo de combustible.
   - **Relación entre masa y emisiones de CO₂**: Gráfico de dispersión que muestra la relación entre el peso del vehículo y sus emisiones de CO₂.
   - **Emisiones promedio por fabricante**: Gráfico de barras que representa el promedio de emisiones de CO₂ de cada fabricante.
   - **Distribuciones por agrupación de fabricantes y otras características**: Gráficos adicionales que muestran cómo se agrupan los fabricantes y se distribuyen otros aspectos relacionados con los vehículos.

### Ejecución del Proyecto

1. Instala las dependencias:
   pip install pandas chardet streamlit matplotlib seaborn
2. Ejecucion de Streamlit:
   streamlit run analisis_csv.py
