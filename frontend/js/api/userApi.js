import { API_BASE } from './config.js';

export const api = API_BASE;

async function parseResponseBody(response) {
    if (response.status === 204) {
        return null;
    }

    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('application/json')) {
        try {
            return await response.json();
        } catch (error) {
            return null;
        }
    }

    try {
        const text = await response.text();
        return text || null;
    } catch (error) {
        return null;
    }
}

export async function login(username, password) {
    try {
        const response = await fetch(`${api}/users/login/`, {
            method: 'POST',
            body: JSON.stringify({
                username,
                password
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8'
            }
        });

        const payload = await parseResponseBody(response);

        if (!response.ok) {
            return {
                ok: false,
                content: payload
            };
        }

        return {
            ok: true,
            content: payload
        };
    } catch (error) {
        return {
            ok: false,
            content: null
        };
    }
}