document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/data');
        if (!response.ok) throw new Error('Data no disponible');
        const data = await response.json();

        // Actualizar UI
        document.getElementById('student-info').textContent = `${data.student_name || 'Desconocido'} | ${data.course || 'Sin curso'}`;
        document.getElementById('ai-insight-text').textContent = data.ai_insight || 'No hay insights disponibles.';

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
                responsive: true,
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
    } catch (error) {
        document.getElementById('student-info').textContent = 'Error al cargar los datos';
        document.getElementById('ai-insight-text').textContent = 'Ocurrió un error: ' + error.message;
    }

    // Funcionalidad del botón de exportar (Low-Hanging Fruit)
    document.getElementById('export-btn').addEventListener('click', () => {
        // Un enfoque simple para exportar a PDF es usar window.print() 
        // y ocultar elementos UI en CSS, o simplemente imprimir tal cual.
        window.print();
    });
});
