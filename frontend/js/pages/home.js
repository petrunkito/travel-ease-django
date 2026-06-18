import {
    getIngresosPorDestino,
    getPaquetesMasVendidos,
    getTemporadaAlta,
    getTopClientes
} from '../api/warehouseApi.js';

export { init };

let chartInstances = [];

async function init() {
    destroyCharts();

    if (!window.Chart) {
        showStatus('No se pudo cargar Chart.js. Revisa el archivo js/chart.min.js.', true);
        return;
    }

    const results = await Promise.all([
        getIngresosPorDestino(),
        getTopClientes(),
        getPaquetesMasVendidos(),
        getTemporadaAlta()
    ]);

    const hasError = results.some(result => !result.ok);

    if (hasError) {
        showStatus('No se pudieron cargar todos los indicadores del warehouse. Verifica que la API de Django este activa.', true);
        return;
    }

    showStatus('', false, true);

    await waitForLayout();

    renderIncomeByDestination(results[0].content);
    renderTopClients(results[1].content);
    renderTopPackages(results[2].content);
    renderHighSeason(results[3].content);
}

function renderIncomeByDestination(items) {
    const rows = normalizeRows(items)
        .map(item => ({
            label: `${item.Ciudad}, ${item.Pais}`,
            value: toNumber(item.Ingresos)
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 8);

    setText('income-total', formatMoney(sumValues(rows)));
    renderDetailList('income-destination-detail', rows, formatMoney);
    createBarChart('income-destination-chart', rows, 'Ingresos', '#2f6bff', true, formatMoney);
}

function renderTopClients(items) {
    const rows = normalizeRows(items)
        .map(item => ({
            label: item.NombreCliente,
            value: toNumber(item.TotalComprado)
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 8);

    setText('clients-total', formatMoney(sumValues(rows)));
    renderDetailList('top-clients-detail', rows, formatMoney);
    createBarChart('top-clients-chart', rows, 'Total comprado', '#16a085', true, formatMoney);
}

function renderTopPackages(items) {
    const rows = normalizeRows(items)
        .map(item => ({
            label: item.NombrePaquete,
            value: toNumber(item.TotalReservas)
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 8);

    setText('packages-total', `${sumValues(rows)} reservas`);
    renderDetailList('top-packages-detail', rows, value => `${value} reservas`);
    createBarChart('top-packages-chart', rows, 'Reservas', '#f59e0b', false, value => `${value} reservas`);
}

function renderHighSeason(items) {
    const rows = normalizeRows(items)
        .map(item => ({
            label: translateMonth(item.MesNombre),
            value: toNumber(item.TotalVentas)
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 8);

    setText('season-total', formatMoney(sumValues(rows)));
    renderDetailList('high-season-detail', rows, formatMoney);
    createBarChart('high-season-chart', rows, 'Ventas por mes', '#7c3aed', false, formatMoney);
}

function createBarChart(canvasId, rows, label, color, horizontal, formatter) {
    const canvas = document.getElementById(canvasId);

    if (!canvas) return;

    const chart = new window.Chart(canvas, {
        type: 'bar',
        data: {
            labels: rows.map(row => row.label),
            datasets: [{
                label,
                data: rows.map(row => row.value),
                backgroundColor: rows.map((row, index) => softenColor(color, index)),
                borderColor: color,
                borderWidth: 1,
                borderRadius: 8,
                maxBarThickness: 34
            }]
        },
        options: buildChartOptions(horizontal, formatter)
    });

    chartInstances.push(chart);
}

function buildChartOptions(horizontal, formatter) {
    return {
        indexAxis: horizontal ? 'y' : 'x',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label(context) {
                        return `${context.dataset.label}: ${formatter(getParsedValue(context, horizontal))}`;
                    }
                }
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(106, 115, 135, 0.12)'
                },
                ticks: {
                    color: '#6a7387',
                    callback(value) {
                        return horizontal ? compactNumber(value) : shortenLabel(this.getLabelForValue(value));
                    }
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: !horizontal,
                    color: 'rgba(106, 115, 135, 0.12)'
                },
                ticks: {
                    color: '#6a7387',
                    autoSkip: false,
                    callback(value) {
                        if (!horizontal) {
                            return compactNumber(value);
                        }

                        return shortenLabel(this.getLabelForValue(value));
                    }
                }
            }
        }
    };
}

function renderDetailList(elementId, rows, formatter) {
    const list = document.getElementById(elementId);

    if (!list) return;

    list.innerHTML = rows.slice(0, 4).map((row, index) => `
        <li>
            <span>${index + 1}. ${escapeHtml(row.label)}</span>
            <strong>${formatter(row.value)}</strong>
        </li>
    `).join('');
}

function normalizeRows(items) {
    return Array.isArray(items) ? items : [];
}

function waitForLayout() {
    return new Promise(resolve => {
        requestAnimationFrame(() => {
            requestAnimationFrame(resolve);
        });
    });
}

function getParsedValue(context, horizontal) {
    return horizontal ? context.parsed.x : context.parsed.y;
}

function destroyCharts() {
    chartInstances.forEach(chart => chart.destroy());
    chartInstances = [];
}

function showStatus(message, isError, isHidden) {
    const status = document.getElementById('dashboard-status');

    if (!status) return;

    status.textContent = message;
    status.classList.toggle('is-error', Boolean(isError));
    status.classList.toggle('is-hidden', Boolean(isHidden));
}

function setText(elementId, value) {
    const element = document.getElementById(elementId);

    if (element) {
        element.textContent = value;
    }
}

function sumValues(rows) {
    return rows.reduce((total, row) => total + row.value, 0);
}

function toNumber(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
}

function formatMoney(value) {
    return new Intl.NumberFormat('es-NI', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(value);
}

function compactNumber(value) {
    return new Intl.NumberFormat('es-NI', {
        notation: 'compact',
        maximumFractionDigits: 1
    }).format(value);
}

function shortenLabel(label) {
    if (!label) return '';
    return label.length > 22 ? `${label.slice(0, 20)}...` : label;
}

function softenColor(color, index) {
    const alpha = Math.max(0.42, 0.9 - index * 0.06);
    const rgb = hexToRgb(color);
    return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`;
}

function hexToRgb(hex) {
    const cleanHex = hex.replace('#', '');
    const value = parseInt(cleanHex, 16);

    return {
        r: (value >> 16) & 255,
        g: (value >> 8) & 255,
        b: value & 255
    };
}

function translateMonth(monthName) {
    const months = {
        January: 'Enero',
        February: 'Febrero',
        March: 'Marzo',
        April: 'Abril',
        May: 'Mayo',
        June: 'Junio',
        July: 'Julio',
        August: 'Agosto',
        September: 'Septiembre',
        October: 'Octubre',
        November: 'Noviembre',
        December: 'Diciembre'
    };

    return months[monthName] || monthName;
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
