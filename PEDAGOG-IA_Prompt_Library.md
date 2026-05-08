# 🧠 PEDAGOG-IA: Prompt Library & Guía de Operaciones de IA

Este documento consolida todos los "Master Prompts" desarrollados durante la creación e industrialización del ecosistema PEDAGOG-IA. Actúa como el **Manual de Operaciones** para mantener, escalar y auditar el código utilizando inteligencia artificial.

## 📑 Tabla de Contenidos

1. [Fase 1: Arquitectura y Diseño de Software](#fase-1-arquitectura-y-diseño-de-software)
   - 1.1. [Diseño de Células de Automatización (Industrialización)](#11-diseño-de-células-de-automatización-industrialización)
   - 1.2. [Interoperabilidad y Pipeline de Datos](#12-interoperabilidad-y-pipeline-de-datos)
   - 1.3. [Refactorización Arquitectural Orientada a Dominios](#13-refactorización-arquitectural-orientada-a-dominios)
2. [Fase 2: Desarrollo y Refactorización](#fase-2-desarrollo-y-refactorización)
   - 2.1. [Rebranding y Sustitución Semántica](#21-rebranding-y-sustitución-semántica)
   - 2.2. [Ingeniería de Prompts para Evaluadores IA (Pedagogía)](#22-ingeniería-de-prompts-para-evaluadores-ia-pedagogía)
3. [Fase 3: QA, Pruebas y Auditoría](#fase-3-qa-pruebas-y-auditoría)
   - 3.1. [Auditoría Profunda de Código (Por Módulo)](#31-auditoría-profunda-de-código-por-módulo)
   - 3.2. [Auditoría Integral del Ecosistema y Binarios](#32-auditoría-integral-del-ecosistema-y-binarios)
4. [Fase 4: DevOps, Build y Despliegue](#fase-4-devops-build-y-despliegue)
   - 4.1. [Sincronización y Workflow de GitHub](#41-sincronización-y-workflow-de-github)
   - 4.2. [Estrategia "Slim Build" (Optimización de Tamaño)](#42-estrategia-slim-build-optimización-de-tamaño)
   - 4.3. [Empaquetado de Células Híbridas (Web/Backend)](#43-empaquetado-de-células-híbridas-webbackend)
   - 4.4. [Optimización de Gestión de Ciclo de Vida (SDLC)](#44-optimización-de-gestión-de-ciclo-de-vida-sdlc)
5. [Fase 5: Gestión de Conocimiento y Gobernanza](#fase-5-gestión-de-conocimiento-y-gobernanza)
   - 5.1. [Actualización Continua de la Librería (Auto-updater)](#51-actualización-continua-de-la-librería-auto-updater)

---

## Fase 1: Arquitectura y Diseño de Software

### 1.1. Diseño de Células de Automatización (Industrialización)
**Objetivo:** Crear una arquitectura robusta (Clean Architecture) para herramientas en Python.
**Casos de Uso:** Iniciar un nuevo proyecto desde cero o estandarizar un script suelto.

> **Instrucción Core:**
> "Contexto: Estamos migrando scripts educativos a un estándar industrial. La meta es crear 'Células de Automatización' modulares.
> Tarea: Define la arquitectura de software (Clean Architecture / MVC) para este módulo.
> 1. Crea la estructura de directorios (`core/`, `adapters/`, `main.py`).
> 2. Usa `Pydantic` para validación de datos en las interfaces de entrada/salida.
> 3. Separa estrictamente la Lógica de Negocio de las integraciones externas.
> 4. Establece un punto de entrada (`main.py`) que sirva de orquestador limpio.
> Output: Un esquema de árbol de archivos y el código base inicial comentado."

### 1.2. Interoperabilidad y Pipeline de Datos
**Objetivo:** Estandarizar el flujo de datos entre múltiples herramientas para que trabajen en cadena.
**Casos de Uso:** Cuando la salida (Ej. un Excel) de un programa es rechazada por el programa siguiente.

> **Instrucción Core:**
> "Contexto: Nuestras células operan en silos de datos. Necesito construir un Pipeline ininterrumpido.
> Tarea:
> 1. Definición de Esquema Común (Data Contract): Crea un estándar de nombres (ej: `student_id`, `nota_media`).
> 2. Refactorización del Emisor: Actualiza la exportación para que cumpla el contrato.
> 3. Refactorización del Receptor: Aplica 'Graceful Degradation' (tolerancia a fallos); si faltan columnas adicionales, que asigne pesos dinámicos y no rompa la ejecución.
> Output: Scripts emisores y receptores actualizados y diagrama de flujo de datos."

### 1.3. Refactorización Arquitectural Orientada a Dominios
**Objetivo:** Evolucionar un ecosistema disperso hacia una estructura modular industrial.
**Casos de Uso:** Reestructuración profunda de repositorios para mejorar la mantenibilidad.

> **Instrucción Core:**
> "Contexto: Estamos ejecutando una refactorización integral hacia una Arquitectura Modular de Grado Industrial.
> Tarea: Reubica y unifica los componentes del sistema siguiendo estos dominios:
> 1.  **Núcleo Unificado (`/core`)**: Fusiona toda la lógica compartida (adapters, IA, config, logger, cache) en un solo paquete central.
> 2.  **Agrupación de Células (`/cells`)**: Migra las aplicaciones funcionales a directorios de dominio específicos (ej: `cells/auditor`).
> 3.  **Segregación de Infraestructura (`/infra`)**: Aísla herramientas de soporte, orquestación y scripts de DevOps.
> 4.  **Normalización de Rutas**: Implementa resolución de rutas dinámica (basada en `pathlib`) para asegurar la portabilidad post-migración.
> Output: Estructura de archivos reubicada y puntos de entrada (`main.py`) con importaciones actualizadas."

---

## Fase 2: Desarrollo y Refactorización

### 2.1. Rebranding y Sustitución Semántica
**Objetivo:** Cambiar nombres, marcas o términos clave a través de todo el código de forma segura.
**Casos de Uso:** Cambios de marca comercial, migración de terminología (Ej. de 'Alumno' a 'Usuario').

> **Instrucción Core:**
> "Contexto: Estamos realizando un Rebranding. Necesitamos cambiar el término '[TERMINO_VIEJO]' por '[TERMINO_NUEVO]' en toda la aplicación.
> Tarea: Ejecuta una Búsqueda y Reemplazo Inteligente Sensible al Contexto.
> 1. Reemplaza variables, funciones, nombres de clases y comentarios.
> 2. Respeta el formato original de capitalización (camelCase, snake_case, PascalCase).
> 3. No modifiques librerías externas o dependencias críticas del sistema.
> Output: Archivos clave refactorizados manteniendo la consistencia de ejecución."

### 2.2. Ingeniería de Prompts para Evaluadores IA (Pedagogía)
**Objetivo:** Crear instrucciones sistémicas para LLMs enfocados en evaluación educativa.
**Casos de Uso:** Programar el "cerebro" de un auditor o generador de material de IA.

> **Instrucción Core:**
> "Contexto: Eres el Arquitecto de IA de una herramienta educativa.
> Tarea: Diseña el 'System Prompt' central para el motor de Inteligencia Artificial de esta célula.
> 1. Rol: Define el comportamiento exacto (Ej: 'Eres un Evaluador Implacable pero Constructivo').
> 2. Input/Output: Define qué información recibe la IA (texto, JSON) y qué formato exacto debe devolver.
> 3. Restricciones (Guardrails): Establece reglas duras (Ej: 'No alucinar notas', 'Basarse solo en la rúbrica').
> Output: El código Python del Wrapper del LLM inyectando este System Prompt."

---

## Fase 3: QA, Pruebas y Auditoría

### 3.1. Auditoría Profunda de Código (Por Módulo)
**Objetivo:** Evaluar la calidad técnica de una herramienta en solitario.
**Casos de Uso:** Antes de la primera compilación a producción.

> **Instrucción Core:**
> "Tarea: Realiza una auditoría técnica profunda y un plan de pruebas sobre la célula actual.
> 1. Análisis de Robustez: Revisa cumplimiento de Clean Architecture y aislamiento de dependencias.
> 2. Stress-Test: Simula Caso Feliz, Caso Límite (archivos vacíos) y Caso Error (corrupción).
> 3. Identificación de Fugas: Busca memory leaks o archivos no cerrados (`with open`).
> Output: Un reporte con Puntuación de Estabilidad (1-10), Tabla de Bugs (con severidad) y Mejoras 'Low-Hanging Fruit'."

### 3.2. Auditoría Integral del Ecosistema y Binarios
**Objetivo:** Probar cómo interactúan las herramientas compiladas entre sí.
**Casos de Uso:** Control de calidad general del producto final (.exe) y la interoperabilidad.

> **Instrucción Core:**
> "Tarea: Realiza una Auditoría Técnica Profunda y Pruebas Cruzadas sobre todo el repositorio.
> 1. Código: Busca vulnerabilidades compartidas (hardcoding, manejo de excepciones).
> 2. Stress-Test de Ejecutables: Analiza tiempos de arranque de los '.exe', peso real y fallos sin internet.
> 3. Pruebas de Interoperabilidad: ¿Qué pasa si alimento al Monitor con el output del Auditor?
> Output: Matriz de Calidad del ecosistema, Tabla de Bugs Inter-célula y Plan de Acción a nivel de infraestructura global."

### 3.3. Depuración de Crash Silencioso en Ejecutables (PyInstaller)
**Objetivo:** Diagnosticar por qué un `.exe` se cierra inmediatamente sin mostrar errores.
**Casos de Uso:** Tras aplicar estrategias agresivas de reducción de tamaño ("Slim Build") o cambiar de entorno.

> **Instrucción Core:**
> "Contexto: Al hacer doble clic sobre el `.exe` recién compilado, la ventana se cierra de golpe.
> Tarea:
> 1. Ejecución Diagnóstica: Ejecuta el binario desde una terminal (PowerShell/cmd) para capturar el Traceback.
> 2. Identificación de Dependencias Ocultas: Busca `ModuleNotFoundError`. Si falta una librería base (ej: `email`, `html`), es porque una dependencia visual (`rich`) la necesita internamente.
> 3. Identificación de Rutas (Paths): Si el error indica que no encuentra un módulo propio (ej: `api_intelligence_wrapper`), significa que PyInstaller no reconoce la ruta raíz del paquete.
> 4. Corrección: Modifica el archivo `.spec`. Retira el módulo faltante de `excluded_modules` o añade la ruta correcta a `pathex=[project_root, os.path.join(project_root, 'mi_paquete')]`.
> 5. Recompilación: Vuelve a ejecutar PyInstaller limpiando la caché (`--clean`).
> Output: El log de error descubierto, el `.spec` corregido y el binario funcional."

---

## Fase 4: DevOps, Build y Despliegue

### 4.1. Sincronización y Workflow de GitHub
**Objetivo:** Mantener el repositorio remoto perfectamente alineado con los cambios locales.
**Casos de Uso:** Después de cualquier hito de desarrollo importante.

> **Instrucción Core:**
> "Contexto: He realizado cambios locales significativos que necesitan respaldarse y compartirse.
> Tarea: Utiliza los scripts de automatización de Git del proyecto.
> 1. Ejecuta el script de sincronización/pull.
> 2. Ejecuta el script de Commit y Push.
> 3. Escribe un mensaje de commit usando el estándar Conventional Commits (feat, fix, refactor, build).
> Output: Confirmación visual del estado del repositorio remoto y local sincronizados."

### 4.2. Estrategia "Slim Build" (Optimización de Tamaño)
**Objetivo:** Reducir el tamaño de los archivos ejecutables (.exe) generados por PyInstaller.
**Casos de Uso:** Cuando el binario excede los 50MB por arrastrar librerías de data science.

> **Instrucción Core:**
> "Contexto: Los ejecutables actuales son demasiado pesados para su distribución.
> Tarea: Implementar un 'Slim Build' drástico.
> 1. Eliminación de Grasa: Refactoriza el código fuente para sustituir librerías pesadas (`pandas`, `numpy`) por nativas (`csv`, `openpyxl`).
> 2. Exclusiones en `.spec`: Crea un archivo `.spec` personalizado excluyendo masivamente módulos innecesarios (`tkinter`, `matplotlib`, `unittest`).
> 3. Compresión: Asegúrate de habilitar `strip=True` y la compresión `UPX` si está disponible.
> Output: Código refactorizado, nuevo archivo `.spec` y validación del tamaño final reducido."

### 4.3. Empaquetado de Células Híbridas (Web/Backend)
**Objetivo:** Compilar aplicaciones que usan un backend Python con frontend HTML/JS en un solo `.exe`.
**Casos de Uso:** Distribución de Dashboards o herramientas con interfaz en el navegador.

> **Instrucción Core:**
> "Contexto: Necesitamos convertir una aplicación web/backend en un archivo ejecutable portátil.
> Tarea: 
> 1. Configurar el archivo `.spec` para usar la sintaxis `datas=[]` y empaquetar las carpetas `web/` y `data/` explícitamente.
> 2. Refactorizar el código de Python (`main.py`) para que resuelva las rutas usando `sys._MEIPASS` (para evitar el Error 404 al correr como binario).
> 3. Compilar manteniendo el modo consola activo para ver los logs del servidor.
> Output: Archivo `.spec` ajustado, `main.py` con resolución dinámica de paths y el ejecutable funcional."

### 4.4. Optimización de Gestión de Ciclo de Vida (SDLC)
**Objetivo:** Automatizar el flujo de desarrollo desde la creación de la tarea hasta el despliegue.
**Casos de Uso:** Gestión profesional de hitos de desarrollo utilizando el framework WorkFlow.

> **Instrucción Core:**
> "Contexto: Eres un DevOps Engineer Senior. Utiliza el framework `/infra/WorkFlow` para gestionar el ciclo de vida del software (SDLC).
> Tarea: Para cada nuevo requerimiento técnico:
> 1.  **Analiza** el impacto arquitectural en los dominios `/core` y `/cells`.
> 2.  **Formaliza** la tarea mediante la creación de GitHub Issues con etiquetas de prioridad.
> 3.  **Aísla** el desarrollo creando ramas de trabajo (`feature/`, `bugfix/`) vinculadas al ID del issue.
> 4.  **Sincroniza** proactivamente el estado del repositorio local con el Tablero Maestro del Proyecto.
> Output: Confirmación de Issues creados, ramas activadas y tablero sincronizado."

---

## Fase 5: Gestión de Conocimiento y Gobernanza

### 5.1. Actualización Continua de la Librería (Auto-updater)
**Objetivo:** Mantener la librería de Prompts viva y actualizada de forma autónoma.
**Casos de Uso:** Directiva de sistema o tarea final de cierre en cualquier sesión de IA.

> **Instrucción Core:**
> "Contexto: Tenemos una Librería de Prompts en `PEDAGOG-IA_Prompt_Library.md`. No debe quedar obsoleta.
> Tarea:
> 1. Auto-Detección: Identifica si la estrategia que acabas de usar califica como un nuevo Master Prompt.
> 2. Inserción Continua: Añádelo al archivo Markdown bajo la fase correcta (o crea una nueva).
> 3. Commit Inmediato: Usa las herramientas de git para guardar los cambios en el repositorio.
> Output: Un documento siempre actualizado sin que el usuario deba pedirlo explícitamente."

## Fase 6: Estabilización Avanzada y Ops

### 6.1. Implementación de Logging Industrial
**Objetivo:** Establecer una trazabilidad completa de errores y eventos.

> **Instrucción Core:**
> "Contexto: Necesitamos añadir trazabilidad a la célula [NOMBRE_CELULA].
> Tarea: Implementa un sistema de logging persistente.
> 1. Usa `shared_core.logger` para instanciar un logger con rotación de archivos.
> 2. Asegura que los errores críticos se capturen con el StackTrace completo.
> 3. Los logs deben guardarse en la carpeta `/logs` de la raíz del proyecto.
> Output: Código actualizado con decoradores de logging o llamadas explícitas en puntos críticos."

### 6.2. Configuración de CI/CD para Binarios
**Objetivo:** Automatizar la creación de entregables (.exe) en cada hito.

> **Instrucción Core:**
> "Contexto: Queremos automatizar el despliegue del ecosistema.
> Tarea: Crea un archivo de workflow de GitHub Actions (`.github/workflows/build_releases.yml`).
> 1. Define disparadores para 'Tags' (ej: v*).
> 2. Configura un runner de Windows.
> 3. Instala dependencias y ejecuta PyInstaller.
> 4. Usa la acción `softprops/action-gh-release` para subir los binarios generados.
> Output: El archivo YAML del workflow listo para commit."

### 6.3. Capa de Caching Pedagógica (Performance Optimization)
**Objetivo:** Evitar el re-procesamiento costoso de archivos o llamadas a IA idénticas.

> **Instrucción Core:**
> "Contexto: Las células están consumiendo demasiados recursos al re-evaluar los mismos datos.
> Tarea: Implementa una capa de persistencia temporal (caché).
> 1. Usa `shared_core.cache` para almacenar resultados basados en el hash del input.
> 2. Define un TTL (Time-To-Live) para que los datos no queden obsoletos.
> 3. Integra la lógica de 'Bypass' en la función de análisis principal: si el hash existe, devuelve el valor cacheado; si no, procesa y guarda.
> Output: Módulo de caché y refactorización del motor de análisis."

---
*Mantenido por Antigravity | Ecosistema PEDAGOG-IA 2026*
