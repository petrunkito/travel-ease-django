import { API_BASE, TOKEN_KEY } from './config.js';

function createHeaders() {
    const token = localStorage.getItem(TOKEN_KEY);
    const headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    };

    if (token) {
        headers.Authorization = `Token ${token}`;
    }

    return headers;
}

async function parseJson(response) {
    try {
        return await response.json();
    } catch (error) {
        return null;
    }
}

function requestResult(ok, content) {
    return {
        ok,
        content
    };
}

async function warehouseGet(path) {
    try {
        const response = await fetch(`${API_BASE}/warehouse/${path}/`, {
            method: 'GET',
            headers: createHeaders()
        });

        const payload = await parseJson(response);

        if (!response.ok) {
            return requestResult(false, payload);
        }

        return requestResult(true, payload || []);
    } catch (error) {
        return requestResult(false, null);
    }
}

export function getIngresosPorDestino() {
    return warehouseGet('ingresos-por-destino');
}

export function getTopClientes() {
    return warehouseGet('top-clientes');
}

export function getPaquetesMasVendidos() {
    return warehouseGet('paquetes-mas-vendidos');
}

export function getTemporadaAlta() {
    return warehouseGet('temporada-alta');
}
