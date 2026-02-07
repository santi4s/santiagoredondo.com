/**
 * Lógica compartida para mostrar datos de Wallapop en las páginas de consolas.
 */

const DATA_BASE_URL = '/consolas-retro/data';

async function loadWallapopData() {
    try {
        const response = await fetch(`${DATA_BASE_URL}/history.json`);
        if (!response.ok) throw new Error('Data not available');
        return await response.json();
    } catch (e) {
        console.warn('No se pudieron cargar los datos de Wallapop:', e);
        return null;
    }
}

function getConsoleHistory(history, consoleKey) {
    return history
        .filter(entry => entry.consoles && entry.consoles[consoleKey])
        .map(entry => ({
            date: entry.date,
            ...entry.consoles[consoleKey]
        }));
}

function renderStatsPanel(containerId, latestData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!latestData) {
        container.innerHTML = '<p style="opacity: 0.6;">Datos de mercado no disponibles todav\u00eda.</p>';
        return;
    }

    const fmt = (val) => val !== null && val !== undefined ? val + ' \u20ac' : 'N/A';

    container.innerHTML = `
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-value">${latestData.available_count ?? 0}</div>
                <div class="stat-label">Anuncios activos</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${latestData.sold_count ?? 0}</div>
                <div class="stat-label">Vendidos</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${fmt(latestData.avg_offer_price)}</div>
                <div class="stat-label">Precio medio oferta</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${fmt(latestData.avg_sold_price)}</div>
                <div class="stat-label">Precio medio venta</div>
            </div>
        </div>
    `;
}

function renderPriceChart(canvasId, consoleData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || consoleData.length === 0) return;

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: consoleData.map(d => d.date),
            datasets: [
                {
                    label: 'Precio medio oferta',
                    data: consoleData.map(d => d.avg_offer_price),
                    borderColor: '#ffdd00',
                    backgroundColor: 'rgba(255, 221, 0, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                },
                {
                    label: 'Precio medio venta',
                    data: consoleData.map(d => d.avg_sold_price),
                    borderColor: '#ff006e',
                    backgroundColor: 'rgba(255, 0, 110, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#fff',
                        font: { family: "'Courier New', monospace" }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#ccc',
                        font: { family: "'Courier New', monospace" },
                        maxRotation: 45,
                    },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                y: {
                    ticks: {
                        color: '#ccc',
                        font: { family: "'Courier New', monospace" },
                        callback: value => value + ' \u20ac'
                    },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                }
            }
        }
    });
}

function renderListingsChart(canvasId, consoleData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || consoleData.length === 0) return;

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: consoleData.map(d => d.date),
            datasets: [
                {
                    label: 'Activos',
                    data: consoleData.map(d => d.available_count),
                    backgroundColor: 'rgba(255, 221, 0, 0.7)',
                    borderColor: '#ffdd00',
                    borderWidth: 1,
                },
                {
                    label: 'Vendidos',
                    data: consoleData.map(d => d.sold_count),
                    backgroundColor: 'rgba(255, 0, 110, 0.7)',
                    borderColor: '#ff006e',
                    borderWidth: 1,
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#fff',
                        font: { family: "'Courier New', monospace" }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#ccc',
                        font: { family: "'Courier New', monospace" },
                        maxRotation: 45,
                    },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                y: {
                    ticks: {
                        color: '#ccc',
                        font: { family: "'Courier New', monospace" },
                    },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                }
            }
        }
    });
}

async function initWallapopSection(consoleKey) {
    const history = await loadWallapopData();
    if (!history) return;

    const consoleHistory = getConsoleHistory(history, consoleKey);
    if (consoleHistory.length === 0) return;

    // Mostrar la sección (está oculta por defecto hasta que haya datos)
    const section = document.getElementById('wallapop-section');
    if (section) section.style.display = 'block';

    const latest = consoleHistory[consoleHistory.length - 1];
    renderStatsPanel('wallapop-stats', latest);
    renderPriceChart('price-chart', consoleHistory);
    renderListingsChart('listings-chart', consoleHistory);
}
