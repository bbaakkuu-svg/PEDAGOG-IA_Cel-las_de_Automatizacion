# 📊 Análisis Sistémico: Diagramas Mermaid

Este documento visualiza la lógica y el flujo de datos del ecosistema PEDAGOG-IA antes de su implementación técnica.

## 🏗️ 1. Mapa de Orquestación del Ecosistema
Representa cómo las células de infraestructura soportan a las células pedagógicas.

```mermaid
graph TD
    subgraph "Infraestructura Core"
        A[Orquestador Sync] --> B[API Intel Wrapper]
        A --> C[Task Scheduler]
        A --> D[Repo Scaffolder]
    end

    subgraph "Células Pedagógicas"
        B --> E[Auditor de Rúbricas]
        B --> F[Generador de Material]
        C --> G[Monitor de Riesgo]
        D --> H[Dashboard Competencias]
    end

    style A fill:#6366f1,color:#fff
    style B fill:#818cf8,color:#fff
    style E fill:#f43f5e,color:#fff
```

## 📋 2. Flujo de Valor: Auditor de Rúbricas
Muestra el proceso de transformación de una entrega bruta en un activo pedagógico.

```mermaid
sequenceDiagram
    participant P as Profesor/Alumno
    participant A as PDF Adapter
    participant I as API Intel Wrapper
    participant M as LLM (Chain of Thought)
    
    P->>A: Carga entrega (PDF)
    A->>A: Limpieza de texto (Regex)
    A->>I: Texto plano normalizado
    I->>M: Prompt CoT + Rúbrica
    M-->>M: Razonamiento / Evidencia
    M->>I: Respuesta JSON (Puntos + Feedback)
    I->>P: Reporte Visual Industrial
```

## 🕵️ 3. Lógica del Monitor de Riesgo (EWS)
Visualiza la heurística de decisión para detectar abandono.

```mermaid
graph LR
    L[Logs Platform] --> P{Procesador}
    P -->|Inactividad > 7d| R1[+40 Pts]
    P -->|Entregas < 50%| R2[+30 Pts]
    P -->|Notas < 5| R3[+20 Pts]
    
    R1 --> S[Suma de Score]
    R2 --> S
    R3 --> S
    
    S --> D{Decisión}
    D -->|Score > 70| C[Riesgo Crítico]
    D -->|Score > 40| M[Riesgo Medio]
    D -->|Score < 40| B[Riesgo Bajo]
```

---
*Análisis Sistémico v1.0 | Ingeniería Pedagógica*
