export { init };

async function init() {
    // Inicializar botones y listeners para transportes
    const saveButton = document.getElementById('transporte-save-button');
    const resetButton = document.getElementById('transporte-reset-button');
    const editButton = document.getElementById('transporte-edit-button');
    const refreshButton = document.getElementById('transporte-refresh-button');

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

    // Cargar transportes iniciales (cuando se implemente el backend)
    // await loadTransportes();
}

function cleanFields() {
    document.getElementById('transporte-id').value = '';
    document.getElementById('transporte-tipo').value = '';
    document.getElementById('transporte-nombre').value = '';
    document.getElementById('transporte-origen').value = '';
    document.getElementById('transporte-destino').value = '';
    document.getElementById('transporte-precio').value = '';
    document.getElementById('transporte-form-feedback').textContent = '';
}
