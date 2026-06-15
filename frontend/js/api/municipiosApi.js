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

export async function getMunicipios() {
    try {
        const response = await fetch(`${API_BASE}/catalogos/municipios/`, {
            method: 'GET',
            headers: createHeaders()
        });

        const payload = await parseJson(response);

        if (!response.ok) {
            return requestResult(false, payload);
        }

        return requestResult(true, payload);
    } catch (error) {
        return requestResult(false, null);
    }
}

export async function getMunicipiosByDepartamento(idDepartamento) {
    try {
        const response = await fetch(`${API_BASE}/municipios/departamento/${idDepartamento}/`, {
            method: 'GET',
            headers: createHeaders()
        });

        const payload = await parseJson(response);

        if (!response.ok) {
            return requestResult(false, payload);
        }

        return requestResult(true, payload);
    } catch (error) {
        return requestResult(false, null);
    }
}

export async function createMunicipio(payload) {
    try {
        const response = await fetch(`${API_BASE}/catalogos/municipios/`, {
            method: 'POST',
            headers: createHeaders(),
            body: JSON.stringify(payload || {})
        });

        const payloadResponse = await parseJson(response);

        if (!response.ok) {
            return requestResult(false, payloadResponse);
        }

        return requestResult(true, payloadResponse);
    } catch (error) {
        return requestResult(false, null);
    }
}
