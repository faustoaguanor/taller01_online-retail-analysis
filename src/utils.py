# Importar librerias
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd


def create_project_structure():
    """
    Crea la estructura de directorios del proyecto.
    """
    directories = ["data", "output", "src", "docs"]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("Estructura de proyecto creada:")
    for directory in directories:
        print(f"* {directory}/")


def format_number(number):
    """
    Formatea números para presentación.

    Argumentoss:
        number (float): Número a formatear

    Returns:
        str: Número formateado
    """
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return f"{number:,.0f}"


def calculate_business_metrics(df):
    """
    Calcula métricas clave .

    Argumentoss:
        df : DataFrame con datos de transacciones

    Returns:
        dict: Métricas
    """
    metrics = {}

    # Métricas básicas
    metrics["total_transactions"] = len(df)
    metrics["total_revenue"] = df["TotalPrice"].sum()
    metrics["unique_customers"] = df["CustomerID"].nunique()
    metrics["unique_products"] = df["StockCode"].nunique()
    metrics["unique_invoices"] = df["InvoiceNo"].nunique()

    # Métricas calculadas
    metrics["avg_transaction_value"] = (
        df.groupby("InvoiceNo")["TotalPrice"].sum().mean()
    )
    metrics["avg_items_per_transaction"] = (
        df.groupby("InvoiceNo")["Quantity"].sum().mean()
    )
    metrics["avg_revenue_per_customer"] = (
        metrics["total_revenue"] / metrics["unique_customers"]
    )

    # Métricas temporales
    date_range = df["InvoiceDate"].max() - df["InvoiceDate"].min()
    metrics["business_days"] = date_range.days
    metrics["avg_daily_revenue"] = metrics["total_revenue"] / date_range.days

    # Métricas de concentración
    customer_revenue = df.groupby("CustomerID")["TotalPrice"].sum()
    metrics["top_10_customers_revenue"] = customer_revenue.nlargest(10).sum()
    metrics["top_10_customers_percent"] = (
        metrics["top_10_customers_revenue"] / metrics["total_revenue"]
    ) * 100

    return metrics


def generate_technical_documentation(df, eda_results):
    """
    Genera documentación  del análisis actualizada.

    Args:
        df : DataFrame con datos
        eda_results (dict): Resultados del EDA

    Returns:
        str: Documentación técnica
    """

    # Contar variables disponibles
    available_vars = []
    essential_vars = [
        "TotalPrice",
        "Month",
        "Hour",
        "DayOfWeek",
        "IsWeekend",
        "PriceCategory",
    ]
    for var in essential_vars:
        if var in df.columns:
            available_vars.append(var)

    doc = f"""
DOCUMENTACIÓN - TALLER CIENCIA DE DATOS
=================================================

PROCESAMIENTO DE DATOS:

1. FUENTE DE DATOS:
   • Dataset: Online Retail (UCI ML Repository)
   • Formato original: Excel (.xlsx)
   • Método de carga: Manual (pd.read_excel) 
   • Registros finales procesados: {len(df):,}
   • Período: {df['InvoiceDate'].min()} - {df['InvoiceDate'].max()}

2. PROCESO DE LIMPIEZA APLICADO:
   • Eliminación de CustomerID nulos (análisis de comportamiento)
   • Eliminación de Description nulos (productos categorizables)
   • Filtrado de Quantity <= 0 (devoluciones y errores)
   • Filtrado de UnitPrice <= 0 (promociones especiales)
   • Eliminación de registros duplicados exactos


3. VARIABLES DERIVADAS CREADAS:
   Variables disponibles en el dataset: {len(available_vars)}/{len(essential_vars)}
   
   Variables implementadas:
   * TotalPrice
    * Month
    * Hour
    * DayOfWeek
    * IsWeekend
    * PriceCategory


4. ARQUITECTURA DE DATOS:
   • Base de datos: SQLite (data/online_retail.db)
   • Tabla principal: online_retail_clean
   • Método de guardado: Chunks de 1,000 registros (límite SQL variables)
   • Índices optimizados: CustomerID, InvoiceNo, InvoiceDate, Country, StockCode

METODOLOGÍA DE ANÁLISIS:

1. ANÁLISIS EXPLORATORIO:
   • Análisis univariado de variables clave
   • Análisis temporal usando Month, Hour, DayOfWeek (mes, hora, día de la semana)
   • Segmentación clientes  
   • Análisis de patrones días de la semana
   • Análisis geográfico por Country (país)
   • Segmentación de productos por PriceCategory (categoría del precio)

2. TÉCNICAS DE VISUALIZACIÓN IMPLEMENTADAS:
   • Análisis de tiempo  
   • Heatmaps (patrones día×hora)
   • Análisis comparativo días de la semana 

3. STACK TECNOLÓGICO:
   • pandas: Manipulación y análisis de datos
   • matplotlib/seaborn: Visualizaciones 
   • SQLite3: Almacenamiento con chunks optimizados
   • numpy: Operaciones numéricas eficientes
   • scipy: Análisis estadístico 
 

REQUERIMIENTOS TÉCNICOS:
• Python 3.8+
• pandas, numpy, matplotlib, seaborn, scipy
• SQLite3 (incluido en Python)
"""
    return doc


def save_metadata_json(df, eda_results, visualization_files):
    """
    Guarda metadata en formato JSON.

    Argumentos:
        df: DataFrame con datos
        eda_results (dict): Resultados del EDA
        visualization_files (dict): Archivos de visualizaciones
    """
    metadata = {
        "project_info": {
            "name": "Online Retail Dataset Analysis",
            "university": "Universidad Yachay Tech",
            "course": "Maestría en Ciencia de Datos",
            "subject": "Fundamentos de Ciencia de Datos",
            "analysis_date": datetime.now().isoformat(),
            "version": "1.0",
        },
        "dataset_info": {
            "source": "UCI ML Repository",
            "original_records": len(df),
            "final_records": len(df),
            "columns": list(df.columns),
            "date_range": {
                "start": str(df["InvoiceDate"].min()),
                "end": str(df["InvoiceDate"].max()),
                "days": (df["InvoiceDate"].max() - df["InvoiceDate"].min()).days,
            },
        },
        "business_metrics": calculate_business_metrics(df),
        "files_generated": {
            "database": "data/online_retail.db",
            "visualizations": list(visualization_files.values()),
            "reports": [
                "output/eda_report.txt",
                "output/reporte_final_online_retail.txt",
                "output/interpretacion_visualizaciones.txt",
            ],
        },
        "quality_assessment": eda_results["metadata"]["quality"],
    }

    # Convertir valores numpy para serialización JSON
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        return obj

    # Limpiar metadata para JSON
    def clean_for_json(data):
        if isinstance(data, dict):
            return {key: clean_for_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_for_json(item) for item in data]
        else:
            return convert_numpy(data)

    clean_metadata = clean_for_json(metadata)

    with open("output/project_metadata.json", "w", encoding="utf-8") as f:
        json.dump(clean_metadata, f, indent=2, ensure_ascii=False, default=str)

    print("Metadata guardada: output/project_metadata.json")


def generate_final_report(df, eda_results, visualization_files):
    """
    Genera el reporte final completo del taller.

    Argumentos:
        df: DataFrame con datos
        eda_results (dict): Resultados del EDA
        visualization_files (dict): Archivos de visualizaciones
    """
    print("\nReporte final completo")

    # Generar componentes del reporte
    technical_docs = generate_technical_documentation(df, eda_results)

    # Compilar reporte final
    final_report = f"""

{technical_docs}


ARCHIVOS ENTREGABLES GENERADOS:
================================
DATABASE:
• data/online_retail.db - Base de datos SQLite optimizada

VISUALIZACIONES:
• output/visualizacion_1_analisis_temporal.png
• output/visualizacion_2_productos_clientes.png  
• output/visualizacion_3_analisis_avanzado.png

REPORTES Y ANÁLISIS:
• output/eda_report.txt - Análisis exploratorio exhaustivo
• output/interpretacion_visualizaciones.txt - Narrativa de gráficos
• output/reporte_final_online_retail.txt - Este reporte integrado
• output/project_metadata.json - Metadata programática para integración

CÓDIGO FUENTE MODULAR:
• main.py - Orquestador principal del pipeline
• src/adquisicion_datos.py - Módulo de adquisición y limpieza
• src/analisis_exploratorio.py - Módulo de análisis exploratorio
• src/visualizacion.py - Módulo de visualizaciones avanzadas  
• src/utils.py - Utilidades y generación de reportes


Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Universidad Yachay Tech - Maestría en Ciencia de Datos  
Curso: Fundamentos de Ciencia de Datos
"""

    # Guardar reporte final
    with open("output/reporte_final_online_retail.txt", "w", encoding="utf-8") as f:
        f.write(final_report)

    # Guardar metadata JSON
    save_metadata_json(df, eda_results, visualization_files)

    print("Reporte final guardado: output/reporte_final_online_retail.txt")
    print("Metadata JSON guardada: output/project_metadata.json")


def print_project_summary():
    """
    Imprime un resumen final del proyecto completado.
    """
    print(
        f"""
ESTRUCTURA DEL PROYECTO
=====================================

📂 Estructura Final del Proyecto:
├── Online Retail.xlsx          (Dataset original)
├── main.py                     (Ejecutor principal)
├── src/
│   ├── adquisicion_datos.py     (Módulo de carga y limpieza)
│   ├── analisis_exploratorio.py (Módulo de EDA)
│   ├── visualizacion.py       (Módulo de visualizaciones)
│   └── utils.py                (Utilidades y reportes)
├── data/
│   └── online_retail.db        (Base de datos SQLite)
├── output/
│   ├── visualizacion_1_analisis_temporal.png
│   ├── visualizacion_2_productos_clientes.png
│   ├── visualizacion_3_analisis_patrones.png
│   ├── eda_report.txt
│   ├── interpretacion_visualizaciones.txt
│   ├── reporte_final_online_retail.txt
│   └── project_metadata.json
└── docs/
    └── (documentación adicional)

"""
    )


if __name__ == "__main__":
    print("Módulo de utilidades cargado exitosamente!")
    print("Para usar: from src.utils import generate_final_report")
