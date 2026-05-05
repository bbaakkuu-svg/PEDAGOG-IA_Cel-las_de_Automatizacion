# 📄 Plan de Extracción de Texto: Auditor de Rúbricas

## 🎯 Objetivo
Dotar a la célula "Auditor de Rúbricas" de la capacidad de "leer" entregas de alumnos en formato PDF, transformándolas en texto plano estructurado para su posterior análisis por la IA.

## 🛠️ Herramientas y Librerías
*   **PyMuPDF (fitz)**: Elegida por su alta velocidad y capacidad para manejar layouts complejos, tablas y metadatos.
*   **Re (Regex)**: Para la limpieza de ruido (encabezados, números de página, caracteres especiales).

## 🏗️ Implementación del Adaptador

Crearemos un `PDFAdapter` siguiendo el patrón de diseño **Adapter** para desacoplar la lógica de extracción de la lógica de auditoría.

### Funcionalidades Clave:
1.  **Extracción por Bloques**: Mantener el orden lógico de lectura.
2.  **Limpieza Inteligente**: Eliminar saltos de línea innecesarios que rompen la semántica del texto.
3.  **Metadatos**: Extraer autor y fecha de creación si están disponibles para validación de autoría.

## 📐 Mejoras a la Instrucción (Self-Correction)
*   **OCR Fallback**: Si el PDF es una imagen (escaneo), el sistema debe detectar que no hay texto y sugerir el uso de un módulo de OCR (como Tesseract).
*   **Chunking Estratégico**: No enviar el PDF completo al LLM de una vez si es muy largo; implementar una estrategia de "Ventana Deslizante" o "Resumen por Secciones" para no exceder los límites de tokens.
*   **Validación de Formato**: Comprobar que el archivo existe y es un PDF válido antes de intentar la apertura.

## 🚀 Hoja de Ruta
1.  **Instalación**: `pip install pymupdf`.
2.  **Desarrollo**: Crear `celula-auditor-rubricas/adapters/pdf_adapter.py`.
3.  **Integración**: Actualizar `main.py` para aceptar rutas de archivos PDF.

---
*Generado por Antigravity AI Engine | Procesamiento Documental 2026*
