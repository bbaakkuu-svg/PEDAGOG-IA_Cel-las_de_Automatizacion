# ☁️ Especificación Técnica: Cloud-Native Task Scheduler

## 🎯 Objetivo de Autoridad
Demostrar el poder del **Desacoplamiento Total**. Este activo debe probar que la lógica de "cuándo" se ejecuta una tarea es independiente de la tecnología de "dónde" se ejecuta. 

## 🛠️ Requisitos de Arquitectura (Dependency Injection Edition)
1.  **Inversion of Control (IoC)**: El Scheduler no debe instanciar sus propios ejecutores; estos deben ser inyectados en el constructor.
2.  **Abstracción de Interfaz**: Definir una clase base abstracta (`TaskExecutor`) que garantice que cualquier nuevo motor de ejecución sea compatible.
3.  **Configuración Dinámica**: Uso de variables de entorno para decidir qué ejecutor inyectar en tiempo de ejecución.
4.  **Logging Pedagógico**: Cada ejecución debe dejar una traza clara de qué "Estrategia de Ejecución" se está utilizando.

## 🚀 Instrucción Mejorada para el Agente
"Diseña un sistema que sea **Agnóstico a la Infraestructura**. El Scheduler debe tratar a la nube y al entorno local como simples 'detalles de implementación'. Prioriza el uso de `abc` (Abstract Base Classes) para definir el contrato de ejecución."
