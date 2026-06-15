import { createTransporte, deleteTransporte, getTransporteById, updateTransporte, getTransportes, createTransportePrice } from "../../api/transporteApi.js"
import { getTipoTransportes, getTipoTransporteById } from "../../api/tipoTransporteApi.js"


export { init }


let selectTipoTransporte = null
let buttonAgregar = null
let fieldOrigen = null;
let fieldDestino = null;
let fieldPrecio = null;
let fieldActualizar = null;
let buttonReset = null;

async function init() {
    selectTipoTransporte = document.getElementById("transporte-tipo");
    buttonAgregar = document.getElementById("transporte-save-button");
    fieldOrigen = document.getElementById("transporte-origen");
    fieldDestino = document.getElementById("transporte-destino");
    fieldPrecio = document.getElementById("transporte-precio");
    fieldActualizar = document.getElementById("transporte-edit-button");
    buttonReset = document.getElementById("transporte-reset-button");

    loadTipoTransportes();
    loadServiceTransports();

    buttonAgregar.addEventListener("click", async (e) => {
        e.preventDefault();
        await createNewTransporte();
    })

    fieldActualizar.addEventListener("click", async (e) => {
        e.preventDefault();
        await updateSelectedTransporte();
    })

    buttonReset.addEventListener("click", (e) => {
        e.preventDefault();
        clearTransporteForm();
    })

}

async function loadTipoTransportes() {
    const result = await getTipoTransportes();

    if (!result.ok) {
        alert("Ocurrió un error al cargar los tipos de transporte");
        return;
    }

    const tipoTransportes = result.content;

    tipoTransportes.forEach(tipoTransporte => {
        const option = document.createElement("option");
        option.value = tipoTransporte.id;
        option.textContent = tipoTransporte.name;
        selectTipoTransporte.appendChild(option);
    });
}

async function loadServiceTransports() {
    const result = await getTransportes();

    if (!result.ok) {
        alert("Ocurrió un error al cargar los transportes");
        return;
    }

    const transportes = result.content;
    const tableBody = document.getElementById("transporte-table-body");
    tableBody.innerHTML = "";

    transportes.forEach(transporte => {
        const row = document.createElement("tr");
        row.dataset.transporteId = transporte.id

        const cellTipoTransporte = document.createElement("td");
        cellTipoTransporte.textContent = transporte.type_transport_name;
        row.appendChild(cellTipoTransporte);

        const cellOrigen = document.createElement("td");
        cellOrigen.textContent = transporte.origin;
        row.appendChild(cellOrigen);

        const cellDestino = document.createElement("td");
        cellDestino.textContent = transporte.destination;
        row.appendChild(cellDestino);

        const cellPrecio = document.createElement("td");
        cellPrecio.textContent = transporte.current_price.toFixed(2);
        row.appendChild(cellPrecio);

        const cellEdit = document.createElement("td");
        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.classList.add("btn", "btn-primary", "btn-sm");
        editButton.textContent = "Editar";
        editButton.addEventListener("click", () => {
            showTransporteForEdit(transporte.id);
        });
        cellEdit.appendChild(editButton);
        row.appendChild(cellEdit);

        const cellDelete = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("btn", "btn-primary", "btn-sm");
        deleteButton.textContent = "Eliminar";
        deleteButton.addEventListener("click", () => {
            deleteSelectedTransporte(transporte.id);
        });
        cellDelete.appendChild(deleteButton);
        row.appendChild(cellDelete);

        tableBody.appendChild(row);

    })

}
let selectedTransporteId = null;
let previousPrice = null;
async function showTransporteForEdit(transporteId) {
   selectedTransporteId = transporteId;
   
    const result = await getTransporteById(transporteId);
    if (!result.ok) {
        alert("Ocurrió un error al cargar el transporte");
        return;
    }
    
    const transporte = result.content;
    selectTipoTransporte.value = transporte.type_transport;
    fieldOrigen.value = transporte.origin;
    fieldDestino.value = transporte.destination;
    fieldPrecio.value = transporte.current_price.toFixed(2);
    previousPrice = transporte.current_price;
}

async function updateSelectedTransporte() {
    if(selectedTransporteId === null) {
        alert("No se ha seleccionado ningún transporte para actualizar");
        return;
    }
    if (!veryfyTransporteForm()) return;

    const updatedTransporte = {
        type_transport: selectTipoTransporte.value,
        origin: fieldOrigen.value.trim(),
        destination: fieldDestino.value.trim()
    };

    if(previousPrice !== parseFloat(fieldPrecio.value)) {
        let resultadoPriceUpdate = await createTransportePrice(selectTipoTransporte,{price: parseFloat(fieldPrecio.value)});
        if (!resultadoPriceUpdate.ok) {
            alert("Ocurrió un error al actualizar el precio del transporte");
            return;
        }
    }

    const result = await updateTransporte(selectedTransporteId, updatedTransporte);

    if (!result.ok) {
        alert("Ocurrió un error al actualizar el transporte");
        return;
    }

    alert("Transporte actualizado exitosamente");
    loadServiceTransports();
    clearTransporteForm();
}

async function deleteSelectedTransporte(transporteId) {
    if (!confirm("¿Está seguro de que desea eliminar este transporte?")) {
        return;
    }
    
    const result = await deleteTransporte(transporteId);
    if (!result.ok) {
        alert("Ocurrió un error al eliminar el transporte");
        return; 
    }

    alert("Transporte eliminado exitosamente");
    loadServiceTransports();

}

function veryfyTransporteForm() {
    if (selectTipoTransporte.value === "") {
        alert("El campo tipo de transporte es obligatorio");
        return false;
    }

    if (fieldOrigen.value.trim() === "") {
        alert("El campo origen es obligatorio");
        return false;
    }

    if (fieldDestino.value.trim() === "") {
        alert("El campo destino es obligatorio");
        return false;
    }

    if (fieldPrecio.value.trim() === "" || isNaN(fieldPrecio.value) || Number(fieldPrecio.value) < 0) {
        alert("El campo precio es obligatorio y debe ser un número mayor o igual a 0");
        return false;
    }

    return true;
}

function clearTransporteForm() {
    selectTipoTransporte.value = "";
    fieldOrigen.value = "";
    fieldDestino.value = "";
    fieldPrecio.value = "";
    selectedTransporteId = null;
    previousPrice = null;
}

async function createNewTransporte() {
    if (!veryfyTransporteForm()) return;

    const newTransporte = {
        type_transport: selectTipoTransporte.value,
        origin: fieldOrigen.value.trim(),
        destination: fieldDestino.value.trim(),
        price: parseFloat(fieldPrecio.value)
    };

    const result = await createTransporte(newTransporte);

    if (!result.ok) {
        alert("Ocurrió un error al crear el transporte");
        return;
    }

    alert("Transporte creado exitosamente");
    loadServiceTransports();
    clearTransporteForm();


}