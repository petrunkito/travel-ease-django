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

export async function getHoteles() {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/`, {
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

export async function getHotelById(hotelId) {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/${hotelId}/`, {
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

export async function createHotel(payload) {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/`, {
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

export async function updateHotel(hotelId, payload) {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/${hotelId}/`, {
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

export async function deleteHotel(hotelId) {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/${hotelId}/`, {
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

export async function createHotelPrice(hotelId, payload) {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/${hotelId}/prices/`, {
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

export async function getHotelPrices(hotelId) {
    try {
        const response = await fetch(`${API_BASE}/services/hotels/${hotelId}/prices/`, {
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
