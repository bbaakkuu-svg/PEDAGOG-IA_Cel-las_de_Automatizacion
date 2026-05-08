# ☁️ cloud_native_task_scheduler v0.1.0

## 🌟 ¿Qué es?
Es el motor de ejecución temporal. Permite programar y orquestar tareas automáticas (como el escaneo semanal de alumnos en riesgo o la generación nocturna de materiales) de forma resiliente y nativa.

## 🚀 Inicio Rápido
### Instalación
```bash
pip install -e .
```

### Uso
```python
from cloud_native_task_scheduler.core.scheduler import TaskScheduler
scheduler = TaskScheduler()
scheduler.add_task("analisis_riesgo", frequency="daily")
```

## 📊 Funcionalidades Clave
*   **Gestión de Estados**: Seguimiento de tareas pendientes, en curso y fallidas.
*   **Reintentos Automáticos**: Lógica de "backoff" para manejar fallos temporales en APIs.
*   **Logging Industrial**: Registro detallado de cada ejecución para auditoría técnica.

## 🧠 Filosofía: Fiabilidad Operativa
Un sistema de automatización solo es útil si es confiable. El scheduler garantiza que nada se quede sin ejecutar, actuando como el metrónomo del ecosistema.

## 🛠️ Soporte
Revisar los logs en la carpeta `/logs` para diagnóstico de errores.
