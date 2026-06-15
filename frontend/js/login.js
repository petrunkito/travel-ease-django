import { login } from './api/userApi.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const errorMessage = document.getElementById('login-error');

    const authToken = localStorage.getItem('auth_token');

    if (authToken) {
        window.location.href = 'index.html';
        return;
    }

    if (!form || !errorMessage) {
        return;
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.textContent = '';

        const formData = new FormData(form);
        const username = String(formData.get('username') || '').trim();
        const password = String(formData.get('password') || '').trim();

        if (!username || !password) {
            errorMessage.textContent = 'Completa usuario y contrasena.';
            return;
        }

        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Validando...';
        }

        try {
            const response = await login(username, password);
            const token = response?.content?.token;

            if (response?.ok && token) {
                localStorage.setItem('auth_token', token);
                window.location.href = 'index.html';
                return;
            }

            errorMessage.textContent = 'Credenciales invalidas o servidor no disponible.';
        } catch (error) {
            errorMessage.textContent = 'Credenciales invalidas o servidor no disponible.';
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Iniciar sesion';
            }
        }
    });
});
