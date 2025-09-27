# Importar librerías
import os
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd


# Cargar Excel
def load_excel_data(filename="Online Retail.xlsx"):
    """
    Carga el archivo Excel del dataset Online Retail.

    Argumentos:
        filename (str): Nombre del archivo Excel a cargar

    Returns:
        pd.DataFrame: DataFrame con los datos
    """
    print("Cargando Excel")

    try:
        # Cargar Excel con pandas
        df = pd.read_excel(filename, engine="openpyxl")
        print(f"Archivo Excel cargado exitosamente: {df.shape}")
        print(f"Archivo utilizado: {filename}")
        return df

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'")
        raise

    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        raise


def analyze_data(df):
    """
    Revisa los datos e identifica problemas.

    Argumentos:
        df: DataFrame a analizar

    Returns:
        dict: Diccionario con estadísticas
    """
    print("\nANÁLISIS DE DATOS:")

    # Información general del dataframe
    print(f"Dimensiones: {df.shape}")
    print(f"Columnas: {list(df.columns)}")

    # Mostrar primeras filas
    print("\nPRIMERAS 5 FILAS:")
    print(df.head().to_string())

    # Información de tipos de datos
    print(f"\nINFORMACIÓN GENERAL:")
    print(df.info())

    # Valores nulos detallado
    print("\nANÁLISIS DE VALORES NULOS:")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100

    missing_summary = pd.DataFrame(
        {
            "Columna": missing_data.index,
            "Valores_Nulos": missing_data.values,
            "Porcentaje": missing_percent.values,
        }
    ).sort_values("Valores_Nulos", ascending=False)

    print(missing_summary.to_string(index=False))

    # Estadísticas descriptivas básicas
    print(f"\nESTADÍSTICAS DESCRIPTIVAS:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())

    # Detectar valores atípicos
    print(f"\nVALORES ATÍPICOS:")

    if "Quantity" in df.columns:
        negative_qty = (df["Quantity"] <= 0).sum()
        print(f"* Cantidades <= 0: {negative_qty:,} ({negative_qty/len(df)*100:.1f}%)")

    if "UnitPrice" in df.columns:
        negative_price = (df["UnitPrice"] <= 0).sum()
        zero_price = (df["UnitPrice"] == 0).sum()
        print(f"* Precios <= 0: {negative_price:,} ({negative_price/len(df)*100:.1f}%)")
        print(f"* Precios = 0: {zero_price:,} ({zero_price/len(df)*100:.1f}%)")

    # Duplicados
    duplicates = df.duplicated().sum()
    print(f"* Registros duplicados: {duplicates:,} ({duplicates/len(df)*100:.1f}%)")

    # Compilar estadísticas
    quality_stats = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_data": missing_data.to_dict(),
        "missing_percent": missing_percent.to_dict(),
        "duplicates": duplicates,
        "data_types": df.dtypes.to_dict(),
    }

    return quality_stats


def clean_data(df):
    """
    Limpia los datos.

    Args:
        df: DataFrame con datos sin limpiar

    Returns:
        pd.DataFrame: DataFrame con datos limpios
    """
    print("\nLIMPIEZA DE DATOS")

    df_clean = df.copy()
    initial_rows = len(df_clean)

    print(f"\nESTADO INICIAL: {initial_rows:,} registros")

    # 1. Eliminar filas con CustomerID nulo
    if "CustomerID" in df_clean.columns:
        before_customer = len(df_clean)
        df_clean = df_clean.dropna(subset=["CustomerID"])
        removed = before_customer - len(df_clean)
        print(f"\nLIMPIEZA CustomerID:")
        print(f"Eliminados: {removed:,} registros ({removed/before_customer*100:.1f}%)")
        print(f"Restantes: {len(df_clean):,} registros")

    # 2. Eliminar filas con Description nulo
    if "Description" in df_clean.columns:
        before_desc = len(df_clean)
        df_clean = df_clean.dropna(subset=["Description"])
        removed = before_desc - len(df_clean)
        print(f"\nLIMPIEZA Description:")
        print(f"Eliminados: {removed:,} registros ({removed/before_desc*100:.1f}%)")
        print(f"Lógica: Productos sin descripción no son categorizables")
        print(f"Restantes: {len(df_clean):,} registros")

    # 3. Eliminar transacciones con cantidad <= 0
    if "Quantity" in df_clean.columns:
        before_qty = len(df_clean)
        negative_qty_count = (df_clean["Quantity"] <= 0).sum()
        df_clean = df_clean[df_clean["Quantity"] > 0]
        removed = before_qty - len(df_clean)
        print(f"\nLIMPIEZA Quantity:")
        print(f"Eliminados: {removed:,} registros ({removed/before_qty*100:.1f}%)")
        print(f"Lógica: Cantidades ≤0 son devoluciones, cancelaciones o errores")
        print(f"Restantes: {len(df_clean):,} registros")

        # Ejemplos de cantidades negativas eliminadas
        if negative_qty_count > 0:
            print(
                f"Ejemplos eliminados: Cantidades desde {df[df['Quantity'] <= 0]['Quantity'].min()} hasta 0"
            )

    # 4. Eliminar precio <= 0
    if "UnitPrice" in df_clean.columns:
        before_price = len(df_clean)
        zero_price_count = (df_clean["UnitPrice"] <= 0).sum()
        df_clean = df_clean[df_clean["UnitPrice"] > 0]
        removed = before_price - len(df_clean)
        print(f"\n LIMPIEZA UnitPrice:")
        print(f"Eliminados: {removed:,} registros ({removed/before_price*100:.1f}%)")
        print(f"Restantes: {len(df_clean):,} registros")

        if zero_price_count > 0:
            print(f"Precios £0.00 eliminados: {zero_price_count:,} registros")

    # 5. Eliminar duplicados exactos
    before_dup = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    removed = before_dup - len(df_clean)
    print(f"\nLIMPIEZA Duplicados:")
    print(f"Eliminados: {removed:,} registros duplicados exactos")
    print(f"Restantes: {len(df_clean):,} registros")

    # 6. Validar consistencia de datos
    print(f"\nVALIDACIÓN DE CONSISTENCIA:")

    # Verificar que no hay valores negativos después de limpieza
    if "Quantity" in df_clean.columns:
        assert df_clean["Quantity"].min() > 0, "Error: Aún hay cantidades <= 0"
        print(
            f"Quantity: Rango válido [{df_clean['Quantity'].min()}, {df_clean['Quantity'].max()}]"
        )

    if "UnitPrice" in df_clean.columns:
        assert df_clean["UnitPrice"].min() > 0, "Error: Aún hay precios <= 0"
        print(
            f"UnitPrice: Rango válido [£{df_clean['UnitPrice'].min():.2f}, £{df_clean['UnitPrice'].max():.2f}]"
        )

    # Verificar integridad referencial básica
    if "CustomerID" in df_clean.columns:
        assert df_clean["CustomerID"].notna().all(), "Error: Aún hay CustomerID nulos"
        print(
            f"CustomerID: {df_clean['CustomerID'].nunique():,} clientes únicos sin nulos"
        )

    # Resumen final
    total_removed = initial_rows - len(df_clean)
    retention_rate = (len(df_clean) / initial_rows) * 100

    print(f"\nRESUMEN FINAL:")
    print(f"Registros iniciales: {initial_rows:,}")
    print(f"Registros eliminados: {total_removed:,} ({100-retention_rate:.1f}%)")
    print(f"Registros finales: {len(df_clean):,}")
    print(f"Porcentaje datos correctos: {retention_rate:.1f}%")
    print(f" Datos listos para análisis")

    return df_clean


def create_derived_variables(df):
    """
    Crea variables adicionales

    Args:
        df : DataFrame con datos limpios

    Returns:
        pd.DataFrame: DataFrame con variables adicionales
    """
    print("\n CREAR VARIABLES ADCIONALES")
    print("-" * 50)

    df_enhanced = df.copy()

    # 1. Variable: TotalPrice del precio total
    print("VARIABLES PRINCIPALES:")
    df_enhanced["TotalPrice"] = df_enhanced["Quantity"] * df_enhanced["UnitPrice"]

    print(
        f"Rango: £{df_enhanced['TotalPrice'].min():.2f} - £{df_enhanced['TotalPrice'].max():.2f}"
    )
    print(f"Promedio: £{df_enhanced['TotalPrice'].mean():.2f}")

    # 2. Variables temporales
    if "InvoiceDate" in df_enhanced.columns:
        print(f"\nVARIABLES TEMPORALES:")

        # Convertir a datetime si no lo está
        df_enhanced["InvoiceDate"] = pd.to_datetime(df_enhanced["InvoiceDate"])

        # Separar variables temporales
        df_enhanced["Month"] = df_enhanced["InvoiceDate"].dt.month
        df_enhanced["Hour"] = df_enhanced["InvoiceDate"].dt.hour
        df_enhanced["DayOfWeek"] = df_enhanced["InvoiceDate"].dt.day_name()
        # Variables booleanas temporales
        df_enhanced["IsWeekend"] = df_enhanced["InvoiceDate"].dt.dayofweek >= 5

        print(
            f"Período de datos: {df_enhanced['InvoiceDate'].min()} a {df_enhanced['InvoiceDate'].max()}"
        )

    # 3. Categorización de precios
    if "UnitPrice" in df_enhanced.columns:
        print(f"\nCATEGORIZACIÓN DE PRECIOS:")

        price_bins = [0, 2, 5, 10, 25, float("inf")]
        price_labels = ["Muy Bajo", "Bajo", "Medio", "Alto", "Premium"]

        df_enhanced["PriceCategory"] = pd.cut(
            df_enhanced["UnitPrice"],
            bins=price_bins,
            labels=price_labels,
            right=False,
            include_lowest=True,
        )

        print(f"PriceCategory: {price_labels}")
        print(f"Distribución por categoría:")
        for category in price_labels:
            count = (df_enhanced["PriceCategory"] == category).sum()
            pct = count / len(df_enhanced) * 100
            print(f"*{category}: {count:,} ({pct:.1f}%)")

    print(f"\nVARIABLES ADICIONALES:")
    print(f"Columnas iniciales: {len(df.columns)}")
    print(f"Columnas finales: {len(df_enhanced.columns)}")
    print(f"Variables añadidas: {len(df_enhanced.columns) - len(df.columns)}")
    print(f"Forma final del dataset: {df_enhanced.shape}")

    return df_enhanced


def save_to_database(
    df, db_name="data/online_retail.db", table_name="online_retail_clean"
):
    """
    Guarda los datos limpios en una base de datos SQLite.

    Argumentos:
        df : DataFrame a guardar
        db_name (str): Nombre del archivo de base de datos
        table_name (str): Nombre de la tabla
    """
    print("\n GUARDANDO EN BASE DE DATOS SQLITE ")

    # Crear directorio si no existe
    db_dir = os.path.dirname(db_name)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        print(f" Directorio : {db_dir}/")

    try:
        # Conectar a SQLite
        conn = sqlite3.connect(db_name)
        print(f" Conexión establecida: {db_name}")

        # Guardar datos principales en chunks para evitar límite de SQLite
        chunk_size = 1000
        total_rows = len(df)
        print(f"Guardando {total_rows:,} registros en chunks de {chunk_size:,}...")
        df.iloc[:chunk_size].to_sql(table_name, conn, if_exists="replace", index=False)
        # Guardar en chunks
        for i in range(chunk_size, total_rows, chunk_size):
            chunk_end = min(i + chunk_size, total_rows)
            chunk = df.iloc[i:chunk_end]
            chunk.to_sql(table_name, conn, if_exists="append", index=False)
            progress = (chunk_end / total_rows) * 100
            print(f"Progreso: {progress:.1f}% ({chunk_end:,}/{total_rows:,} registros)")

        print(f"Datos guardados exitosamente en tabla: {table_name}")

        indices = [
            f"CREATE INDEX IF NOT EXISTS idx_customer ON {table_name} (CustomerID)",
            f"CREATE INDEX IF NOT EXISTS idx_invoice ON {table_name} (InvoiceNo)",
            f"CREATE INDEX IF NOT EXISTS idx_date ON {table_name} (InvoiceDate)",
            f"CREATE INDEX IF NOT EXISTS idx_country ON {table_name} (Country)",
            f"CREATE INDEX IF NOT EXISTS idx_stock ON {table_name} (StockCode)",
        ]

        for idx_sql in indices:
            conn.execute(idx_sql)

        # Commit cambios
        conn.commit()

        # Verificar guardado y obtener estadísticas
        query_test = f"SELECT COUNT(*) as total_records FROM {table_name}"
        result = pd.read_sql_query(query_test, conn)
        total_records = result.iloc[0, 0]

        print(f"\nVERIFICACIÓN DE BASE DE DATOS:")
        print(f"Registros guardados: {total_records:,}")

        # Obtener información del schema
        schema_query = f"PRAGMA table_info({table_name})"
        schema_info = pd.read_sql_query(schema_query, conn)
        print(f"Columnas en tabla: {len(schema_info)}")

        # Mostrar  columnas
        key_columns = ["InvoiceNo", "CustomerID", "TotalPrice", "InvoiceDate"]
        existing_key_cols = [col for col in key_columns if col in df.columns]

        if existing_key_cols:
            sample_query = (
                f"SELECT {', '.join(existing_key_cols)} FROM {table_name} LIMIT 3"
            )
            sample_data = pd.read_sql_query(sample_query, conn)
            print(f"Muestra de datos guardados:")
            print(sample_data.to_string(index=False))

        print(f"\nBASE DE DATOS CREADA ")
        print(f"Ubicación: {os.path.abspath(db_name)}")
        print(f"Tabla: {table_name}")

    except Exception as e:
        print(f"Error al guardar en base de datos: {e}")
        raise
    finally:
        conn.close()
        print(f"Conexión a base de datos cerrada")


def load_and_clean_data():
    """
    Función principal que ejecuta todo el proceso.

    Returns:
        pd.DataFrame: DataFrame con datos limpios
    """

    try:
        # 1. Cargar datos desde Excel
        print("\nPASO 1: CARGA DE DATOS")
        df_raw = load_excel_data()

        # 2. Analizar datos
        print("\nPASO 2: ANÁLISIS DE CALIDAD")
        quality_stats = analyze_data(df_raw)

        # 3. Limpiar datos
        print("\nPASO 3: LIMPIEZA DE DATOS")
        df_clean = clean_data(df_raw)

        # 4. Crear variables
        print("\nPASO 4: CREACIÓN DE VARIABLES")
        df_enhanced = create_derived_variables(df_clean)

        # 5. Guardar en base de datos
        print("\nPASO 5: ALMACENAMIENTO EN BASE DE DATOS")
        save_to_database(df_enhanced)

        # Resumen final
        print(f"\nRESUMEN:")
        print(f"*Registros originales: {len(df_raw):,}")
        print(f"*Registros después de limpieza: {len(df_clean):,}")
        print(f"*Registros finales: {len(df_enhanced):,}")
        print(f"*Columnas finales: {len(df_enhanced.columns)}")
        print(f"*Base de datos: data/online_retail.db")
        print(f"*Datos listos para análisis exploratorio")

        return df_enhanced

    except Exception as e:
        print(f"\nERROR EN EL PROCESO DE ADQUISICIÓN Y LIMPIEZA:")
        print(f"Error: {str(e)}")
        print(f"Tipo: {type(e).__name__}")
        raise


if __name__ == "__main__":

    print("Ejecutando módulo de adquisición y limpieza de datos")
    df_result = load_and_clean_data()
    print(f"\nTarea finalizada")
    print(f"Dataset final: {df_result.shape}")
    print(f"Columnas disponibles: {list(df_result.columns)}")
