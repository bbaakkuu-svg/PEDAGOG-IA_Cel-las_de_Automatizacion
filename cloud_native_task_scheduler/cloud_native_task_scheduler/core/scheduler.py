from .interfaces import TaskExecutor

class CloudNativeScheduler:
    """
    El Scheduler: No sabe DÓNDE se ejecutan las tareas.
    Solo sabe QUÉ tareas ejecutar y utiliza el ejecutor INYECTADO.
    """
    
    def __init__(self, executor: TaskExecutor):
        # Inyección de Dependencia
        self.executor = executor

    def schedule_daily_report(self):
        task_name = "Generate_Docensas_KPI_Report"
        payload = {"format": "PDF", "recipients": ["admin@docensas.com"]}
        
        return self.executor.run(task_name, payload)
