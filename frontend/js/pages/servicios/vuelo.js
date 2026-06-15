import { getVuelos, createVuelo , getVueloById, updateVuelo, updateVueloPrice, deleteVuelo} from "../../api/vueloApi.js"



export { init }


let fieldAerolinea = null
let fieldOrigen = null
let fieldDestino = null
let fieldFechaSalida = null
let fieldFechaEntreda = null
let fieldPrecio = null
let fieldButtonSave = null
let fieldButtonClear = null
let fieldButtonEdit = null

async function init() {
    fieldAerolinea = document.getElementById('vuelo-aerolinea');
    fieldOrigen = document.getElementById('vuelo-origen');
    fieldDestino = document.getElementById('vuelo-destino');
    fieldFechaSalida = document.getElementById('vuelo-fecha-salida');
    fieldFechaEntreda = document.getElementById('vuelo-fecha-entrada');
    fieldPrecio = document.getElementById('vuelo-precio');
    fieldButtonSave = document.getElementById('vuelo-save-button');
    fieldButtonClear = document.getElementById('vuelo-clear-button');
    fieldButtonEdit = document.getElementById('vuelo-edit-button');


    loadVuelos();

    fieldButtonSave.addEventListener("click", createFlight);
    fieldButtonClear.addEventListener("click", clearFields);
    fieldButtonEdit.addEventListener("click", async (e) => {
        e.preventDefault();
        await updateFlight();
    })


}

async function loadVuelos() {
    const result = await getVuelos();

    if (!result.ok) {
        alert("Ocurrió un error al cargar los vuelos");
        return;
    }

    const vuelos = result.content;
    const tableBody = document.getElementById("vuelo-table-body");
    tableBody.innerHTML = "";

    vuelos.forEach(vuelo => {
        const row = document.createElement("tr");
        row.dataset.vueloId = vuelo.id


        const cellAerolinea = document.createElement("td");
        cellAerolinea.textContent = vuelo.airline;
        row.appendChild(cellAerolinea);

        const cellOrigen = document.createElement("td");
        cellOrigen.textContent = vuelo.origin;
        row.appendChild(cellOrigen);

        const cellDestino = document.createElement("td");
        cellDestino.textContent = vuelo.destination;
        row.appendChild(cellDestino);

        const cellFechaSalida = document.createElement("td");
        cellFechaSalida.textContent = new Date(vuelo.departure_date).toLocaleString();
        row.appendChild(cellFechaSalida);

        const cellFechaEntrada = document.createElement("td");
        cellFechaEntrada.textContent = new Date(vuelo.arrival_date).toLocaleString();
        row.appendChild(cellFechaEntrada);

        const cellPrecio = document.createElement("td");
        cellPrecio.textContent = `${vuelo.current_price.toFixed(2)}`;
        row.appendChild(cellPrecio);

        let cellAccionEditar = document.createElement("td")
        let editButton = document.createElement("button")
        editButton.textContent = "Editar"
        editButton.classList.add("btn", "btn-primary", "btn-sm")
        // editButton.addEventListener("click", showCustomerForEdit)
        cellAccionEditar.appendChild(editButton)
        row.appendChild(cellAccionEditar)

        editButton.addEventListener("click", async (e) => {
            e.preventDefault();
            showFlightForEdit(e);
        })


        let cellAccionEliminar = document.createElement("td")
        let deleteButton = document.createElement("button")
        deleteButton.textContent = "Eliminar"
        deleteButton.classList.add("btn", "btn-primary", "btn-sm")
        // editButton.addEventListener("click", showCustomerForEdit)
        cellAccionEliminar.appendChild(deleteButton)
        row.appendChild(cellAccionEliminar)

        deleteButton.addEventListener("click", async (e) => {
            e.preventDefault();
            deleteFlight(e);
        })
        tableBody.appendChild(row);
    });


}

async function verifyFields() {

    if (fieldAerolinea.value.trim() === "") {
        alert("El campo Aerolínea es obligatorio")
        return false;
    }

    if (fieldPrecio.value.trim() === "") {
        alert("El campo Precio es obligatorio")
        return false;
    }

    if (fieldOrigen.value.trim() === "") {
        alert("El campo Origen es obligatorio")
        return false;
    }

    if (fieldDestino.value.trim() === "") {
        alert("El campo Destino es obligatorio")
        return false;
    }

    if (fieldFechaSalida.value.trim() === "") {
        alert("El campo Fecha de salida es obligatorio")
        return false;
    }

    if (fieldFechaEntreda.value.trim() === "") {
        alert("El campo Fecha de entrada es obligatorio")
        return false;
    }
    return true;
}


async function createFlight() {
    if (!await verifyFields()) {
        return;
    }

    const newFlight = {
        airline: fieldAerolinea.value.trim(),
        origin: fieldOrigen.value.trim(),
        destination: fieldDestino.value.trim(),
        departure_date: fieldFechaSalida.value,
        arrival_date: fieldFechaEntreda.value,
        price: parseFloat(fieldPrecio.value)
    }
    const resultado = await createVuelo(newFlight)

    if (!resultado.ok) {
        alert("Ocurrió un error al crear el vuelo");
        return;
    }

    alert("Vuelo creado exitosamente");
    loadVuelos();
    clearFields();



}

function clearFields() {
    fieldAerolinea.value = "";
    fieldOrigen.value = "";
    fieldDestino.value = "";
    fieldFechaSalida.value = "";
    fieldFechaEntreda.value = "";
    fieldPrecio.value = "";
    selectedVueloId = null;
    previusPrice = null;
}

let selectedVueloId = null;
let previusPrice = null;
async function showFlightForEdit(e) {
    selectedVueloId = e.target.closest("tr").dataset.vueloId;

    let resultadoVuelo = await getVueloById(selectedVueloId)

    if (!resultadoVuelo.ok) {
        alert("Ocurrió un error al cargar el vuelo");
        return;
    }

    let vuelo = resultadoVuelo.content
    fieldAerolinea.value = vuelo.airline
    fieldOrigen.value = vuelo.origin
    fieldDestino.value = vuelo.destination
    fieldFechaSalida.value = vuelo.departure_date.slice(0, 16)
    fieldFechaEntreda.value = vuelo.arrival_date.slice(0, 16)
    fieldPrecio.value = vuelo.current_price
    previusPrice = vuelo.current_price
}

async function updateFlight() {
    if (!await verifyFields()) {
        return;
    }

    const updatedFlight = {
        airline: fieldAerolinea.value.trim(),
        origin: fieldOrigen.value.trim(),
        destination: fieldDestino.value.trim(),
        departure_date: fieldFechaSalida.value,
        arrival_date: fieldFechaEntreda.value
    }

    if(previusPrice != parseFloat(fieldPrecio.value)){
        let resultadoPriceUpdate = await updateVueloPrice(selectedVueloId,{price:fieldPrecio.value})
        if(!resultadoPriceUpdate.ok){
            alert("Ocurrió un error al actualizar el precio del vuelo");
            return;
        }
    }

    let resultado = await updateVuelo(selectedVueloId, updatedFlight)
    if(resultado.ok){
        alert("Vuelo actualizado exitosamente");
        loadVuelos();
        clearFields();
    } else {
        alert("Ocurrió un error al actualizar el vuelo");
    }


}

async function deleteFlight(e) {
    const vueloId = e.target.closest("tr").dataset.vueloId;
    let resultado = await deleteVuelo(vueloId)

    if(resultado.ok){
        alert("Vuelo eliminado exitosamente");
        loadVuelos();
    } else {
        alert("Ocurrió un error al eliminar el vuelo");
    }
}
