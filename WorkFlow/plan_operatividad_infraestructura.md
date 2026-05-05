# 🛠️ Plan de Operatividad: Infraestructura PEDAGOG-IA

## 🎯 Objetivo
Activar el núcleo de automatización (4 infra-células) y dar comienzo al desarrollo técnico de la célula "Auditor de Rúbricas" utilizando los estándares industriales establecidos.

## ⚙️ Orquestación de Infraestructura (Bootstrapping)

Para poner en funcionamiento el sistema, realizaremos una instalación en modo **Editable (-e)** de los 4 componentes core. Esto permite que los cambios en el código se reflejen instantáneamente en el entorno de ejecución.

| Módulo | Función Crítica en la Fase 2 |
| :--- | :--- |
| `api_intelligence_wrapper` | Interfaz de comunicación con Gemini para el análisis de rúbricas. |
| `auto_repo_scaffolder` | Generación de la estructura Kenneth Reitz para cada nueva célula pedagógica. |
| `cloud_native_task_scheduler` | Programación de escaneos masivos de entregas de alumnos. |
| `ecosystem_sync_orchestrator`| Garantía de que todas las células operan con la última versión del core. |

## 📐 Mejoras a la Instrucción (Self-Correction)
*   **Virtual Environment Isolation**: Antes de instalar, recomendaremos el uso de un entorno virtual para evitar conflictos de dependencias.
*   **Unified CLI**: Desarrollar un pequeño "launcher" en la raíz que use el orquestador para verificar que los 4 módulos están operativos.
*   **Prompt Engineering Standard**: Para el "Auditor de Rúbricas", no solo usaremos prompts simples, sino una técnica de **Chain of Thought (CoT)** para que la IA "razone" el cumplimiento de cada ítem de la rúbrica antes de dar una nota.

## 🚀 Hoja de Ruta Inmediata
1.  **Activación Core**: Ejecución de `pip install -e .` en las 4 carpetas indicadas.
2.  **Validación**: Prueba de importación de los módulos desde un script de testeo.
3.  **Desarrollo Auditor**: 
    - Inicialización de rama `feature/auditor-rubricas-core`.
    - Implementación del `RubricAnalyzer` usando el wrapper de inteligencia.

---
*Generado por Antigravity AI Engine | Operatividad de Sistemas 2026*
