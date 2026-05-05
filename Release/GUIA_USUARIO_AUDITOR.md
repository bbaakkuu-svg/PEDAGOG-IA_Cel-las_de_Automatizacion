# 🎓 Guía del Usuario: Auditor de Rúbricas MVP v1.0

¡Bienvenido a **PEDAGOG-IA**! Esta herramienta ha sido diseñada para asistir al profesorado en la tarea crítica de la evaluación, proporcionando un feedback formativo, objetivo y basado en evidencias.

## 🌟 ¿Qué es el Auditor de Rúbricas?
Es un asistente de inteligencia artificial que "lee" las entregas de los alumnos (PDF) y las contrasta con una rúbrica de evaluación. Su objetivo no es sustituir al profesor, sino proporcionarle un **borrador de evaluación** altamente detallado con justificaciones claras para cada puntuación.

## 🚀 Inicio Rápido (Quick Start)

### 1. Requisitos
No necesitas instalar Python ni ninguna librería. El archivo es un ejecutable autocontenido para Windows.

### 2. Ejecución
1.  Localiza el archivo `Auditor_Rubricas_MVP.exe` en la carpeta `/Release`.
2.  **Opción A (Modo Demo)**: Haz doble clic en el archivo. El sistema ejecutará un análisis de ejemplo para que veas el formato de salida.
3.  **Opción B (Análisis Real)**: Arrastra un archivo PDF sobre el ejecutable, o ejecútalo desde la terminal pasando la ruta del archivo:
    ```bash
    .\Auditor_Rubricas_MVP.exe "ruta\a\la\entrega_alumno.pdf"
    ```

## 📊 Entendiendo el Reporte
El Auditor genera una tabla con cuatro columnas clave:
*   **Criterio**: El aspecto de la rúbrica evaluado.
*   **Pts**: La puntuación asignada (basada en el cumplimiento detectado).
*   **Evidencia**: La cita textual o descripción de lo hallado en el trabajo del alumno.
*   **Acción de Mejora**: Una recomendación concreta para que el alumno evolucione su trabajo.

## 🧠 Filosofía Pedagógica: Chain of Thought (CoT)
A diferencia de otros sistemas de IA, este auditor utiliza **Razonamiento en Cadena**. Esto significa que antes de asignar una nota, la IA debe "pensar" y localizar evidencias. Si no hay evidencia clara, el sistema lo indicará, evitando alucinaciones y garantizando una evaluación justa.

## 🛠️ Soporte y Feedback
Este es un **Proyecto Piloto (MVP)**. Si encuentras algún error o tienes sugerencias de mejora, por favor contacta con la Célula de Automatización a través del repositorio de GitHub.

---
*Transformando la educación a través de la transparencia algorítmica.*
