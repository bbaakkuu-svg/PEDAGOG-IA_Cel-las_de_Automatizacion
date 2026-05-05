# 🕵️ Plan: Monitor de Alumnos en Riesgo (EWS)

## 🎯 Objetivo
Desarrollar una célula de inteligencia analítica capaz de identificar patrones de desenganche o abandono (drop-out) en estudiantes mediante el procesamiento de logs de actividad y métricas de rendimiento.

## 📊 Modelado de Datos (Input)
Para que el monitor sea efectivo, procesaremos tres fuentes de datos principales:
1.  **Logs de Actividad (LMS)**: Frecuencia de acceso, tiempo en plataforma, clics en recursos.
2.  **Métricas de Entrega**: Retrasos en tareas, entregas vacías o con baja calificación recurrente.
3.  **Interacción Social**: Participación en foros y tono del lenguaje (opcional/Fase 3).

## 🧠 Lógica de Detección (Analítica)
Implementaremos un sistema de puntuación de riesgo (**Risk Score**) basado en:
*   **Umbral de Inactividad**: > 7 días sin login = Riesgo Alto.
*   **Tendencia de Calificaciones**: Pendiente negativa en las últimas 3 entregas.
*   **Ratio de Completitud**: < 50% de recursos obligatorios visualizados.

## 🏗️ Arquitectura de la Célula
*   `LogAdapter`: Lector de CSV/JSON provenientes de Moodle/Canvas.
*   `HeuristicEngine`: Aplicación de reglas de negocio para calcular el score.
*   `AlertDispatcher`: Generador de notificaciones (Slack, Email, o reporte JSON).

## 📐 Mejoras a la Instrucción (Self-Correction)
*   **Privacidad por Diseño (GDPR)**: Los logs deben ser anonimizados (Hashear IDs de alumnos) antes del análisis si se procesan en la nube.
*   **Falsos Positivos**: Implementar un sistema de "Contexto" (ej. periodos de vacaciones o exámenes) para evitar alertas erróneas por inactividad general.
*   **Intervención Sugerida**: La IA no solo detecta el riesgo, sino que genera un "Borrador de Mensaje de Apoyo" personalizado para que el tutor lo envíe.

## 🚀 Hoja de Ruta Inmediata
1.  **Scaffolding**: Crear `/celula-monitor-riesgo/core` y `/celula-monitor-riesgo/data`.
2.  **Dataset Sintético**: Generar un `logs_ejemplo.csv` para simular actividad.
3.  **Implementación**: Desarrollar el `RiskAnalyzer` base.

---
*Generado por Antigravity AI Engine | Analítica Predictiva 2026*
