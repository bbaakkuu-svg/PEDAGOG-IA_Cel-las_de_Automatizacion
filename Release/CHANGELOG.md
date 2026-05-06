# 📝 Changelog: Auditor de Rúbricas MVP

## [1.0.0] - 2026-05-05

### ✨ Características
- **Motor de Ingesta**: Soporte inicial para extracción de texto en archivos PDF.
- **Lógica de Auditoría**: Implementación de flujo de razonamiento Chain of Thought (CoT).
- **Interfaz Visual**: Reportes enriquecidos en consola con tablas y colores (Rich UI).
- **Modo Offline/Demo**: Capacidad de ejecución sin parámetros para demostraciones rápidas.

### 🛠️ Infraestructura Core
- Integración con el ecosistema **PEDAGOG-IA** (api_intelligence, scaffolding).
- Empaquetado binario autocontenido mediante PyInstaller.

### 🐛 Correcciones
- Solucionado el error crítico `UnicodeEncodeError` en consolas Windows (UTF-8 Enforcing).
- Implementada pausa de seguridad (`input()`) para evitar el cierre instantáneo de la consola.
- Añadida robustez en la carga de módulos y manejo de excepciones en `main.py`.
- Sincronizada dependencia `pymupdf` en el manifiesto global.

---
*Célula de Automatización | v1.0-Release*
