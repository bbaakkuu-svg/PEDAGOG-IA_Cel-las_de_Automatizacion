# 📊 Blueprint: Dashboard Analítico SEA v4.0

## 🎯 Visión Sistémica
El Dashboard Analítico no es solo un visualizador, es el **Nervio Central** del ecosistema PEDAGOG-IA. Su propósito es convertir datos crudos de múltiples fuentes en decisiones pedagógicas accionables.

## 🏗️ Arquitectura de Datos (Data Harmonization)
El Dashboard consume un Pipeline híbrido:
1.  **Auditor de Rúbricas**: Provee métricas de desempeño académico y desglose por competencias vía Excel (`.xlsx`).
2.  **Monitor de Riesgo**: Provee alertas tempranas basadas en patrones de actividad y sentimiento vía JSON (`.json`).
3.  **DataEngine (Python)**: Actúa como el orquestador que unifica estos formatos en un solo contrato de datos para el Frontend.

## 🎨 Principios de Diseño (Premium UX)
-   **Dark First**: Interfaz optimizada para reducir la fatiga visual del docente.
-   **Glassmorphism**: Uso de transparencias y desenfoque para una estética moderna y profesional.
-   **Interactividad Proactiva**: Gráficos de radar dinámicos que permiten comparar el progreso individual vs. grupal.

## 🤖 Capa de IA Insights
El sistema no solo muestra números, aplica una lógica de inferencia para generar:
-   **Alertas de Intervención**: Identifica qué alumnos están en el "Valle del Abandono".
-   **Recomendaciones de Material**: Sugiere al docente reforzar ciertos temas en el `Generador de Material` basándose en las competencias más débiles de la cohorte.

## 🛠️ Roadmap de Mejora (Industrialización)
1.  **[PROX] Exportación Multi-formato**: Generación de reportes PDF para juntas de evaluación.
2.  **[PROX] Heatmaps de Actividad**: Visualización temporal de cuándo los alumnos interactúan más con el contenido.
3.  **[PROX] Real-time Sync**: Uso de WebSockets para actualizaciones sin recargar la página.

---
*Diseñado por Antigravity | Ingeniería de Pedagogía Aumentada 2026*
