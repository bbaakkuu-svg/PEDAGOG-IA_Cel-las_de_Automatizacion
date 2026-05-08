# 📚 Plan: Generador Dinámico de Material (IA)

## 🎯 Objetivo
Crear una factoría de contenido educativo capaz de transformar temarios densos, transcripciones de clases o documentación técnica en recursos de aprendizaje listos para el consumo (Resúmenes, Cuestionarios y Estructuras de Presentación).

## 🧩 Componentes del Generador
La célula operará mediante un motor de transformación multi-salida:
1.  **Summarizer (Resumidor)**: Generación de "Key Takeaways" y resúmenes ejecutivos.
2.  **Quiz Master**: Creación de preguntas de opción múltiple (Multiple Choice) con retroalimentación inmediata.
3.  **Slide Architect**: Estructuración de diapositivas (Título, Bullet Points, Sugerencia de Imagen) exportable a formatos como Markdown o PPTX.

## 🏗️ Arquitectura de la Célula
*   `TransformEngine`: Núcleo que utiliza la infraestructura de `api_intelligence_wrapper` para procesar el contenido.
*   `TemplateSystem`: Uso de Jinja2 (vía `auto_repo_scaffolder`) para formatear las salidas.
*   `ResourceExporter`: Adaptadores para exportar a PDF, Markdown y (futuro) PPTX.

## 📐 Mejoras a la Instrucción (Self-Correction)
*   **Taxonomía de Bloom**: Clasificar las preguntas del cuestionario según niveles cognitivos (Recordar, Comprender, Aplicar).
*   **Adaptación de Estilo**: Permitir configurar el "Tono" del material (Académico, Divulgativo, Gamificado).
*   **Consistencia Visual**: Generar sugerencias de "Prompts de Imagen" para que el profesor pueda usarlos en herramientas de generación de imágenes (DALL-E/Midjourney) para ilustrar el material.

## 🚀 Hoja de Ruta Inmediata
1.  **Sincronización Core**: Ejecución del orquestador para validar dependencias.
2.  **Scaffolding**: Crear `/celula-generador-material/templates` y `/celula-generador-material/output`.
3.  **Implementación**: Desarrollar el `ContentEngine` base que genere un Cuestionario JSON a partir de un texto.

---
*Generado por Antigravity AI Engine | Generación de Activos 2026*
