import {createHotel, deleteHotel, getHotelById, getHoteles,updateHotel, createHotelPrice, getHotelPrices} from '../../api/hotelApi.js'
export {init}

/*
 <div class="table-wrap">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Ciudad</th>
                        <th>Estrellas</th>
                        <th>Precio</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody id="hotel-table-body">
                    <tr>
                        <td colspan="5" class="empty-state">Cargando hoteles...</td>
                    </tr>
                </tbody>
            </table>
        </div>
*/

let fieldHotelName = null;
let fieldHotelCity = null;
let fieldHotelPrice = null;
let fieldHotelEstrellas = null;

let buttonAgregar = null;
let buttonActualizar = null;
let buttonLimpiar = null;

async function init() {
    fieldHotelName = document.getElementById("hotel-nombre");
    fieldHotelCity = document.getElementById("hotel-ciudad");
    fieldHotelPrice = document.getElementById("hotel-precio");
    fieldHotelEstrellas = document.getElementById("hotel-estrellas");

    buttonAgregar = document.getElementById("hotel-save-button");
    buttonActualizar = document.getElementById("hotel-edit-button");
    buttonLimpiar = document.getElementById("hotel-reset-button");

    loadHoteles();

    buttonAgregar.addEventListener("click", async (e) => {
        e.preventDefault();
        await createNewHotel();
    })

    buttonActualizar.addEventListener("click", async (e) => {
        e.preventDefault();
        await updateSelectedHotel();
    })

    buttonLimpiar.addEventListener("click", (e) => {
        e.preventDefault();
        clearHotelForm();
    })
}

async function loadHoteles() {
    const result = await getHoteles();

    if (!result.ok) {
        alert("Ocurrió un error al cargar los hoteles");
        return;
    }

    const hoteles = result.content;
    const tableBody = document.getElementById("hotel-table-body");
    tableBody.innerHTML = "";

    hoteles.forEach(hotel => {
        const row = document.createElement("tr");
        row.dataset.hotelId = hotel.id;

        const cellNombre = document.createElement("td");
        cellNombre.textContent = hotel.name;
        row.appendChild(cellNombre);

        const cellCiudad = document.createElement("td");
        cellCiudad.textContent = hotel.city;
        row.appendChild(cellCiudad);
        
        const cellEstrellas = document.createElement("td");
        cellEstrellas.textContent = hotel.stars;
        row.appendChild(cellEstrellas);

        const cellPrecio = document.createElement("td");
        cellPrecio.textContent = hotel.current_price;
        row.appendChild(cellPrecio);

        ///
        const cellEdit = document.createElement("td");
        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.classList.add("btn", "btn-primary", "btn-sm");
        editButton.textContent = "Editar";
        editButton.addEventListener("click", () => {
            showHotelForEdit(hotel.id);
        });
        cellEdit.appendChild(editButton);
        row.appendChild(cellEdit);

        const cellDelete = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("btn", "btn-primary", "btn-sm");
        deleteButton.textContent = "Eliminar";
        deleteButton.addEventListener("click", () => {
            deleteSelectedHotel(hotel.id);
        });
        cellDelete.appendChild(deleteButton);
        row.appendChild(cellDelete);

        tableBody.appendChild(row);

    });
}

let selectedHotelId = null;
let previousHotelPrice = null;
async function showHotelForEdit(hotelId) {
    selectedHotelId = hotelId;

    const result = await getHotelById(hotelId);
    if (!result.ok) {
        alert("Ocurrió un error al obtener los detalles del hotel");
        return;
    }
    
    const hotel = result.content;
    fieldHotelName.value = hotel.name;
    fieldHotelCity.value = hotel.city;
    fieldHotelPrice.value = hotel.current_price;
    fieldHotelEstrellas.value = hotel.stars;
    previousHotelPrice = hotel.current_price;
}

async function deleteSelectedHotel(hotelId) {
    if (!confirm("¿Está seguro de que desea eliminar este hotel?")) {
        return;
    }

    const result = await deleteHotel(hotelId);
    if (!result.ok) {
        alert("Ocurrió un error al eliminar el hotel");
        return;
    }

    alert("Hotel eliminado exitosamente");
    loadHoteles();
}

async function updateSelectedHotel() {
    if (selectedHotelId === null) {
        alert("No hay un hotel seleccionado para actualizar");
        return;
    }

    if (!verifyHotelForm()) return;
    
    const updatedHotel = {
        name: fieldHotelName.value.trim(),
        city: fieldHotelCity.value.trim(),
        stars: parseInt(fieldHotelEstrellas.value)
    };

    if (parseFloat(fieldHotelPrice.value) !== previousHotelPrice) {
        const priceResult = await createHotelPrice(
            selectedHotelId,
            {price: parseFloat(fieldHotelPrice.value)}
        );

        if (!priceResult.ok) {
            alert("Ocurrió un error al actualizar el precio del hotel");
            return;
        }
    }

    const result = await updateHotel(selectedHotelId, updatedHotel);
    if (!result.ok) {
        alert("Ocurrió un error al actualizar el hotel");
        return;
    }

    alert("Hotel actualizado exitosamente");
    clearHotelForm();
    loadHoteles();
}

function verifyHotelForm() {
    if(fieldHotelName.value.trim() === "") {
        alert("El nombre del hotel es requerido");
        return false;
    }

    if(fieldHotelCity.value.trim() === "") {
        alert("La ciudad del hotel es requerida");
        return false;
    }

    if(fieldHotelPrice.value.trim() === "" || isNaN(parseFloat(fieldHotelPrice.value))) {
        alert("El precio del hotel es requerido y debe ser un número válido");
        return false;
    }

    if(fieldHotelEstrellas.value.trim() === "" || isNaN(parseInt(fieldHotelEstrellas.value)) || parseInt(fieldHotelEstrellas.value) < 1 || parseInt(fieldHotelEstrellas.value) > 5) {
        alert("Las estrellas del hotel son requeridas y deben ser un número entero entre 1 y 5");
        return false;
    }

    return true;
}

function clearHotelForm() {
    fieldHotelName.value = "";
    fieldHotelCity.value = "";
    fieldHotelPrice.value = "";
    fieldHotelEstrellas.value = "";
    selectedHotelId = null;
    previousHotelPrice = null;
}


async function createNewHotel()
{
    if (!verifyHotelForm()) return;
    
    const newHotel = {
        name: fieldHotelName.value.trim(),
        city: fieldHotelCity.value.trim(),
        price: parseFloat(fieldHotelPrice.value),
        stars: parseInt(fieldHotelEstrellas.value)
    };

    const result = await createHotel(newHotel);
    if (!result.ok) {
        alert("Ocurrió un error al crear el hotel");
        return;
    }

    alert("Hotel creado exitosamente");
    clearHotelForm();
    loadHoteles();
}