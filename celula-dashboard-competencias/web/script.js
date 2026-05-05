// Simulación de carga de datos (En producción se cargaría del JSON generado)
const data = {
    "student_name": "Juan Perez",
    "course": "Arquitectura de Automatizacion",
    "competencies": [
        {"name": "Pensamiento Critico", "value": 85, "average": 70},
        {"name": "Resolucion de Problemas", "value": 92, "average": 75},
        {"name": "Trabajo en Equipo", "value": 65, "average": 80},
        {"name": "Competencia Tecnica", "value": 88, "average": 65},
        {"name": "Comunicacion", "value": 70, "average": 72}
    ],
    "ai_insight": "Juan destaca en resolución de problemas técnicos, pero necesita reforzar su colaboración en equipo para equilibrar su perfil profesional."
};

document.addEventListener('DOMContentLoaded', () => {
    // Actualizar UI
    document.getElementById('student-info').textContent = `${data.student_name} | ${data.course}`;
    document.getElementById('ai-insight-text').textContent = data.ai_insight;

    // Configurar Chart.js
    const ctx = document.getElementById('competencyChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.competencies.map(c => c.name),
            datasets: [{
                label: 'Alumno',
                data: data.competencies.map(c => c.value),
                fill: true,
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: '#6366f1',
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#6366f1'
            }, {
                label: 'Media Grupo',
                data: data.competencies.map(c => c.average),
                fill: true,
                backgroundColor: 'rgba(244, 63, 94, 0.1)',
                borderColor: '#f43f5e',
                borderDash: [5, 5],
                pointBackgroundColor: '#f43f5e',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#f43f5e'
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: { color: '#94a3b8', font: { size: 12 } },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#f8fafc' }
                }
            }
        }
    });
});
