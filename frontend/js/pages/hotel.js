export { init };

async function init() {
    // Inicializar botones y listeners para hoteles
    const saveButton = document.getElementById('hotel-save-button');
    const resetButton = document.getElementById('hotel-reset-button');
    const editButton = document.getElementById('hotel-edit-button');
    const refreshButton = document.getElementById('hotel-refresh-button');

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

    // Cargar hoteles iniciales (cuando se implemente el backend)
    // await loadHoteles();
}

function cleanFields() {
    document.getElementById('hotel-id').value = '';
    document.getElementById('hotel-nombre').value = '';
    document.getElementById('hotel-ciudad').value = '';
    document.getElementById('hotel-precio').value = '';
    document.getElementById('hotel-estrellas').value = '';
    document.getElementById('hotel-form-feedback').textContent = '';
}
