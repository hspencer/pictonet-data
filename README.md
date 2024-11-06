# PictoNet Data

Sistema de gestión y procesamiento de datos para PictoNet. Maneja la recolección, limpieza y preparación de datasets para el entrenamiento.

## Componentes Principales

### 📁 collectors/
- `quickdraw.py`: Integración con Google Quick Draw Dataset
- `arasaac.py`: Colector de pictogramas ARASAAC
- `openmoji.py`: Procesamiento de OpenMoji

### 📁 processors/
- `svg_cleaner.py`: Limpieza y normalización de SVGs
- `normalizer.py`: Estandarización de formatos

### 📁 datasets/
- `generator.py`: Generación de datasets de entrenamiento
- `validator.py`: Validación de calidad de datos

### 📁 metadata/
- `labels.json`: Etiquetas y categorías
- `mappings.json`: Mapeos entre conceptos y pictogramas

## Fuentes de Datos Soportadas

- Google Quick Draw Dataset
- ARASAAC
- OpenMoji
- Material Design Icons

## Instalación

```bash
poetry install
```

## Uso

```python
from pictonet_data.collectors import QuickDrawCollector
from pictonet_data.processors import SVGCleaner

# Recolectar datos
collector = QuickDrawCollector()
raw_data = collector.collect("chair")

# Procesar SVGs
cleaner = SVGCleaner()
processed_data = cleaner.clean(raw_data)
```

## Pipeline de Datos

1. Recolección de fuentes múltiples
2. Limpieza y normalización
3. Validación de calidad
4. Generación de dataset final