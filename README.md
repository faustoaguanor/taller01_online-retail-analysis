# 📊 Online Retail Dataset Analysis - Complete Data Science Workflow

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-green?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.4+-orange?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-lightblue?style=for-the-badge&logo=sqlite)
![Universidad](https://img.shields.io/badge/University-Yachay%20Tech-blue?style=for-the-badge)

**Universidad Yachay Tech - Maestría en Ciencia de Datos**  
**Curso:** Fundamentos de Ciencia de Datos  
**Dataset:** [Online Retail (UCI ML Repository)](https://archive.ics.uci.edu/dataset/352/online+retail)  
**Período del Dataset:** Diciembre 2010 - Diciembre 2011

---

## 🎯 Descripción del Proyecto

Este proyecto implementa un **taller de ciencia de datos** desde la adquisición hasta conclusiones accionables, utilizando el dataset Online Retail de UCI. El análisis revela patrones de comportamiento en e-commerce de regalos y decoración, identificando oportunidades estratégicas de crecimiento.

### 🔍 **Objetivos Principales:**
- **Adquisición y limpieza** de datos desde archivo Excel manual
- **Análisis exploratorio comprehensivo** (EDA) con metodología sistemática  
- **3 visualizaciones** generados desde lo datos
- **Generación de conclusiones** sobre el negocio

---

## 🗂️ Estructura del Proyecto

```
online_retail_analysis/
├── 📁 src/
│   ├── 🐍 adquisicion_datos.py      # Carga, limpieza y almacenamiento optimizado
│   ├── 📊 analisis_exploratorio.py  # EDA completo con metadata generada
│   ├── 📈 visualizacion.py          # 3 visualizaciones  
│   └── 🛠️ utils.py                  # Utilidades y generación de reportes
├── 📁 data/
│   └── 🗄️ online_retail.db         # Base SQLite con datos limpios (generada)
├── 📁 output/
│   ├── 🖼️ visualizacion_*.png      # Gráficos en alta resolución
│   ├── 📄 *.txt                    # Reportes detallados de análisis
│   └── 🔧 project_metadata.json    # Metadata programática
├── 🎯 main.py                      # Ejecutor principal del pipeline
├── 📋 README.md                    # Este archivo
├── 🚫 .gitignore                   # Configuración Git
└── 📊 Online Retail.xlsx           # Dataset original (descargar manualmente)
```

---

## 🚀 Instalación y Configuración

### 📋 Prerrequisitos

```bash
# Python 3.8 o superior
python --version

# Instalar dependencias
pip install pandas numpy matplotlib seaborn scipy
```

### 📥 Descargar Dataset

1. **Visitar:** [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)
2. **Descargar:** `Online Retail.xlsx` 
3. **Ubicar:** En el directorio raíz del proyecto
4. **Verificar:** El archivo debe llamarse exactamente `Online Retail.xlsx`

### ⚡ Ejecución Rápida

```bash
# Clonar el repositorio
git clone https://github.com/faustoaguanor/taller01_online-retail-analysis.git
cd taller01_online-retail-analysis

# Ejecutar análisis completo
python main.py
```

### 🔧 Ejecución Modular

```bash
# Solo adquisición y limpieza de datos
python src/data_acquisition.py

# Solo análisis exploratorio (EDA)
python src/exploratory_analysis.py

# Solo generación de visualizaciones
python src/visualizations.py
```

---

## 📊 Resultados y Outputs

### 🎨 **Visualizaciones Generadas**

#### 1️⃣ **Análisis Temporal Completo**
- Revenue mensual con tendencia estacional
- Patrones semanales de transacciones  
- Heatmap de intensidad horaria por día
- Top países por revenue total

#### 2️⃣ **Análisis de Productos y Clientes**
- Distribución de precios con análisis estadístico
- Top productos más vendidos por cantidad
- Análisis RFM (Recency, Frequency, Monetary)
- Segmentación por categorías de precio

#### 3️⃣ **Análisis Avanzado - Correlaciones y Pareto**
- Estacionalidad normalizada
- Comparativo Weekdays vs Weekend

### 📈 **Reportes Generados**

| Archivo | Descripción | Contenido |
|---------|-------------|-----------|
| `eda_report.txt` | Análisis exploratorio completo | Estadísticas, metadata, insights por campo |
| `interpretacion_visualizaciones.txt` | Explicación de los gráficos | 
| `reporte_final_online_retail.txt` | Resumen |
| `project_metadata.json` | Metadata | Métricas, configuración, información técnica |

---

## 🎯 Insights Principales Descubiertos

### 📅 **1. Estacionalidad Extrema**
- **60%+ del ingreso** concentrado en Nov-Dic
- **Riesgo de concentración temporal** identificado
- **Oportunidad:** Diversificación de productos anti-estacionales

### 🌍 **2. Concentración Geográfica**
- **Reino Unido:** 80%+ de transacciones
- **Mercados internacionales:** Subexplotados  
- **Oportunidad:** Expansión estratégica en Francia y Alemania

### 👥 **3. Segmentación Clara de Clientes**
- **Base diversa:** Oportunidades de personalización
- **Oportunidad:** Programa para retención de clientes top

### ⏰ **4. Patrones Operacionales B2B**
- **Horario comercial:** 9AM-5PM GMT concentra actividad
- **Días laborales:** 85%+ del ingreso semanal
- **Oportunidad:** Activación de mercado los fines de semana

---

## 🔄 Metodología y Proceso

### 📝 **Fase 1: Adquisición y Limpieza**
- **Carga manual** desde Excel (sin librerías externas)
- **Limpieza documentada** con lógica de negocio justificada
- **Validaciones robustas** post-limpieza
- **Almacenamiento optimizado** con chunks en SQLite

### 🔍 **Fase 2: Análisis Exploratorio**
- **Análisis sistemático** de cada variable
- **Metadata comprehensiva** generada automáticamente
- **Segmentación** de clientes implementada
- **Patrones temporales** identificados y cuantificados

### 📊 **Fase 3: Visualización e Insights**
- **3 visualizaciones** con explicaciones
- **Técnicas avanzadas:** Heatmaps, Pareto, correlaciones

---

 
### 📧 **Contacto**
- **Universidad:** Yachay Tech - Maestría en Ciencia de Datos
- **Curso:** Fundamentos de Ciencia de Datos
- **GitHub:** [@faustoaguanor](https://github.com/faustoaguanor)

---

## 📄 Licencia y Reconocimientos

### 📜 **Licencia**
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles.

### 🙏 **Reconocimientos**
- **UCI ML Repository** por el dataset Online Retail
- **Universidad Yachay Tech** por la formación académica
- **Comunidad Python** por las herramientas open-source utilizadas

---

## 📊 Estadísticas del Proyecto

![GitHub repo size](https://img.shields.io/github/repo-size/tu_usuario/taller01_online-retail-analysis)
![GitHub last commit](https://img.shields.io/github/last-commit/tu_usuario/taller01_online-retail-analysis)
![GitHub issues](https://img.shields.io/github/issues/tu_usuario/taller01_online-retail-analysis)
![GitHub stars](https://img.shields.io/github/stars/tu_usuario/taller01_online-retail-analysis)

---
