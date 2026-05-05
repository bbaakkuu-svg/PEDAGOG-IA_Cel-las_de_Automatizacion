# 🔄 ecosystem_sync_orchestrator v0.1.0

## 🌟 ¿Qué es?
Es el guardián de la integridad. Se encarga de sincronizar y validar que todas las células del ecosistema estén operando con las versiones correctas y que las dependencias compartidas estén armonizadas.

## 🚀 Inicio Rápido
### Ejecución de Sincronización
```bash
python sync.py --all
```

## 📊 Funcionalidades Clave
*   **Gestión de Dependencias**: Verifica que los módulos core estén instalados en modo editable.
*   **Git-Sync**: Automatiza los pulls y actualizaciones de submódulos o carpetas vinculadas.
*   **Check de Salud**: Realiza un "ping" técnico a cada célula para confirmar su operatividad.

## 🧠 Filosofía: Sincronía Modular
En un sistema basado en células independientes, la desincronización es el mayor riesgo. El orquestador actúa como el tejido conectivo que mantiene el orden y la coherencia.

## 🛠️ Soporte
Usa `python sync.py --status` para ver el estado de salud de tu entorno local.
