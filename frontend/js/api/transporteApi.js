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

export async function getTransportes() {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/`, {
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

export async function getTransporteById(transporteId) {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/${transporteId}/`, {
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

export async function createTransporte(payload) {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/`, {
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

export async function updateTransporte(transporteId, payload) {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/${transporteId}/`, {
            method: 'PATCH',
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

export async function deleteTransporte(transporteId) {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/${transporteId}/`, {
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

export async function createTransportePrice(transporteId, payload) {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/${transporteId}/prices/`, {
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

export async function getTransportePrices(transporteId) {
    try {
        const response = await fetch(`${API_BASE}/services/transportation/${transporteId}/prices/`, {
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
