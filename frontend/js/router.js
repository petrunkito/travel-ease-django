const originalFetch = window.fetch;
window.fetch = async function (url, options) {
    const response = await originalFetch(url, options);
    if ((response.status === 401 || response.status === 403) && options?.method === 'GET') {
        window.location.href = 'login.html';
    }
    return response;
};

export async function loadPage(pageName) {

    try {

        const content = document.getElementById('app-content');

        const title = document.getElementById('page-title');

        // LIMPIAR CONTENIDO
        content.innerHTML = '';

        // CARGAR HTML
        const response = await fetch(`views/${pageName}.html`);

        const html = await response.text();

        content.innerHTML = html;

        // ACTUALIZAR TITULO
        title.textContent = getPageTitle(pageName);

        // REMOVER CSS ANTERIOR
        removeDynamicStyles();

        // CARGAR CSS DE LA PAGINA
        loadPageCSS(pageName);

        // CARGAR JS DE LA PAGINA
        const module = await import(`./pages/${pageName}.js`);

        // EJECUTAR INIT SI EXISTE
        if (module.init) {
            module.init();
        }

    } catch (error) {

        
    }
}

function getPageTitle(pageName) {

    const titles = {

        home: 'Inicio',
        servicios: 'Servicios',
        paquetes: 'Paquetes Turísticos',
        reservas: 'Reservas',
        clientes: 'Clientes'
    };

    return titles[pageName] || 'TravelEase';
}

function loadPageCSS(pageName) {

    const link = document.createElement('link');

    link.rel = 'stylesheet';

    link.href = `css/${pageName}.css`;

    link.classList.add('dynamic-page-style');

    document.head.appendChild(link);
}

function removeDynamicStyles() {

    const styles = document.querySelectorAll('.dynamic-page-style');

    styles.forEach(style => style.remove());
}