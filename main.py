"""
Taller: Adquisición, procesamiento y visualización de datos
Dataset: Online Retail Data Set
Universidad Yachay Tech - Maestría en Ciencia de Datos

Autor: Fausto Guano
Fecha: 27/09/2025

"""

import os

# Importar módulos
import sys
from datetime import datetime

# Importar módulos del proyecto
from src.adquisicion_datos import load_and_clean_data
from src.analisis_exploratorio import perform_eda
from src.utils import generate_final_report
from src.visualizacion import create_all_visualizations


def main():
    """Función principal que ejecuta todo el taller"""

    print("TALLER DE CIENCIA DE DATOS - ONLINE RETAIL DATASET")
    print("Universidad Yachay Tech - Maestría en Ciencia de Datos")

    try:
        # PARTE 1: Adquisición y limpieza de datos
        print("=" * 60)
        print("PARTE 1: ADQUISICIÓN Y LIMPIEZA DE DATOS")

        df_clean = load_and_clean_data()
        print(f"Datos limpios: {df_clean.shape}")

        # PARTE 2: Análisis Exploratorio
        print("\n" + "=" * 60)
        print("PARTE 2: ANÁLISIS EXPLORATORIO DE DATOS (EDA)")

        eda_results = perform_eda(df_clean)
        print("EDA realizado.")

        # PARTE 3: Visualizaciones
        print("\n" + "=" * 60)
        print("PARTE 3: VISUALIZACIONES")

        visualizations = create_all_visualizations(df_clean)

        # Reporte final
        print("\n" + "=" * 60)
        print("REPORTE FINAL")

        generate_final_report(df_clean, eda_results, visualizations)
        print("Reporte final.")

        print("\n ARCHIVOS GENERADOS:")
        output_files = [
            "data/online_retail.db",
            "output/visualizacion_1_analisis_temporal.png",
            "output/visualizacion_2_productos_clientes.png",
            "output/visualizacion_3_analisis_avanzado.png",
            "output/reporte_final_online_retail.txt",
        ]

    except Exception as e:
        print(f"\n Error de ejecución: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
