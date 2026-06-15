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

export async function getReservas() {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservations`, {
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

export async function getReservaById(reservaId) {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservations/${reservaId}/`, {
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

export async function createReserva(payload) {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservations/`, {
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

export async function updateReserva(reservaId, payload) {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservations/${reservaId}/`, {
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

export async function updateReservaStatus(reservaId, payload) {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservations/${reservaId}/update_status/`, {
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

export async function deleteReserva(reservaId) {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservations/${reservaId}/`, {
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

export async function getReservationStatuses() {
    try {
        const response = await fetch(`${API_BASE}/reservations/reservation-statuses/`, {
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
