import { loadPage } from './router.js';

document.addEventListener('DOMContentLoaded', () => {

    const authToken = localStorage.getItem('auth_token');

    if (!authToken) {
        window.location.href = 'login.html';
        return;
    }

    initializeMenu();

    const homeButton = document.querySelector('.menu-item[data-page="home"]');

    if (homeButton) {
        updateActiveButton(homeButton);
    }

    loadPage('home');
});

function initializeMenu() {

    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(button => {

        button.addEventListener('click', () => {

            const page = button.dataset.page;

            updateActiveButton(button);

            loadPage(page);
        });
    });
}

function updateActiveButton(activeButton) {

    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(button => {
        button.classList.remove('active');
    });

    activeButton.classList.add('active');
}