# 🧠 api_intelligence_wrapper v0.1.0

## 🌟 ¿Qué es?
Es la capa de inteligencia del ecosistema. Actúa como un **Facade Pattern** que simplifica y estandariza la comunicación con modelos de lenguaje (LLMs) y APIs de inteligencia externa, ocultando la complejidad técnica bajo una interfaz limpia.

## 🚀 Inicio Rápido
### Requisitos
- Python >= 3.9
- `pydantic`, `requests`

### Instalación
```bash
pip install -e .
```

### Uso Básico
```python
from api_intelligence_wrapper.facade import DocensasIntelligenceFacade
ai = DocensasIntelligenceFacade(api_token="TU_TOKEN")
assets = ai.fetch_active_assets()
```

## 📊 Funcionalidades Clave
*   **Normalización de Datos**: Transforma respuestas crudas de APIs en objetos Pydantic validados.
*   **Gestión de Tokens**: Manejo centralizado de autenticación.
*   **Abstracción de IA**: Preparado para integrar Gemini, OpenAI o modelos locales sin cambiar el código cliente.

## 🧠 Filosofía: Inteligencia Transparente
Creemos que la IA debe ser una herramienta predecible. Este wrapper garantiza que los datos que entran y salen del sistema sigan esquemas estrictos, evitando errores en tiempo de ejecución.

## 🛠️ Soporte
Reportar issues en el repositorio central de PEDAGOG-IA.
