# 🚀 Proyecto Piloto: Auditor de Rúbricas (MVP Industrial)

## 🎯 Visión del Piloto
El "Auditor de Rúbricas" ha sido seleccionado como el MVP para demostrar la potencia de la automatización pedagógica. Su propósito no es solo calificar, sino **humanizar el feedback** mediante la transparencia algorítmica.

## 🏗️ Alcance del MVP (V1.0-Release)
1.  **Motor de Ingesta**: Soporte completo para PDFs (vía `PyMuPDF`).
2.  **Lógica CoT (Chain of Thought)**: Implementación de un flujo de razonamiento donde la IA "explica" cada punto asignado.
3.  **UI Industrial**: Interfaz de terminal enriquecida con `rich` que muestra barras de progreso y tablas de resultados estilizadas.
4.  **Ejecutable Portable**: Generación de un `.exe` autocontenido para que cualquier profesor pueda usarlo sin instalar Python.

## 📐 Mejoras a la Instrucción (Self-Correction)
*   **Modo Demo Integrado**: Si el usuario no proporciona un PDF, el MVP debe ejecutar un análisis de una "Entrega de Ejemplo" interna para demostrar su valor instantáneamente.
*   **Gestión de Errores Robusta**: Capturar excepciones de archivos corruptos o falta de conexión a la API (usando mocks si es necesario para el ejecutable).
*   **Release Automatizada**: El proceso de empaquetado debe incluir los templates de prompts como recursos incrustados en el ejecutable.

## 🛠️ Proceso de Release (WorkFlow)
1.  **Validación**: Test de integración de los 4 módulos core.
2.  **Compilación**: Uso de `PyInstaller` con el flag `--onefile`.
3.  **Distribución**: Colocación del binario en la carpeta `/Release` del repositorio.

---
*Generado por Antigravity AI Engine | Proyecto Piloto Pedagog-IA 2026*
