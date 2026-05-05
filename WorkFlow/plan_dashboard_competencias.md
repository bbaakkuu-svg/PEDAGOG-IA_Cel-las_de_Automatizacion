# 📊 Plan: Dashboard de Competencias (Visualizer)

## 🎯 Objetivo
Crear una interfaz visual de alta fidelidad que transforme datos fríos de calificaciones en un mapa estratégico de competencias, permitiendo a profesores y alumnos identificar fortalezas y áreas de mejora de un vistazo.

## 📈 Visualización Estratégica
La pieza central del dashboard será el **Radar Chart (Spider Chart)**, ideal para visualizar perfiles competenciales multidimensionales.
*   **Competencias Core**: Pensamiento Crítico, Resolución de Problemas, Trabajo en Equipo, Competencia Técnica, Comunicación.
*   **Comparativa**: Capacidad de superponer el perfil del alumno con la media del grupo o el objetivo del curso.

## 🏗️ Arquitectura de la Célula
*   `DataProcessor`: Script Python que lee JSON/CSV y normaliza los datos.
*   `WebDashboard`: Aplicación web estática (HTML5/Vanilla JS) ultra-moderna que consume los datos procesados.
*   **Tech Stack**: Plotly.js o Chart.js para los gráficos, CSS con estética "Glassmorphism" para la interfaz.

## 📐 Mejoras a la Instrucción (Self-Correction)
*   **Interactividad**: Los gráficos deben ser reactivos (hover effects) para mostrar el detalle de cada competencia.
*   **Exportación**: Opción de descargar el gráfico de radar como imagen (PNG) para incluir en reportes oficiales.
*   **Insights IA**: Integrar un pequeño cuadro de "Recomendación de la IA" que analice los puntos bajos del radar y sugiera material de la célula "Generador de Material".

## 🚀 Hoja de Ruta Inmediata
1.  **Scaffolding**: Crear `/celula-dashboard-competencias/web` y `/celula-dashboard-competencias/data`.
2.  **Dataset**: Crear `competencias_alumno.json`.
3.  **Frontend**: Desarrollar el Dashboard web siguiendo las directrices de diseño premium (WOW factor).

---
*Generado por Antigravity AI Engine | Visualización de Datos 2026*
