# Importar librerías
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def setup_visualization_style():
    """
    Configura el estilo global para las visualizaciones.
    """
    plt.style.use("default")
    sns.set_palette("husl")
    plt.rcParams["figure.figsize"] = (16, 12)
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["xtick.labelsize"] = 10
    plt.rcParams["ytick.labelsize"] = 10

    # Colores personalizados
    colors = [
        "#2E86AB",
        "#A23B72",
        "#F18F01",
        "#C73E1D",
        "#6A994E",
        "#9A031E",
        "#FB8500",
    ]
    return colors


def create_temporal_analysis_visualization(df):
    """
    Crea visualización completa del análisis temporal usando variables disponibles.

    Argumentoss:
        df: DataFrame con datos de transacciones

    Returns:
        str: Nombre del archivo guardado
    """
    print("Visualización 1: Análisis Temporal")

    colors = setup_visualization_style()

    # Crear figura con subplots y mejor spacing
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(22, 18))
    fig.suptitle(
        "Análisis Temporal - Online Retail Dataset",
        fontsize=24,
        fontweight="bold",
        y=0.98,
    )

    plt.subplots_adjust(
        top=0.92, bottom=0.08, left=0.08, right=0.95, hspace=0.35, wspace=0.25
    )

    # 1. Ingreso mensual
    monthly_revenue = df.groupby("Month")["TotalPrice"].sum()
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

    # Filtrar solo los meses que existen en los datos
    existing_months = monthly_revenue.index.tolist()
    month_labels = [month_names[i - 1] for i in existing_months if 1 <= i <= 12]

    ax1.plot(
        month_labels,
        monthly_revenue.values,
        marker="o",
        linewidth=4,
        markersize=10,
        color=colors[0],
        markerfacecolor="white",
        markeredgewidth=2,
    )
    ax1.fill_between(
        range(len(month_labels)), monthly_revenue.values, alpha=0.3, color=colors[0]
    )
    ax1.set_title("Ingreso Mensual", fontsize=16, pad=20)
    ax1.set_ylabel("Ingreso (£)", fontsize=13, fontweight="bold")
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(True, alpha=0.3, linestyle="--")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"£{x/1000:.0f}K"))

    # Añadir anotaciones para picos
    max_idx = monthly_revenue.idxmax()
    max_val = monthly_revenue.max()
    peak_position = list(existing_months).index(max_idx)
    ax1.annotate(
        f"Pico: £{max_val/1000:.0f}K",
        xy=(peak_position, max_val),
        xytext=(peak_position, max_val * 1.1),
        arrowprops=dict(arrowstyle="->", color="red", lw=2),
        fontsize=12,
        ha="center",
        fontweight="bold",
    )

    # 2. Transacciones por día de la semana
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    daily_transactions = df.groupby("DayOfWeek")["InvoiceNo"].nunique()

    # Reindexar solo con días que existen en los datos
    existing_days = [day for day in day_order if day in daily_transactions.index]
    daily_transactions_ordered = daily_transactions.reindex(existing_days)

    bars1 = ax2.bar(
        range(len(existing_days)),
        daily_transactions_ordered.values,
        color=colors[1],
        alpha=0.8,
        edgecolor="black",
        linewidth=1,
    )
    ax2.set_title("Patrón Semanal - Transacciones por Día", fontsize=16, pad=20)
    ax2.set_ylabel("Número de Transacciones", fontsize=13, fontweight="bold")
    ax2.set_xlabel("Día de la Semana", fontsize=13, fontweight="bold")
    ax2.set_xticks(range(len(existing_days)))
    ax2.set_xticklabels([day[:3] for day in existing_days])

    # Destacar días laborales vs fines de semana
    for i, (bar, day) in enumerate(zip(bars1, existing_days)):
        height = bar.get_height()
        if day in ["Saturday", "Sunday"]:  # Weekend
            bar.set_alpha(0.5)
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + height * 0.01,
            f"{int(height):,}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    # Línea promedio
    avg_transactions = daily_transactions_ordered.mean()
    ax2.axhline(y=avg_transactions, color="red", linestyle="--", linewidth=2, alpha=0.7)
    ax2.text(
        len(existing_days) - 1,
        avg_transactions * 1.05,
        f"Promedio: {avg_transactions:.0f}",
        ha="right",
        va="bottom",
        fontsize=11,
        color="red",
        fontweight="bold",
    )

    # 3. Heatmap de ventas por hora y día
    pivot_hour_day = (
        df.groupby(["DayOfWeek", "Hour"])["TotalPrice"].sum().unstack(fill_value=0)
    )
    pivot_hour_day = pivot_hour_day.reindex(
        [day for day in day_order if day in pivot_hour_day.index]
    )

    im1 = ax3.imshow(
        pivot_hour_day.values, aspect="auto", cmap="YlOrRd", interpolation="bilinear"
    )
    ax3.set_title("Heatmap: Intensidad de Ventas (Día × Hora)", fontsize=16, pad=20)
    ax3.set_xlabel("Hora del Día", fontsize=13, fontweight="bold")
    ax3.set_ylabel("Día de la Semana", fontsize=13, fontweight="bold")

    # Configurar ejes del heatmap
    hours_available = sorted(df["Hour"].unique())
    ax3.set_xticks(range(0, len(hours_available), max(1, len(hours_available) // 12)))
    ax3.set_xticklabels(
        [
            f"{hours_available[i]}:00"
            for i in range(0, len(hours_available), max(1, len(hours_available) // 12))
        ]
    )
    ax3.set_yticks(range(len(pivot_hour_day.index)))
    ax3.set_yticklabels([day[:3] for day in pivot_hour_day.index])

    # Color para heatmap
    cbar1 = plt.colorbar(im1, ax=ax3, shrink=0.8)
    cbar1.set_label("Ventas (£)", fontsize=12, fontweight="bold")

    # 4. Top países por ingresos
    country_revenue = (
        df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=True).tail(8)
    )

    bars2 = ax4.barh(
        range(len(country_revenue)),
        country_revenue.values,
        color=colors[3],
        alpha=0.8,
        edgecolor="black",
        linewidth=1,
    )
    ax4.set_title("Top 8 Países por Ingreso Total", fontsize=16, pad=20)
    ax4.set_xlabel("Ingreso Total (£)", fontsize=13, fontweight="bold")
    ax4.set_yticks(range(len(country_revenue)))
    ax4.set_yticklabels(country_revenue.index, fontsize=11)
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"£{x/1000:.0f}K"))

    # Añadir valores en las barras
    for i, bar in enumerate(bars2):
        width = bar.get_width()
        ax4.text(
            width + width * 0.01,
            bar.get_y() + bar.get_height() / 2.0,
            f"£{int(width/1000):,}K",
            ha="left",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Guardar visualización
    os.makedirs("output", exist_ok=True)
    filename = "output/visualizacion_1_analisis_temporal.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()

    print(f"Visualización temporal guardada: {filename}")
    return filename


def create_customer_product_analysis_visualization(df):
    """
    Crea visualización del análisis de productos y clientes.

    Argumentos:
        df: DataFrame con datos de transacciones

    Returns:
        str: Nombre del archivo guardado
    """
    print("Visualización 2: Análisis de Productos y Clientes")

    colors = setup_visualization_style()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(22, 18))
    fig.suptitle(
        "Análisis de Productos y de Clientes",
        fontsize=24,
        fontweight="bold",
        y=0.98,
    )

    plt.subplots_adjust(
        top=0.92, bottom=0.08, left=0.08, right=0.95, hspace=0.4, wspace=0.25
    )

    # 1. Distribución de precios con Kernel
    prices = df["UnitPrice"]
    # Filtrar outliers extremos para mejor visualización
    price_95th = prices.quantile(0.95)
    prices_filtered = prices[prices <= price_95th]

    ax1.hist(
        prices_filtered,
        bins=50,
        alpha=0.7,
        color=colors[0],
        edgecolor="black",
        linewidth=0.5,
        density=True,
    )

    try:
        from scipy import stats

        kde = stats.gaussian_kde(prices_filtered)
        x_range = np.linspace(prices_filtered.min(), prices_filtered.max(), 100)
        ax1.plot(x_range, kde(x_range), color="red", linewidth=3, label="Densidad KDE")
        ax1.legend(fontsize=12)
    except ImportError:
        pass

    ax1.set_title(
        "Distribución de Precios Unitarios (95% de datos)", fontsize=16, pad=20
    )
    ax1.set_xlabel("Precio Unitario (£)", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Densidad", fontsize=13, fontweight="bold")
    ax1.grid(True, alpha=0.3)

    # Estadísticas en el gráfico
    mean_price = prices_filtered.mean()
    median_price = prices_filtered.median()
    ax1.axvline(mean_price, color="green", linestyle="--", linewidth=2, alpha=0.8)
    ax1.axvline(median_price, color="orange", linestyle="--", linewidth=2, alpha=0.8)
    ax1.text(
        0.7,
        0.8,
        f"Media: £{mean_price:.2f}\nMediana: £{median_price:.2f}",
        transform=ax1.transAxes,
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
    )

    # 2. Top 12 productos más vendidos
    product_sales = (
        df.groupby("Description")["Quantity"].sum().sort_values(ascending=True).tail(12)
    )

    product_names = [
        name[:35] + "..." if len(name) > 35 else name for name in product_sales.index
    ]

    bars3 = ax2.barh(
        range(len(product_sales)),
        product_sales.values,
        color=colors[1],
        alpha=0.8,
        edgecolor="black",
        linewidth=0.5,
    )
    ax2.set_yticks(range(len(product_sales)))
    ax2.set_yticklabels(product_names, fontsize=10)
    ax2.set_title("Top 12 Productos Más Vendidos por Cantidad", fontsize=16, pad=20)
    ax2.set_xlabel("Cantidad Total Vendida", fontsize=13, fontweight="bold")

    # Gradiente de colores para las barras
    for i, bar in enumerate(bars3):
        bar.set_color(plt.cm.viridis(i / len(bars3)))
        width = bar.get_width()
        ax2.text(
            width + width * 0.01,
            bar.get_y() + bar.get_height() / 2.0,
            f"{int(width):,}",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold",
        )

    # 3. Análisis - Frecuencia vs Monetario
    customer_analysis = (
        df.groupby("CustomerID")
        .agg({"InvoiceNo": "nunique", "TotalPrice": "sum"})  # Frecuencia  # Monetario
        .rename(columns={"InvoiceNo": "Frequency", "TotalPrice": "Monetary"})
    )

    # Scatter plot con densidad
    scatter = ax3.scatter(
        customer_analysis["Frequency"],
        customer_analysis["Monetary"],
        alpha=0.6,
        c=customer_analysis["Monetary"],
        cmap="viridis",
        s=50,
        edgecolors="black",
        linewidth=0.5,
    )

    ax3.set_title(
        "Análisis: Frecuencia vs Valor Monetario por Cliente", fontsize=16, pad=20
    )
    ax3.set_xlabel(
        "Frecuencia de Compra (# Transacciones)", fontsize=13, fontweight="bold"
    )
    ax3.set_ylabel("Valor Monetario Total (£)", fontsize=13, fontweight="bold")
    ax3.set_yscale("log")
    ax3.grid(True, alpha=0.3)

    # Colorbar para scatter
    cbar2 = plt.colorbar(scatter, ax=ax3)
    cbar2.set_label("Valor Monetario (£)", fontsize=12, fontweight="bold")

    # Líneas de segmentación
    freq_median = customer_analysis["Frequency"].median()
    monetary_median = customer_analysis["Monetary"].median()
    ax3.axvline(freq_median, color="red", linestyle="--", alpha=0.7, linewidth=2)
    ax3.axhline(monetary_median, color="red", linestyle="--", alpha=0.7, linewidth=2)

    # Etiquetas de cuadrantes
    ax3.text(
        0.25,
        0.85,
        "Bajo Valor\nBaja Frecuencia",
        transform=ax3.transAxes,
        ha="center",
        va="center",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.5),
    )
    ax3.text(
        0.75,
        0.85,
        "Alto Valor\nBaja Frecuencia",
        transform=ax3.transAxes,
        ha="center",
        va="center",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.5),
    )

    # 4. Análisis de categorías de productos por ingresos
    if "PriceCategory" in df.columns:
        category_analysis = df.groupby("PriceCategory", observed=False).agg(
            {"TotalPrice": "sum", "Quantity": "sum", "CustomerID": "nunique"}
        )

        # Gráfico de barras apiladas
        x_pos = range(len(category_analysis))
        width = 0.35

        bars4a = ax4.bar(
            [x - width / 2 for x in x_pos],
            category_analysis["TotalPrice"] / 1000,
            width,
            label="Ingresos (£K)",
            color=colors[2],
            alpha=0.8,
            edgecolor="black",
        )

        # Eje secundario para cantidad
        ax4_twin = ax4.twinx()
        bars4b = ax4_twin.bar(
            [x + width / 2 for x in x_pos],
            category_analysis["Quantity"],
            width,
            label="Cantidad Vendida",
            color=colors[4],
            alpha=0.8,
            edgecolor="black",
        )

        ax4.set_title(
            "Ingresos y Cantidad por Categoría de Precio", fontsize=16, pad=20
        )
        ax4.set_xlabel("Categoría de Precio", fontsize=13, fontweight="bold")
        ax4.set_ylabel("Ingresos(£K)", fontsize=13, fontweight="bold", color=colors[2])
        ax4_twin.set_ylabel(
            "Cantidad Vendida", fontsize=13, fontweight="bold", color=colors[4]
        )

        ax4.set_xticks(x_pos)
        ax4.set_xticklabels(category_analysis.index, rotation=45, ha="right")
        ax4.tick_params(axis="y", labelcolor=colors[2])
        ax4_twin.tick_params(axis="y", labelcolor=colors[4])

        # Añadir valores en las barras
        for bar, val in zip(bars4a, category_analysis["TotalPrice"] / 1000):
            height = bar.get_height()
            ax4.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + height * 0.01,
                f"£{val:.0f}K",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        for bar, val in zip(bars4b, category_analysis["Quantity"]):
            height = bar.get_height()
            ax4_twin.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + height * 0.01,
                f"{val:,.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        # Leyendas
        ax4.legend(loc="upper center", fontsize=12)
        ax4_twin.legend(loc="upper right", fontsize=12)

    # Guardar con tight_layout final
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Dejar espacio para suptitle

    # Guardar visualización
    filename = "output/visualizacion_2_productos_clientes.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()

    print(f"Visualización de productos y clientes guardada: {filename}")
    return filename


def create_advanced_analytics_visualization(df):
    """
    Crea visualización de análisis avanzado usando solo las variables disponibles.

    Args:
        df: DataFrame con datos de transacciones

    Returns:
        str: Nombre del archivo guardado
    """
    print("Visualización 3: Estacionalidad")

    colors = setup_visualization_style()

    # Crear figura con 2x2 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(22, 18))
    fig.suptitle(
        "Análisis Patrones",
        fontsize=24,
        fontweight="bold",
        y=0.98,
    )

    plt.subplots_adjust(
        top=0.92, bottom=0.08, left=0.08, right=0.95, hspace=0.4, wspace=0.3
    )

    # Gráfico 1: Top países por cantidad de clientes (ax1)
    country_customers = (
        df.groupby("Country")["CustomerID"]
        .nunique()
        .sort_values(ascending=True)
        .tail(8)
    )

    bars1 = ax1.barh(
        range(len(country_customers)),
        country_customers.values,
        color=colors[2],
        alpha=0.8,
        edgecolor="black",
        linewidth=1,
    )
    ax1.set_title("Top 8 Países por Número de Clientes", fontsize=16, pad=20)
    ax1.set_xlabel("Número de Clientes Únicos", fontsize=13, fontweight="bold")
    ax1.set_yticks(range(len(country_customers)))
    ax1.set_yticklabels(country_customers.index, fontsize=11)

    for i, bar in enumerate(bars1):
        width = bar.get_width()
        ax1.text(
            width + width * 0.01,
            bar.get_y() + bar.get_height() / 2.0,
            f"{int(width):,}",
            ha="left",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    # Gráfico 2: Análisis de estacionalidad usando Month (ax2)
    if "Month" in df.columns:
        monthly_metrics = (
            df.groupby("Month")
            .agg({"TotalPrice": "sum", "CustomerID": "nunique", "InvoiceNo": "nunique"})
            .reset_index()
        )

        # Normalizar para visualización
        monthly_metrics["Revenue_Norm"] = (
            monthly_metrics["TotalPrice"] / monthly_metrics["TotalPrice"].max() * 100
        )
        monthly_metrics["Customers_Norm"] = (
            monthly_metrics["CustomerID"] / monthly_metrics["CustomerID"].max() * 100
        )
        monthly_metrics["Transactions_Norm"] = (
            monthly_metrics["InvoiceNo"] / monthly_metrics["InvoiceNo"].max() * 100
        )

        x_months = monthly_metrics["Month"]
        ax2.plot(
            x_months,
            monthly_metrics["Revenue_Norm"],
            marker="o",
            linewidth=3,
            markersize=8,
            label="Ingresos",
            color=colors[0],
        )
        ax2.plot(
            x_months,
            monthly_metrics["Customers_Norm"],
            marker="s",
            linewidth=3,
            markersize=8,
            label="Clientes Únicos",
            color=colors[1],
        )
        ax2.plot(
            x_months,
            monthly_metrics["Transactions_Norm"],
            marker="^",
            linewidth=3,
            markersize=8,
            label="Transacciones",
            color=colors[2],
        )

        ax2.set_title("Estacionalidad Normalizada", fontsize=16, pad=20)
        ax2.set_xlabel("Mes", fontsize=13, fontweight="bold")
        ax2.set_ylabel("Índice Normalizado", fontsize=13, fontweight="bold")
        ax2.set_xticks(range(1, 13))
        ax2.set_xticklabels(
            [
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
        )
        ax2.legend(fontsize=12, loc="upper left")
        ax2.grid(True, alpha=0.3)

        # Destacar temporada alta (Nov-Dic)
        peak_months = monthly_metrics.nlargest(2, "TotalPrice")["Month"].values
        for month in peak_months:
            ax2.axvline(x=month, color="red", linestyle="--", alpha=0.5)

        ax2.text(
            0.75,
            0.95,
            "Temporada\nNavideña",
            transform=ax2.transAxes,
            ha="center",
            va="top",
            fontsize=12,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8),
        )

    # Gráfico 3: Distribución Ingresos Días de la semana vs Fin de semana (ax3)
    if "IsWeekend" in df.columns:
        weekend_analysis = (
            df.groupby("IsWeekend")
            .agg({"TotalPrice": "sum", "InvoiceNo": "nunique"})
            .rename(columns={"InvoiceNo": "Transactions"})
        )

        labels = ["Días Laborales", "Fines de Semana"]
        sizes = weekend_analysis["TotalPrice"].values
        colors_pie = [colors[2], colors[3]]

        wedges, texts, autotexts = ax3.pie(
            sizes,
            labels=labels,
            colors=colors_pie,
            autopct="%1.1f%%",
            startangle=90,
            explode=(0.05, 0),
        )

        ax3.set_title(
            "Distribución Ingresos: Días de la semana vs Fin de semana",
            fontsize=16,
            pad=20,
        )

        # Mejorar texto del pie chart
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
            autotext.set_fontsize(12)

    # Gráfico 4: Distribución de transacciones por valor (ax4)
    transaction_values = df.groupby("InvoiceNo")["TotalPrice"].sum()

    # Crear bins logarítmicos
    bins = np.logspace(
        np.log10(max(transaction_values.min(), 0.1)),
        np.log10(transaction_values.max()),
        25,
    )

    n, bins_used, patches = ax4.hist(
        transaction_values,
        bins=bins,
        alpha=0.8,
        color=colors[3],
        edgecolor="black",
        linewidth=0.8,
    )

    # Colorear barras según altura con mejor gradiente
    for i, patch in enumerate(patches):
        patch.set_facecolor(plt.cm.viridis(n[i] / n.max()))

    ax4.set_title(
        "Distribución de Valores de Transacciones",
        fontsize=18,
        pad=25,
        fontweight="bold",
    )
    ax4.set_xlabel(
        "Valor de Transacción (£) - Escala Log", fontsize=14, fontweight="bold"
    )
    ax4.set_ylabel("Frecuencia", fontsize=14, fontweight="bold")
    ax4.set_xscale("log")
    ax4.grid(True, alpha=0.3, linewidth=0.8)

    # Estadísticas más visibles
    mean_trans = transaction_values.mean()
    median_trans = transaction_values.median()
    ax4.axvline(
        mean_trans,
        color="green",
        linestyle="--",
        linewidth=3,
        alpha=0.9,
        label=f"Media: £{mean_trans:.2f}",
    )
    ax4.axvline(
        median_trans,
        color="orange",
        linestyle="--",
        linewidth=3,
        alpha=0.9,
        label=f"Mediana: £{median_trans:.2f}",
    )
    ax4.legend(fontsize=13, loc="upper right")

    # Guardar con tight_layout final
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Guardar visualización
    filename = "output/visualizacion_3_analisis_patrones.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()

    print(f"Visualización de análisis patrones guardada: {filename}")
    return filename


def create_all_visualizations(df):
    """
    Crea todas las visualizaciones del taller.

    Argumentoss:
        df: DataFrame con datos de transacciones

    Returns:
        dict: Diccionario con nombres de archivos generados
    """

    print("CREANDO TODAS LAS VISUALIZACIONES")

    # Crear directorio de output si no existe
    os.makedirs("output", exist_ok=True)

    try:
        # Configurar estilo global
        setup_visualization_style()

        # Crear las tres visualizaciones principales
        viz_files = {}

        viz_files["temporal"] = create_temporal_analysis_visualization(df)
        viz_files["products_customers"] = (
            create_customer_product_analysis_visualization(df)
        )
        viz_files["advanced"] = create_advanced_analytics_visualization(df)

        # Crear interpretación de las visualizaciones
        create_visualization_interpretation()

        print(f"\nTODAS LAS VISUALIZACIONES COMPLETADAS:")
        for viz_type, filename in viz_files.items():
            print(f" {viz_type.replace('_', ' ').title()}: {filename}")

        return viz_files

    except Exception as e:
        print(f"\nError al crear visualizaciones: {e}")
        raise


def create_visualization_interpretation():
    """
    Crea un archivo con la interpretación de las visualizaciones.
    """
    interpretation_content = """
INTERPRETACIÓN DE VISUALIZACIONES
Universidad Yachay Tech - Maestría en Ciencia de Datos
=====================================================

VISUALIZACIÓN 1: ANÁLISIS TEMPORAL
====================================


Ingreso Mensual:
• Clara estacionalidad con pico masivo en noviembre-diciembre (temporada navideña)
• Patrón descendente enero-febrero (post-navidad)
• Sugiere negocio altamente dependiente de compras estacionales

Patrón Semanal:
• Días laborales (mar-jue) muestran mayor actividad transaccional
• Actividad significativamente reducida en fines de semana

Heatmap Temporal:
• Actividad concentrada en horario comercial británico 9AM-5PM  
• Picos de intensidad martes-jueves entre 11AM-2PM
 

Distribución Geográfica:
• Reino Unido domina completamente con >80% de las transacciones
• Concentración geográfica indica dependencia de mercado doméstico

VISUALIZACIÓN 2: PRODUCTOS Y CLIENTES
=======================================

Distribución de Precios:
• Mayoría de productos concentrados en rango £0.50-£5.00 
• Distribución sesgada hacia precios económicos con cola larga hacia precios altos


Top Productos Más Vendidos:
• Dominan artículos navideños y decorativos estacionales
• Artículos específicos de temporada en top ventas confirman estacionalidad del negocio


Análisis (Frecuencia vs Monetario):
• Concentración de clientes de alto valor en frecuencias bajas (compras ocasionales grandes)
• Mayoría son compradores de bajo valor y baja frecuencia


Análisis por Categoría de Precio:
• Productos económicos generan mayor volumen de transacciones
• Productos premium contribuyen desproporcionadamente al margen


VISUALIZACIÓN 3: ANÁLISIS PATRONESs
===================================


Estacionalidad Normalizada:
• Todos los métricas (Ingresos, clientes, transacciones) siguen patrón estacional similar
• Noviembre-diciembre concentran picos en todas las dimensiones
• Enero-febrero representan valle crítico en todas las métricas

Top 8 Países por Número de Clientes:
• Dominancia del Reino Unido  como mercado principal y más importante para el negocio.
• Mercados secundarios significativos Alemania, Francia y España 

Análisis Fines de semana vs Días laborables:
• Días laborales dominan completamente 

Distribución de Valores de Transacciones:
• Sesgo hacia valores bajos, la distribución muestra que la mayoría de las transacciones son de valor bajo a moderado 
• Media: £479.56 - Valor promedio de las transacciones
• Mediana: £302.57 - Punto donde el 50% de las transacciones son menores y 50% mayores

CONCLUSIONES  
=============================

1. DEPENDENCIA ESTACIONAL CRÍTICA:
   • 60%+ del ingreso anual concentrado en Nov-Dic
   • Necesidad urgente de productos y estrategias anti-estacionales

2. CONCENTRACIÓN GEOGRÁFICA LIMITANTE:
   • Mercado UK representa >80% pero tiene límites de crecimiento
   • Oportunidades internacionales masivas sin explotar

3. SEGMENTACIÓN DE CLIENTES CLARA PERO SUBEXPLOTADA:
   • Base de clientes diversa con oportunidades de personalización


La combinación de análisis temporal y geográfico proporciona
una base para decisiones informadas y medibles.
"""

    with open("output/interpretacion_visualizaciones.txt", "w", encoding="utf-8") as f:
        f.write(interpretation_content)

    print(
        "Interpretación de visualizaciones guardada: output/interpretacion_visualizaciones.txt"
    )


if __name__ == "__main__":
    # Ejecutar solo si se llama directamente
    print("Módulo de visualizaciones listo para ejecutar!")
