export { init };

let currentService = 'vuelo';
let currentModule = null;

async function init() {
    // Cargar el servicio inicial (vuelo)
    await loadService('vuelo');

    // Inicializar listeners de tabs
    const tabs = document.querySelectorAll('.servicios-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', async (e) => {
            const service = tab.dataset.service;
            await loadService(service);
        });
    });
}

async function loadService(serviceName) {
    try {
        // Actualizar estado de tabs
        updateTabsState(serviceName);
        currentService = serviceName;

        // Contenedor donde se cargará el contenido
        const content = document.getElementById('servicios-content');
        content.innerHTML = '';

        // Cargar HTML del servicio
        const response = await fetch(`views/servicios/${serviceName}.html`);
        const html = await response.text();
        content.innerHTML = html;

        // Cargar el módulo JS del servicio
        const module = await import(`./servicios/${serviceName}.js`);

        // Ejecutar init si existe
        if (module.init) {
            await module.init();
        }

        currentModule = module;

    } catch (error) {
        console.error(`Error cargando servicio ${serviceName}:`, error);
    }
}

function updateTabsState(activeName) {
    const tabs = document.querySelectorAll('.servicios-tab');
    tabs.forEach(tab => {
        const isActive = tab.dataset.service === activeName;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive);
    });
}