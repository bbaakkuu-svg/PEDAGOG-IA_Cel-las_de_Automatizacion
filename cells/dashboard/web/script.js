document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    
    document.getElementById('export-btn').addEventListener('click', exportToPDF);
});

function exportToPDF() {
    const element = document.querySelector('.container');
    const opt = {
        margin:       0.5,
        filename:     'Reporte_PedagogIA.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, backgroundColor: '#0f172a' },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
    };

    // Estilo temporal para la exportación para asegurar que todo se vea bien
    const btn = document.getElementById('export-btn');
    const syncBtn = btn.nextElementSibling;
    btn.style.display = 'none';
    syncBtn.style.display = 'none';

    html2pdf().set(opt).from(element).save().then(() => {
        btn.style.display = 'block';
        syncBtn.style.display = 'block';
    });
}

async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        if (data.error) {
            console.error(data.error);
            showError(data.error);
            return;
        }

        updateStats(data.stats);
        renderCompetencyChart(data.competencies);
        updateRiskList(data.at_risk);
        generateInsights(data);
        
        document.getElementById('last-update').innerText = `Última actualización: ${data.last_update}`;
        
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateStats(stats) {
    animateValue('total-evals', 0, stats.total_evaluaciones, 1000);
    animateValue('avg-grade', 0, stats.nota_promedio, 1000, true);
    document.getElementById('pass-rate').innerText = `${stats.tasa_aprobacion}%`;
    animateValue('risk-count', 0, stats.alerta_riesgo, 1000);
}

function renderCompetencyChart(competencies) {
    const ctx = document.getElementById('competencyChart').getContext('2d');
    
    // Si no hay datos, mostrar placeholder
    if (!competencies || competencies.length === 0) {
        return;
    }

    const labels = competencies.map(c => c.name);
    const values = competencies.map(c => c.value);

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Promedio de Cohorte',
                data: values,
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: '#6366f1',
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#6366f1',
                borderWidth: 3
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: { color: '#94a3b8', font: { size: 12 } },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function updateRiskList(atRisk) {
    const list = document.getElementById('at-risk-list');
    list.innerHTML = '';

    if (!atRisk || atRisk.length === 0) {
        list.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 20px;">No hay alumnos en riesgo detectados.</p>';
        return;
    }

    atRisk.forEach(student => {
        const item = document.createElement('div');
        item.className = 'risk-item';
        
        // El formato depende de si viene del Monitor o del Auditor
        const id = student.student_id || student['Entidad ID'];
        const score = student.risk_score || (student.Valor * 10);
        const level = student.risk_level || (student.Valor < 3 ? "CRITICO" : "MEDIO");

        item.innerHTML = `
            <div>
                <span style="font-weight: bold; color: white;">${id}</span>
                <div style="font-size: 0.8rem; color: var(--text-muted);">Score de Riesgo: ${score}</div>
            </div>
            <span class="risk-tag tag-${level.toLowerCase()}">${level}</span>
        `;
        list.appendChild(item);
    });
}

function generateInsights(data) {
    const textElement = document.getElementById('ai-insight-text');
    let insight = "";

    if (data.stats.nota_promedio > 7) {
        insight = "La cohorte presenta un rendimiento académico sólido. Se observa una alta correlación entre el uso de la plataforma y las calificaciones finales.";
    } else if (data.stats.nota_promedio < 5) {
        insight = "Se detecta una tendencia crítica de bajo rendimiento. Se recomienda una intervención inmediata revisando los materiales de la célula 'Generador'.";
    } else {
        insight = "El rendimiento es estable, pero hay una brecha notable en competencias de Pensamiento Computacional.";
    }

    if (data.stats.alerta_riesgo > 0) {
        insight += ` Hay ${data.stats.alerta_riesgo} estudiantes que requieren atención prioritaria por inactividad prolongada.`;
    }

    textElement.innerText = insight;
}

function animateValue(id, start, end, duration, isFloat = false) {
    const obj = document.getElementById(id);
    if (!obj) return;
    
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const val = progress * (end - start) + start;
        obj.innerHTML = isFloat ? val.toFixed(1) : Math.floor(val);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function showError(msg) {
    const container = document.querySelector('.container');
    container.innerHTML = `<div style="text-align:center; padding:50px;">
        <h2 style="color:var(--danger)">✘ Error de Datos</h2>
        <p style="color:var(--text-muted); margin-top:10px;">${msg}</p>
        <button onclick="location.reload()" style="margin-top:20px; padding:10px 20px; background:var(--primary); border:none; color:white; border-radius:8px; cursor:pointer;">Reintentar</button>
    </div>`;
}
