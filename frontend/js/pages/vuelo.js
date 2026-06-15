export { init };

async function init() {
    // Inicializar botones y listeners para vuelos
    const saveButton = document.getElementById('vuelo-save-button');
    const resetButton = document.getElementById('vuelo-reset-button');
    const editButton = document.getElementById('vuelo-edit-button');
    const refreshButton = document.getElementById('vuelo-refresh-button');

    if (saveButton) {
        saveButton.addEventListener('click', (e) => {
            e.preventDefault();
            
        });
    }

    if (resetButton) {
        resetButton.addEventListener('click', (e) => {
            e.preventDefault();
            cleanFields();
        });
    }

    if (editButton) {
        editButton.addEventListener('click', (e) => {
            e.preventDefault();
            
        });
    }

    if (refreshButton) {
        refreshButton.addEventListener('click', async (e) => {
            e.preventDefault();
            
        });
    }

    // Cargar vuelos iniciales (cuando se implemente el backend)
    // await loadVuelos();
}

function cleanFields() {
    document.getElementById('vuelo-id').value = '';
    document.getElementById('vuelo-aerolinea').value = '';
    document.getElementById('vuelo-origen').value = '';
    document.getElementById('vuelo-destino').value = '';
    document.getElementById('vuelo-fecha-salida').value = '';
    document.getElementById('vuelo-fecha-entrada').value = '';
    document.getElementById('vuelo-precio').value = '';
    document.getElementById('vuelo-form-feedback').textContent = '';
}
