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

// OBTENER TODOS LOS VUELOS
export async function getVuelos() {
    try {
        const response = await fetch(`${API_BASE}/services/flights/`, {
            method: 'GET',
            headers: createHeaders()
        });

        if (!response.ok) {
            const payload = await parseJson(response);
            return requestResult(false, payload);
        }

        const payload = await parseJson(response);
        return requestResult(true, payload);
    } catch (error) {
        return requestResult(false, null);
    }
}

// OBTENER UN VUELO ESPECÍFICO
export async function getVueloById(vueloId) {
    try {
        const response = await fetch(`${API_BASE}/services/flights/${vueloId}/`, {
            method: 'GET',
            headers: createHeaders()
        });

        if (!response.ok) {
            const payload = await parseJson(response);
            return requestResult(false, payload);
        }

        const payload = await parseJson(response);
        return requestResult(true, payload);
    } catch (error) {
        return requestResult(false, null);
    }
}

// CREAR UN NUEVO VUELO
export async function createVuelo(payload) {
    try {
        const response = await fetch(`${API_BASE}/services/flights/`, {
            method: 'POST',
            headers: createHeaders(),
            body: JSON.stringify(payload || {})
        });

        if (!response.ok) {
            const payloadResponse = await parseJson(response);
            return requestResult(false, payloadResponse);
        }

        const payloadResponse = await parseJson(response);
        return requestResult(true, payloadResponse);
    } catch (error) {
        return requestResult(false, null);
    }
}

// ACTUALIZAR UN VUELO (sin editar precio)
export async function updateVuelo(vueloId, payload) {
    try {
        const response = await fetch(`${API_BASE}/services/flights/${vueloId}/`, {
            method: 'PUT',
            headers: createHeaders(),
            body: JSON.stringify(payload || {})
        });

        if (!response.ok) {
            const payloadResponse = await parseJson(response);
            return requestResult(false, payloadResponse);
        }

        const payloadResponse = await parseJson(response);
        return requestResult(true, payloadResponse);
    } catch (error) {
        return requestResult(false, null);
    }
}

// ELIMINAR UN VUELO
export async function deleteVuelo(vueloId) {
    try {
        const response = await fetch(`${API_BASE}/services/flights/${vueloId}/`, {
            method: 'DELETE',
            headers: createHeaders()
        });

        if (!response.ok) {
            const payload = await parseJson(response);
            return requestResult(false, payload);
        }

        const payload = await parseJson(response);
        return requestResult(true, payload);
    } catch (error) {
        return requestResult(false, null);
    }
}

// OBTENER HISTORIAL DE PRECIOS DE UN VUELO
export async function getVueloPrices(vueloId) {
    try {
        const response = await fetch(`${API_BASE}/services/flights/${vueloId}/prices/`, {
            method: 'GET',
            headers: createHeaders()
        });

        if (!response.ok) {
            const payload = await parseJson(response);
            return requestResult(false, payload);
        }

        const payload = await parseJson(response);
        return requestResult(true, payload);
    } catch (error) {
        return requestResult(false, null);
    }
}

// ACTUALIZAR PRECIO DE UN VUELO
export async function updateVueloPrice(vueloId, pricePayload) {
    try {
        const response = await fetch(`${API_BASE}/services/flights/${vueloId}/prices/`, {
            method: 'POST',
            headers: createHeaders(),
            body: JSON.stringify(pricePayload || {})
        });

        if (!response.ok) {
            const payloadResponse = await parseJson(response);
            return requestResult(false, payloadResponse);
        }

        const payloadResponse = await parseJson(response);
        return requestResult(true, payloadResponse);
    } catch (error) {
        return requestResult(false, null);
    }
}
