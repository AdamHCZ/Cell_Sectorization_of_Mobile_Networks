# 📡 Planificador de Red Móvil — 1G / 2G Calculator

Este proyecto es una **aplicación web interactiva** construida con [Flet](https://flet.dev) en Python.  
Permite a estudiantes, ingenieros e investigadores simular y visualizar la **planificación de redes celulares** para las tecnologías **1G** y **2G**.

La aplicación calcula parámetros clave como:

- 📍 Radio de cobertura  
- 🔄 Distancia de reutilización  
- 📐 Área del clúster  
- 📊 Relación de protección  
- 📶 Frecuencias por sector, celda y clúster  
- 📡 Canales disponibles (para 2G)  

También genera **tablas de asignación de frecuencias** de manera dinámica, basadas en el tamaño del clúster y el número de sectores.

---

## ✨ Características

- ✅ **Cambio entre 1G y 2G** mediante la barra de navegación superior  
- ✅ Validación de entradas con banners de error y asteriscos en campos requeridos  
- ✅ Botón de limpieza para reiniciar todas las entradas y resultados  
- ✅ Diseño responsivo (entradas/resultados a la izquierda, información técnica a la derecha)  
- ✅ Tablas de frecuencias dinámicas con desplazamiento horizontal  
- ✅ Barra lateral con resumen teórico de la tecnología seleccionada  
- ✅ Tema y colores consistentes inspirados en [calculator.net](https://www.calculator.net/area-calculator.html)  

---

## 🖼️ Captura de Pantalla

*(Agrega aquí una captura de tu aplicación en ejecución si es posible)*

---

## 🛠️ Tecnologías

- [Python 3.10+](https://www.python.org/)  
- [Flet](https://flet.dev) — framework frontend en Python  
- [FastAPI / asyncio (usado internamente por Flet)]  
- Módulos personalizados:
  - `pages/` — páginas de la interfaz (`radio_page.py`, `tech_info.py`)  
  - `components/` — componentes reutilizables (`controls.py`)  
  - `utils/` — constantes y datos auxiliares (`DATA.py`)  
  - `theme.py` — colores, espaciados y estilos de la UI  

---

## 📦 Requisitos

Instala las dependencias con `pip`:

```bash
pip install flet
