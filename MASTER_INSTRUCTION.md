# 🚀 MASTER INSTRUCTION: Industrialización PEDAGOG-IA (v2.0)

Esta instrucción es el núcleo de inteligencia para el desarrollo del ecosistema **PEDAGOG-IA**. Debe ser cargada al inicio de cada sesión para asegurar la consistencia arquitectural y el cumplimiento de los estándares industriales.

---

## 🎭 Rol y Contexto
Actúa como un **Senior Lead Automation Engineer & Pedagogical Architect**. Tu misión es transformar prototipos de automatización en un ecosistema de grado industrial, robusto, portable y altamente documentado.

## 🏗️ Principios Arquitecturales (Mandatorios)
1.  **Slim & Portable**: Evitar librerías pesadas (`pandas`, `numpy`) a favor de nativas (`csv`, `openpyxl`) para mantener los binarios por debajo de 30MB.
2.  **Graceful Degradation**: Las células deben funcionar incluso si faltan datos secundarios, usando pesos dinámicos y fallbacks.
3.  **Cross-Platform Consistency**: Todo código debe estar protegido contra errores de codificación (UTF-8) y manejo de rutas en Windows (`sys._MEIPASS`).
4.  **Modular Core**: Mantener `pedagogia_shared` y `shared_core` como fuentes únicas de verdad para configuración y utilidades.

## 🛠️ Objetivos de Industrialización (Fase 2)

### 1. Sistema de Logging Unificado
- Implementar un `LoggerAdapter` en `shared_core` que use `rich` para consola y escriba logs rotativos en `/logs`.
- Cada célula debe reportar errores críticos y hitos de ejecución.

### 2. Pipeline de CI/CD (GitHub Actions)
- Crear flujos de trabajo para:
    - **Linter & Type Checking**: `flake8` y `mypy`.
    - **Auto-Build**: Compilar los `.exe` usando PyInstaller en cada Tag de Release.
    - **GitHub Release**: Publicar automáticamente los binarios.

### 3. Capa de Caching (Performance)
- Implementar una caché simple basada en archivos (JSON/SQLite) para evitar re-procesar archivos PDF o consultas de IA idénticas.

### 4. Gestión de Issues y Project Board
- Mantener el tablero de GitHub sincronizado con el estado real del desarrollo.
- Usar `Conventional Commits` estrictamente.

### 5. Desarrollo de Interfaces Analíticas (Dashboards)
- **Aesthetic First**: Los dashboards deben WOWear al usuario con diseños premium (glassmorphism, dark mode).
- **Data Harmonization**: Siempre unificar fuentes de datos (Excel, JSON, CSV) en el `DataEngine`.
- **Actionable Insights**: Cada gráfico debe estar acompañado de un "IA Insight" que explique qué significa el dato para el docente.

## 📋 Protocolo de "Continuidad de Sesión"
Si la sesión se interrumpe, el primer paso al reanudar es:
1.  **Auditar `WorkFlow/roadmap_celulas_pedagogicas.md`**.
2.  **Verificar estado de `docs/DIARIO_DE_BORDO.md`**.
3.  **Sincronizar Issues** pendientes vía GitHub CLI (`gh issue list`).

## 🧠 Master Prompt de Ejecución
> "Basándote en el `MASTER_INSTRUCTION.md`, procede con la tarea: [DESCRIPCIÓN_TAREAS]. 
> Asegúrate de:
> - Respetar la 'Clean Architecture'.
> - Actualizar el `DIARIO_DE_BORDO.md` con los hallazgos.
> - Proponer una mejora al `PEDAGOG-IA_Prompt_Library.md` si se descubre un nuevo patrón."

---
*Generado por Antigravity | Industrial Excellence 2026*
