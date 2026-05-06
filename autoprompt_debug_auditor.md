# 🤖 Autoprompt: Depuración y Mejora del Auditor de Rúbricas MVP

## 📝 Diagnóstico Técnico
Tras analizar el fallo reportado en `Auditor_Rubricas_MVP.exe`, se identificaron dos problemas críticos:

1.  **UnicodeEncodeError (Crash en Windows):** La aplicación intentaba imprimir caracteres especiales (emojis como 🎓) en una consola de Windows configurada con `cp1252`. Esto causaba un cierre inmediato por excepción no controlada.
2.  **Cierre Instantáneo por Finalización:** Como aplicación de consola, si no se proporcionan argumentos (un PDF), la aplicación ejecuta una demo rápida y finaliza, cerrando la ventana antes de que el usuario pueda ver los resultados.
3.  **Dependencias Faltantes:** El paquete `pymupdf` (fitz) no estaba declarado en los `requirements.txt` del proyecto raíz, lo que podría causar fallos si el adaptador PDF es invocado.

## 🛠️ Acciones Realizadas
-   ✅ **Reconfiguración de E/S:** Se añadió lógica en `main.py` para forzar `utf-8` en `stdout` y `stderr` cuando se detecta Windows.
-   ✅ **Control de Flujo:** Se implementó un `input()` al final del bloque `if __name__ == "__main__":` para asegurar que la consola permanezca abierta hasta que el usuario decida cerrarla.
-   ✅ **Gestión de Errores Robusta:** Se envolvieron los bloques principales en `try-except` para capturar cualquier fallo de importación o ejecución y mostrarlo de forma elegante con `rich`.
-   ✅ **Sincronización de Dependencias:** Se actualizó `requirements.txt` con `pymupdf`.

## 🚀 Instrucción Mejorada (Prompt Engineering)
*Si necesitas volver a solicitar una tarea similar, utiliza este formato optimizado para obtener mejores resultados:*

> "Actúa como un Ingeniero de Automatización Senior. Tengo un problema con el ejecutable `Auditor_Rubricas_MVP.exe` en Windows. Se cierra inmediatamente al abrirlo. 
> 1. **Analiza el punto de entrada (`main.py`)** buscando errores de codificación (Unicode) y gestión de consola.
> 2. **Implementa un mecanismo de pausa** al finalizar la ejecución para que los resultados sean visibles.
> 3. **Asegura la compatibilidad con UTF-8** en entornos Windows legacy.
> 4. **Verifica las dependencias del adaptador PDF** (`fitz/pymupdf`) y asegúrate de que estén correctamente importadas o tengan un fallback seguro.
> 5. **Genera un reporte de cambios** en el `.md` de la release."

## 📦 Pasos para Re-empaquetar
Para generar el nuevo binario corregido, ejecuta desde la raíz:

```powershell
# Instalar dependencias necesarias
pip install -r requirements.txt
pip install pyinstaller

# Generar el ejecutable usando el archivo .spec existente
cd Release
pyinstaller --clean Auditor_Rubricas_MVP.spec
```

---
*Generado por Antigravity | Célula de Automatización PEDAGOG-IA*
