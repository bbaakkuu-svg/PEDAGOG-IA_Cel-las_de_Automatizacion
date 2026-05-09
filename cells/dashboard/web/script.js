async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateUI(data) {
    // Stats
    document.getElementById('total-evaluations').textContent = data.stats.total_evaluaciones;
    document.getElementById('active-reinforcements').textContent = data.stats.total_reforzamientos;
    document.getElementById('total-cost').textContent = `$${data.stats.costo_total_usd.toFixed(4)}`;
    document.getElementById('avg-latency').textContent = `${data.stats.latencia_media_ms}ms`;
    document.getElementById('last-update').textContent = data.last_update;

    // Cycles Table
    const tableBody = document.getElementById('cycles-table-body');
    tableBody.innerHTML = '';
    data.recent_cycles.forEach(cycle => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${cycle.student}</td>
            <td><span style="color: ${cycle.grade >= 5 ? '#00ffaa' : '#ff4444'}">${cycle.grade}/10</span></td>
            <td><span class="status-badge ${cycle.status.toLowerCase()}">${cycle.status}</span></td>
            <td style="color: #a0a0b0; font-size: 0.8rem">${cycle.timestamp}</td>
        `;
        tableBody.appendChild(row);
    });

    // Ops Feed
    const feed = document.getElementById('ops-feed');
    feed.innerHTML = '';
    data.ia_ops.slice().reverse().forEach(op => {
        const item = document.createElement('div');
        item.className = 'feed-item';
        item.innerHTML = `
            <div class="meta">
                <span>${op.cell_id.toUpperCase()}</span>
                <span>${op.latency_ms.toFixed(1)}ms</span>
            </div>
            <div class="content">${op.model_id} - ${op.status}</div>
        `;
        feed.appendChild(item);
    });

    // Chart update
    updateChart(data.ia_ops);
}

let latencyChart;
function updateChart(ops) {
    const ctx = document.getElementById('latencyChart').getContext('2d');
    const labels = ops.map((_, i) => i + 1);
    const latencies = ops.map(op => op.latency_ms);

    if (latencyChart) {
        latencyChart.data.labels = labels;
        latencyChart.data.datasets[0].data = latencies;
        latencyChart.update();
    } else {
        latencyChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Latencia IA (ms)',
                    data: latencies,
                    borderColor: '#00d2ff',
                    backgroundColor: 'rgba(0, 210, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// Initial fetch and interval
fetchData();
setInterval(fetchData, 5000); // Refresh every 5s
