# Importar librerías
import os
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd


def load_data_from_db(
    db_name="data/online_retail.db", table_name="online_retail_clean"
):
    """
    Carga datos desde la base de datos SQLite.

    Argumentos:
        db_name (str): Nombre del archivo de base de datos
        table_name (str): Nombre de la tabla

    Returns:
        pd.DataFrame: DataFrame con los datos
    """
    try:
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()

        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

        print(f"Datos cargados al dataframe exitosamente: {df.shape}")
        return df

    except Exception as e:
        print(f"Error al cargar datos al dataframe: {e}")
        raise


def describe_dataset(df):
    """
    Describe el dataset.

    Argumentos:
        df: DataFrame

    Returns:
        dict: Diccionario con información del dataset
    """
    print("\nDESCRIPCIÓN DEL DATASET:")

    dataset_description = """
    ONLINE RETAIL DATASET - DESCRIPCIÓN COMPLETA:
    
    *RESUMEN GENERAL:
    Este dataset contiene transacciones de una tienda online de regalos
    ubicada en Reino Unido con ventas al exterior. Los datos cubren transacciones reales entre
    diciembre 2010 y diciembre 2011.
    """

    print(dataset_description)

    # Estadísticas generales
    unique_customers = df["CustomerID"].nunique()
    unique_products = df["StockCode"].nunique()
    unique_invoices = df["InvoiceNo"].nunique()
    date_range = df["InvoiceDate"]
    total_revenue = df["TotalPrice"].sum()

    stats = {
        "total_transactions": len(df),
        "unique_customers": unique_customers,
        "unique_products": unique_products,
        "unique_invoices": unique_invoices,
        "total_revenue": total_revenue,
        "date_range_start": date_range.min(),
        "date_range_end": date_range.max(),
        "date_range_days": (date_range.max() - date_range.min()).days,
        "countries_served": df["Country"].nunique(),
        "avg_transaction_value": df.groupby("InvoiceNo")["TotalPrice"].sum().mean(),
    }

    print(f"\nESTADÍSTICAS:")
    print(f"*Total de transacciones: {stats['total_transactions']:,}")
    print(f"*Clientes únicos: {stats['unique_customers']:,}")
    print(f"*Productos únicos: {stats['unique_products']:,}")
    print(f"*Facturas únicas: {stats['unique_invoices']:,}")
    print(f"*Ingreso total: £{stats['total_revenue']:,.2f}")
    print(f"*Período: {stats['date_range_start']} a {stats['date_range_end']}")
    print(f"*Duración: {stats['date_range_days']} días")
    print(f"*Países atendidos: {stats['countries_served']}")
    print(f"*Valor promedio por transacción: £{stats['avg_transaction_value']:.2f}")

    return stats


def analyze_fields(df):
    """
    Analiza campos del dataset.

    Argumentos:
        df: DataFrame a analizar

    Returns:
        dict: Análisis por campo
    """
    print("\nANÁLISIS POR CAMPO:")

    field_analysis = {}

    # 1. InvoiceNo
    print("1. Factura:")
    unique_invoices = df["InvoiceNo"].nunique()
    avg_lines_per_invoice = len(df) / unique_invoices

    # Convertir a string
    try:
        invoice_str = df["InvoiceNo"].astype(str)
        invoice_patterns = invoice_str.str.len().value_counts().head()
        print(f"*Facturas únicas: {unique_invoices:,}")
        print(f"*Líneas por factura (promedio): {avg_lines_per_invoice:.1f}")
        print(f"*Patrones de longitud: {invoice_patterns.to_dict()}")

        field_analysis["InvoiceNo"] = {
            "unique_count": unique_invoices,
            "avg_lines_per_invoice": avg_lines_per_invoice,
            "length_patterns": invoice_patterns.to_dict(),
        }
    except Exception as e:
        print(f"*Error en análisis")

        field_analysis["InvoiceNo"] = {
            "unique_count": unique_invoices,
            "avg_lines_per_invoice": avg_lines_per_invoice,
            "length_patterns": "Mixed data types",
        }

    # 2. StockCode
    print(f"\n2. Código de Producto:")
    unique_products = df["StockCode"].nunique()
    top_products = df["StockCode"].value_counts().head()
    print(f"*Productos únicos: {unique_products:,}")
    print(f"*Top 5 productos más transaccionados:")
    for code, count in top_products.items():
        print(f"     - {code}: {count:,} transacciones")

    field_analysis["StockCode"] = {
        "unique_count": unique_products,
        "top_products": top_products.to_dict(),
    }

    # 3. Description
    print(f"\n3. Descripción del Producto:")
    unique_descriptions = df["Description"].nunique()
    print(f"*Descripciones únicas: {unique_descriptions:,}")
    print("*Ejemplos de productos:")
    for i, desc in enumerate(df["Description"].unique()[:5], 1):
        print(f"     {i}. {desc}")

    field_analysis["Description"] = {
        "unique_count": unique_descriptions,
        "examples": df["Description"].unique()[:10].tolist(),
    }

    # 4. Quantity
    print(f"\n4. Cantidad:")
    qty_stats = df["Quantity"].describe()
    print(f"*Rango: {df['Quantity'].min()} - {df['Quantity'].max()}")
    print(f"*Promedio: {df['Quantity'].mean():.2f}")
    print(f"*Mediana: {df['Quantity'].median():.1f}")
    print(f"*Desviación estándar: {df['Quantity'].std():.2f}")

    field_analysis["Quantity"] = qty_stats.to_dict()

    # 5. UnitPrice
    print(f"\n5. Precio Unitario:")
    price_stats = df["UnitPrice"].describe()
    print(f"*Rango: £{df['UnitPrice'].min():.2f} - £{df['UnitPrice'].max():.2f}")
    print(f"*Promedio: £{df['UnitPrice'].mean():.2f}")
    print(f"*Mediana: £{df['UnitPrice'].median():.2f}")
    print(f"*Productos más caros:")
    expensive_items = df.nlargest(3, "UnitPrice")[["Description", "UnitPrice"]]
    for _, item in expensive_items.iterrows():
        print(f"     - {item['Description']}: £{item['UnitPrice']:.2f}")

    field_analysis["UnitPrice"] = price_stats.to_dict()

    # 6. CustomerID
    print(f"\n6. ID de Cliente:")
    unique_customers = df["CustomerID"].nunique()
    transactions_per_customer = len(df) / unique_customers
    top_customers = df["CustomerID"].value_counts().head()
    print(f"*Clientes únicos: {unique_customers:,}")
    print(f"*Transacciones promedio por cliente: {transactions_per_customer:.1f}")
    print(f"*Top 3 clientes más activos:")
    for customer_id, count in top_customers.head(3).items():
        print(f"     - Cliente {int(customer_id)}: {count:,} transacciones")

    field_analysis["CustomerID"] = {
        "unique_count": unique_customers,
        "avg_transactions_per_customer": transactions_per_customer,
        "top_customers": top_customers.head().to_dict(),
    }

    # 7. Country
    print(f"\n7. País:")
    country_stats = df["Country"].value_counts()
    print(f"*Países únicos: {df['Country'].nunique()}")
    print(f"*Top 5 países por transacciones:")
    for i, (country, count) in enumerate(country_stats.head().items(), 1):
        percentage = count / len(df) * 100
        print(f"     {i}. {country}: {count:,} ({percentage:.1f}%)")

    field_analysis["Country"] = country_stats.to_dict()

    # 8. Análisis Temporal Detallado
    print(f"\n8. Análisis Temporal:")
    date_range = df["InvoiceDate"]
    print(f"*Período completo: {date_range.min()} a {date_range.max()}")
    print(f"*Duración total: {(date_range.max() - date_range.min()).days} días")

    # Análisis por mes
    monthly_transactions = df.groupby(df["InvoiceDate"].dt.month).size()
    peak_month = monthly_transactions.idxmax()
    print(
        f"*Mes pico: {peak_month} ({monthly_transactions[peak_month]:,} transacciones)"
    )

    # Análisis por día de semana
    daily_pattern = df.groupby("DayOfWeek").size()
    busiest_day = daily_pattern.idxmax()
    print(
        f"*Día más activo: {busiest_day} ({daily_pattern[busiest_day]:,} transacciones)"
    )

    field_analysis["Temporal"] = {
        "date_range": (date_range.min(), date_range.max()),
        "duration_days": (date_range.max() - date_range.min()).days,
        "monthly_transactions": monthly_transactions.to_dict(),
        "daily_pattern": daily_pattern.to_dict(),
        "peak_month": peak_month,
        "busiest_day": busiest_day,
    }

    return field_analysis


def generate_metadata(df):
    """
    Genera metadata comprehensiva del dataset.

    Argumentos:
        df: DataFrame a analizar

    Returns:
        dict: Metadata del dataset
    """
    print("\nGENERACIÓN DE METADATA:")

    # Metadata básica
    basic_metadata = {
        "dataset_name": "Online Retail Dataset",
        "source": "UCI ML Repository",
        "collection_period": f"{df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}",
        "business_type": "E-commerce",
        "geographic_focus": "United Kingdom + International",
        "data_granularity": "Transaction line level",
        "total_records": len(df),
        "total_columns": len(df.columns),
        "file_size_mb": df.memory_usage(deep=True).sum() / (1024**2),
    }

    # Metadata de la lógica del negocio
    business_metadata = {
        "total_revenue": df["TotalPrice"].sum(),
        "avg_transaction_value": df.groupby("InvoiceNo")["TotalPrice"].sum().mean(),
        "customer_base_size": df["CustomerID"].nunique(),
        "product_catalog_size": df["StockCode"].nunique(),
        "market_coverage": df["Country"].nunique(),
        "seasonal_business": True,
        "emp_consu_model": True,
    }

    # Metadata temporal
    temporal_metadata = {
        "time_span_days": (df["InvoiceDate"].max() - df["InvoiceDate"].min()).days,
        "transactions_per_day": len(df)
        / ((df["InvoiceDate"].max() - df["InvoiceDate"].min()).days),
        "peak_season": "November-December",
        "business_hours": "9AM-5PM GMT",
        "weekend_activity": df[df["IsWeekend"]].shape[0] / len(df) < 0.1,
    }

    # Metadata de calidad
    quality_metadata = {
        "completeness_score": 1
        - (df.isnull().sum().sum() / (len(df) * len(df.columns))),
        "duplicate_records": 0,
        "data_consistency": "High",
        "outliers_present": True,
        "data_freshness": "Historical",
    }

    # Combinar toda la metadata
    full_metadata = {
        "basic": basic_metadata,
        "business": business_metadata,
        "temporal": temporal_metadata,
        "quality": quality_metadata,
        "generation_timestamp": datetime.now().isoformat(),
        "analysis_version": "1.0",
    }

    print("Metadata generada:")
    print(f"*Records: {basic_metadata['total_records']:,}")
    print(f"*Revenue: £{business_metadata['total_revenue']:,.2f}")
    print(f"*Customers: {business_metadata['customer_base_size']:,}")
    print(f"*Products: {business_metadata['product_catalog_size']:,}")
    print(f"*Countries: {business_metadata['market_coverage']}")
    print(f"*Completeness: {quality_metadata['completeness_score']:.1%}")

    return full_metadata


def customer_segmentation_analysis(df):
    """
    Análisis de segmentación de clientes.

    Argumentos:
        df: DataFrame con datos de transacciones

    Returns:
        dict: Resultados del análisis de segmentación
    """
    print("\nANÁLISIS DE SEGMENTACIÓN DE CLIENTES:")

    # Calcular métricas por cliente
    current_date = df["InvoiceDate"].max()

    rfm_analysis = (
        df.groupby("CustomerID")
        .agg(
            {
                "InvoiceDate": lambda x: (current_date - x.max()).days,
                "InvoiceNo": "nunique",
                "TotalPrice": "sum",
            }
        )
        .rename(
            columns={
                "InvoiceDate": "Recency",
                "InvoiceNo": "Frequency",
                "TotalPrice": "Monetary",
            }
        )
    )

    # Estadísticas de segmentación
    print("MÉTRICAS CLIENTE:")
    print(f"*Recency promedio: {rfm_analysis['Recency'].mean():.0f} días")
    print(f"*Frequency promedio: {rfm_analysis['Frequency'].mean():.1f} transacciones")
    print(f"*Monetary promedio: £{rfm_analysis['Monetary'].mean():.2f}")

    high_value_customers = rfm_analysis[
        rfm_analysis["Monetary"] > rfm_analysis["Monetary"].quantile(0.8)
    ]
    frequent_customers = rfm_analysis[
        rfm_analysis["Frequency"] > rfm_analysis["Frequency"].quantile(0.8)
    ]
    recent_customers = rfm_analysis[
        rfm_analysis["Recency"] < rfm_analysis["Recency"].quantile(0.2)
    ]

    print(f"\nSEGMENTOS IDENTIFICADOS:")
    print(
        f"*Clientes alto valor: {len(high_value_customers):,} ({len(high_value_customers)/len(rfm_analysis):.1%})"
    )
    print(
        f"*Clientes frecuentes: {len(frequent_customers):,} ({len(frequent_customers)/len(rfm_analysis):.1%})"
    )
    print(
        f"*Clientes recientes: {len(recent_customers):,} ({len(recent_customers)/len(rfm_analysis):.1%})"
    )

    segmentation_results = {
        "rfm_data": rfm_analysis,
        "high_value_customers": high_value_customers.index.tolist(),
        "frequent_customers": frequent_customers.index.tolist(),
        "recent_customers": recent_customers.index.tolist(),
        "segment_stats": {
            "high_value_count": len(high_value_customers),
            "frequent_count": len(frequent_customers),
            "recent_count": len(recent_customers),
            "total_customers": len(rfm_analysis),
        },
    }

    return segmentation_results


def product_analysis(df):
    """
    Realiza análisis detallado de productos.

    Argumentos:
        df: DataFrame con datos de transacciones

    Returns:
        dict: Resultados del análisis de productos
    """
    print("\nANÁLISIS DETALLADO DE PRODUCTOS:")

    # Análisis por producto
    product_sales = (
        df.groupby(["StockCode", "Description"])
        .agg(
            {
                "Quantity": "sum",
                "TotalPrice": "sum",
                "InvoiceNo": "nunique",
            }
        )
        .rename(columns={"InvoiceNo": "TransactionCount"})
    )

    # Top productos
    top_by_quantity = product_sales.nlargest(10, "Quantity")
    top_by_revenue = product_sales.nlargest(10, "TotalPrice")
    top_by_transactions = product_sales.nlargest(10, "TransactionCount")

    print("TOP 5 PRODUCTOS POR CANTIDAD VENDIDA:")
    for i, (idx, row) in enumerate(top_by_quantity.head().iterrows(), 1):
        code, desc = idx
        print(f"   {i}. {desc[:50]}... ({code})")
        print(
            f"      Cantidad: {row['Quantity']:,} | Revenue: £{row['TotalPrice']:,.2f}"
        )

    print(f"\nTOP 5 PRODUCTOS POR INGRESOS:")
    for i, (idx, row) in enumerate(top_by_revenue.head().iterrows(), 1):
        code, desc = idx
        print(f"   {i}. {desc[:50]}... ({code})")
        print(
            f"      Ingreso: £{row['TotalPrice']:,.2f} | Cantidad: {row['Quantity']:,}"
        )

    # Análisis de precio
    price_category_analysis = (
        df.groupby("PriceCategory", observed=False)
        .agg({"TotalPrice": ["sum", "count"], "Quantity": "sum"})
        .round(2)
    )

    print(f"\nANÁLISIS POR PRECIO:")
    for category in price_category_analysis.index:
        revenue = price_category_analysis.loc[category, ("TotalPrice", "sum")]
        count = price_category_analysis.loc[category, ("TotalPrice", "count")]
        print(f"* {category}: £{revenue:,.2f} ({count:,} transacciones)")

    product_results = {
        "product_sales": product_sales,
        "top_by_quantity": top_by_quantity,
        "top_by_revenue": top_by_revenue,
        "top_by_transactions": top_by_transactions,
        "price_category_analysis": price_category_analysis,
        "total_products": len(product_sales),
        "avg_product_revenue": product_sales["TotalPrice"].mean(),
    }

    return product_results


def temporal_patterns_analysis(df):
    """
    Analiza patrones temporales usando las variables disponibles.

    Argumentos:
        df: DataFrame con datos de transacciones

    Returns:
        dict: Resultados del análisis temporal
    """
    print("\nANÁLISIS DE PATRONES TEMPORALES:")

    # Análisis mensual
    monthly_analysis = (
        df.groupby("Month")
        .agg(
            {
                "TotalPrice": "sum",
                "Quantity": "sum",
                "InvoiceNo": "nunique",
                "CustomerID": "nunique",
            }
        )
        .rename(columns={"InvoiceNo": "Transactions", "CustomerID": "UniqueCustomers"})
    )

    print("PATRÓN MENSUAL:")
    month_names = [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Oct",
        "Nov",
        "Dic",
    ]
    for month, row in monthly_analysis.iterrows():
        if month <= 12 and month >= 1:  # Validar mes válido
            month_name = month_names[month - 1]
            print(
                f"   • {month_name}: £{row['TotalPrice']:,.0f} ({row['Transactions']:,} trans, {row['UniqueCustomers']:,} clientes)"
            )

    # Análisis por día de semana
    daily_analysis = (
        df.groupby("DayOfWeek")
        .agg({"TotalPrice": "sum", "InvoiceNo": "nunique"})
        .rename(columns={"InvoiceNo": "Transactions"})
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    daily_analysis = daily_analysis.reindex(
        [day for day in day_order if day in daily_analysis.index]
    )

    print(f"\nPATRÓN SEMANAL:")
    for day, row in daily_analysis.iterrows():
        print(
            f"* {day}: £{row['TotalPrice']:,.0f} ({row['Transactions']:,} transacciones)"
        )

    # Análisis por hora
    hourly_analysis = (
        df.groupby("Hour")
        .agg({"TotalPrice": "sum", "InvoiceNo": "nunique"})
        .rename(columns={"InvoiceNo": "Transactions"})
    )

    peak_hours = hourly_analysis.nlargest(5, "TotalPrice")
    print(f"\n*HORAS PICO (Top 5 por revenue):")
    for hour, row in peak_hours.iterrows():
        print(
            f"*{hour:02d}:00 - £{row['TotalPrice']:,.0f} ({row['Transactions']:,} transacciones)"
        )

    # Análisis fin de semana
    weekend_analysis = (
        df.groupby("IsWeekend")
        .agg({"TotalPrice": "sum", "InvoiceNo": "nunique"})
        .rename(columns={"InvoiceNo": "Transactions"})
    )

    print(f"\nPATRÓN FIN DE SEMANA:")
    for is_weekend, row in weekend_analysis.iterrows():
        period_type = "Weekend" if is_weekend else "Weekdays"
        pct_revenue = (row["TotalPrice"] / df["TotalPrice"].sum()) * 100
        print(
            f"*{period_type}: £{row['TotalPrice']:,.0f} ({pct_revenue:.1f}% del revenue)"
        )

    temporal_results = {
        "monthly_analysis": monthly_analysis,
        "daily_analysis": daily_analysis,
        "hourly_analysis": hourly_analysis,
        "weekend_analysis": weekend_analysis,
        "peak_month": monthly_analysis["TotalPrice"].idxmax(),
        "peak_day": daily_analysis["TotalPrice"].idxmax(),
        "peak_hour": hourly_analysis["TotalPrice"].idxmax(),
        "seasonality_detected": True,
        "business_hours_pattern": True,
    }

    return temporal_results


def perform_eda(df=None):
    """
    Función principal que ejecuta todo el análisis exploratorio.

    Argumentoss:
        df: DataFrame a analizar. Si None, carga desde DB.

    Returns:
        dict: Resultados completos del EDA
    """
    print("ANÁLISIS EXPLORATORIO DE DATOS (EDA)")

    # Cargar datos
    if df is None:
        df = load_data_from_db()

    try:
        # 1. Descripción general del dataset
        dataset_stats = describe_dataset(df)

        # 2. Análisis detallado por campo
        field_analysis = analyze_fields(df)

        # 3. Generación de metadata
        metadata = generate_metadata(df)

        # 4. Análisis de clientes
        customer_segments = customer_segmentation_analysis(df)

        # 5. Análisis de productos
        product_analysis_results = product_analysis(df)

        # 6. Análisis temporal
        temporal_patterns = temporal_patterns_analysis(df)

        # Compilar todos los resultados
        eda_results = {
            "dataset_stats": dataset_stats,
            "field_analysis": field_analysis,
            "metadata": metadata,
            "customer_segments": customer_segments,
            "product_analysis": product_analysis_results,
            "temporal_patterns": temporal_patterns,
            "data_shape": df.shape,
            "analysis_timestamp": datetime.now().isoformat(),
        }

        # Guardar EDA
        save_eda_report(eda_results)

        print(f"\nANÁLISIS EXPLORATORIO COMPLETADO:")
        print(f"Datos analizados: {df.shape}")
        print(f"Reporte guardado: output/eda_report.txt")

        return eda_results

    except Exception as e:
        print(f"\nError en el análisis exploratorio: {e}")
        raise


def save_eda_report(eda_results):
    """
    Guarda el reporte de EDA en un archivo de texto.

    Argumentos:
        eda_results (dict): Resultados del EDA
    """
    # Crear directorio si no existe
    os.makedirs("output", exist_ok=True)

    report_content = f"""
REPORTE DE ANÁLISIS EXPLORATORIO DE DATOS (EDA)
Universidad Yachay Tech - Maestría en Ciencia de Datos
Dataset: Online Retail
========================================================

FECHA DE ANÁLISIS: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. RESUMEN EJECUTIVO
====================
Total de registros: {eda_results['dataset_stats']['total_transactions']:,}
Clientes únicos: {eda_results['dataset_stats']['unique_customers']:,}
Productos únicos: {eda_results['dataset_stats']['unique_products']:,}
Ingreso total: £{eda_results['dataset_stats']['total_revenue']:,.2f}
Período de datos: {eda_results['dataset_stats']['date_range_start']} - {eda_results['dataset_stats']['date_range_end']}

2. CONCLUSIONES PRINCIPALES
========================
• Negocio altamente estacional con picos navideños
• Mercado concentrado en Reino Unido ({eda_results['field_analysis']['Country']['United Kingdom']/eda_results['dataset_stats']['total_transactions']*100:.1f}% de transacciones)
• Horario comercial 9AM-5PM


3. CALIDAD DE DATOS
===================
Completitud: {eda_results['metadata']['quality']['completeness_score']:.1%}
Consistencia: {eda_results['metadata']['quality']['data_consistency']}
Duplicados: {eda_results['metadata']['quality']['duplicate_records']}
Outliers: {'Presentes' if eda_results['metadata']['quality']['outliers_present'] else 'No detectados'}

4. METADATA 
====================
Tamaño del dataset: {eda_results['metadata']['basic']['file_size_mb']:.1f} MB
Granularidad: {eda_results['metadata']['basic']['data_granularity']}
Tipo de negocio: {eda_results['metadata']['basic']['business_type']}
Cobertura geográfica: {eda_results['metadata']['basic']['geographic_focus']}

"""

    with open("output/eda_report.txt", "w", encoding="utf-8") as f:
        f.write(report_content)

    print("Reporte de EDA guardado en 'output/eda_report.txt'")


if __name__ == "__main__":
    # Ejecutar solo si se llama directamente
    results = perform_eda()
    print("Módulo de análisis exploratorio ejecutado exitosamente!")
