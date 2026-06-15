import { getDepartamentos } from "../api/departamentosApi.js"
import { getMunicipiosByDepartamento } from "../api/municipiosApi.js"
import { getClientes, createCliente, getClienteById, updateCliente } from "../api/clienteApi.js"
export { init }



async function init() {
    let fieldDepartamento = document.getElementById("departamento")
    let fieldMunicipio = document.getElementById("municipio")
    let fieldNombre = document.getElementById("nombre")
    let fieldCedula = document.getElementById("cedula")
    let fieldDireccion = document.getElementById("direccion")
    let fieldTelefono = document.getElementById("telefono")
    let fieldLimpiar = document.getElementById("cliente-reset-button")
    let fieldCreateCustomer = document.getElementById("cliente-save-button")
    let fieldForm = document.getElementById("cliente-form")

    let resultDepartments = await getDepartamentos()
    if (!resultDepartments.ok) {
        alert("Ucurrio un problema al cargar los departamentos")
    }

    loadDepartments(resultDepartments.content);
    loadCustomers()

    fieldLimpiar.addEventListener("click", cleanFields)
    fieldCreateCustomer.addEventListener("click", async (e) => {
        e.preventDefault();
        await createCustomer()
    })

   

    document.getElementById("cliente-edit-button").addEventListener("click", async (e) => {
        e.preventDefault();
        await updateCustomer()
    })


}


function loadDepartments(departments) {
    if (departments == null) return;

    let select = document.getElementById("departamento")
    departments.forEach(department => {
        let option = document.createElement("option")
        option.value = department.id
        option.text = department.name
        select.appendChild(option)
    });

    select.addEventListener("change", async (event) => {
        let departmentId = event.target.value
        loadMunicipalitiesByDepartment(departmentId)
    })




}

async function loadMunicipalitiesByDepartment(departmentId) {

    if (departmentId == "") {
        let fieldMunicipio = document.getElementById("municipio")
        fieldMunicipio.innerHTML = ""
        let option = document.createElement("option")
        option.value = ""
        option.text = "Seleccione un departamento primero"
        fieldMunicipio.appendChild(option)
        return;
    }

    let fieldMunicipio = document.getElementById("municipio")
    fieldMunicipio.innerHTML = ""

    let resultMunicipalities = await getMunicipiosByDepartamento(departmentId)

    if (!resultMunicipalities.ok) {
        alert("Ocurrio un problema al cargar los municipios")
        return;
    }
    let content = resultMunicipalities.content
    content.forEach(municipality => {
        let option = document.createElement("option")
        option.value = municipality.id
        option.text = municipality.name
        fieldMunicipio.appendChild(option)
    })
}

function cleanFields() {
    let fieldDepartamento = document.getElementById("departamento")
    let fieldMunicipio = document.getElementById("municipio")
    let fieldNombre = document.getElementById("nombre")
    let fieldCedula = document.getElementById("cedula")
    let fieldDireccion = document.getElementById("direccion")
    let fieldTelefono = document.getElementById("telefono")

    fieldDepartamento.value = ""
    fieldMunicipio.innerHTML = "<option value=''>Seleccione un municipio</option>"
    fieldNombre.value = ""
    fieldCedula.value = ""
    fieldDireccion.value = ""
    fieldTelefono.value = ""
    let selectedCustomerId = null;

}

async function loadCustomers() {

    let resultadoClientes = await getClientes()

    

    if (!resultadoClientes.ok) {
        alert("Ocurrio un problema al cargar los clientes")
        return;
    }

    let content = resultadoClientes.content
    let tableBody = document.getElementById("clientes-table-body")
    tableBody.innerHTML = ""

    content.forEach(cliente => {
        let row = document.createElement("tr")
        row.dataset.clienteId = cliente.id

        let cellNombre = document.createElement("td")
        cellNombre.textContent = cliente.name
        row.appendChild(cellNombre)

        let cellCedula = document.createElement("td")
        cellCedula.textContent = cliente.national_id
        row.appendChild(cellCedula)

        let cellDireccion = document.createElement("td")
        cellDireccion.textContent = cliente.address
        row.appendChild(cellDireccion)

        let cellTelefono = document.createElement("td")
        cellTelefono.textContent = cliente.phone_number
        row.appendChild(cellTelefono)

        let cellMunicipio = document.createElement("td")
        cellMunicipio.textContent = cliente.municipality_name
        row.appendChild(cellMunicipio)

        let cellAccion = document.createElement("td")
        let editButton = document.createElement("button")
        editButton.textContent = "Editar"
        editButton.classList.add("btn", "btn-primary", "btn-sm")
        editButton.addEventListener("click", showCustomerForEdit)
        cellAccion.appendChild(editButton)
        row.appendChild(cellAccion)

        tableBody.appendChild(row)
    })
    
    
}

let selectedCustomerId = null;
async function showCustomerForEdit(e) {
    let row = e.target.closest("tr")
    selectedCustomerId = row.dataset.clienteId


    let resultadoCliente = await getClienteById(selectedCustomerId)

    if (!resultadoCliente.ok) {
        alert("Ocurrio un problema al cargar el cliente")
        return;
    }

    let cliente = resultadoCliente.content
    document.getElementById("nombre").value = cliente.name
    document.getElementById("cedula").value = cliente.national_id
    document.getElementById("direccion").value = cliente.address
    document.getElementById("telefono").value = cliente.phone_number
    document.getElementById("departamento").value = cliente.department_id
    await loadMunicipalitiesByDepartment(cliente.department_id)
    document.getElementById("municipio").value = cliente.municipality

}


function verifyFieldsForCreation() {
    let fieldDepartamento = document.getElementById("departamento")
    let fieldMunicipio = document.getElementById("municipio")
    let fieldNombre = document.getElementById("nombre")
    let fieldCedula = document.getElementById("cedula")
    let fieldDireccion = document.getElementById("direccion")
    let fieldTelefono = document.getElementById("telefono")


    if (fieldDepartamento.value == "") {
        alert("Seleccione un departamento")
        return false;
    }

    if (fieldMunicipio.value == "") {
        alert("Seleccione un municipio")
        return false;
    }

    if (fieldNombre.value.trim() == "") {
        alert("Ingrese el nombre del cliente")
        return false;
    }

    if (fieldCedula.value.trim() == "") {
        alert("Ingrese la cédula del cliente")
        return false;
    }

    if (fieldDireccion.value.trim() == "") {
        alert("Ingrese la dirección del cliente")
        return false;
    }

    if (fieldTelefono.value.trim() == "") {
        alert("Ingrese el teléfono del cliente")
        return false;
    }

    return true;
}

async function createCustomer() {
    
    if (!verifyFieldsForCreation()) return;
    
    
    
    createCliente({
        municipality: document.getElementById("municipio").value,
        name: document.getElementById("nombre").value,
        national_id: document.getElementById("cedula").value,
        address: document.getElementById("direccion").value,
        phone_number: document.getElementById("telefono").value
    })
    .then(result => {
        
        
        
        if (!result.ok) {
            alert("Ocurrio un problema al crear el cliente")
            return;
        }
        
        cleanFields()
        
        return loadCustomers();
    })
    .then(() => {
        
    })
    .catch(error => {
        
        
    })

}

function updateCustomer() {
    if (!verifyFieldsForCreation()) return;
    updateCliente(selectedCustomerId, {
        municipality: document.getElementById("municipio").value,//no pasamos el departamento porque el backend solo necesita el id del municipio, y este ya tiene asociado el departamento que corresponde 
        name: document.getElementById("nombre").value,
        national_id: document.getElementById("cedula").value,
        address: document.getElementById("direccion").value,
        phone_number: document.getElementById("telefono").value
    }).then(result => {
        if (!result.ok) {
            alert("Ocurrio un problema al actualizar el cliente")
            return;
        }
        alert("Cliente actualizado exitosamente")
        cleanFields()
        loadCustomers()
    })
}
