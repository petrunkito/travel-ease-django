import { getReservas, getReservaById, getReservationStatuses, createReserva, updateReserva, deleteReserva, updateReservaStatus } from '../api/reservaApi.js';
import { getClienteById, getClientes } from '../api/clienteApi.js';
import { getPaqueteById, getPaquetes } from '../api/paqueteApi.js';

export { init }


let fieldEstadoReserva = null;
let fieldTipoPago = null;
let fieldCrearReserva = null;
let previewDivCliente = null;
let previewDivPaquete = null;
let fieldLimpiarCampos = null;
let fieldActualizarReserva = null;

async function init() {
	fieldEstadoReserva = document.getElementById("estado-reserva");
	fieldTipoPago = document.getElementById("tipo-pago");
	fieldCrearReserva = document.getElementById("reserva-add-button");
	previewDivCliente = document.getElementById('cliente-preview-block');
	previewDivPaquete = document.getElementById('paquete-preview-block');
	fieldLimpiarCampos = document.getElementById("reserva-reset-button");
	fieldActualizarReserva = document.getElementById("reserva-update-button");

	await loadData();


	fieldCrearReserva.addEventListener("click", (e) => {
		crearReserva();
	})

	fieldLimpiarCampos.addEventListener("click", (e) => {
		clean();
	})

	fieldActualizarReserva.addEventListener('click', (e) => {
		actualizarReserva();
	})
}


async function loadData() {
	await loadClientes();
	await loadPaquetes();
	await loadEstados();
	await loadReservas();
}

async function loadClientes() {
	const result = await getClientes();

	if (!result.ok) {
		alert("Ocurrio un error al cargar los clientes");
		return;
	}
	const content = result.content;
	let tableBody = document.getElementById("clientes-list-tbody");
	tableBody.innerHTML = "";

	content.forEach(cliente => {
		tableBody.innerHTML += `
		    <tr data-cliente-id="${cliente.id}" onclick="selectCliente(${cliente.id})">
				<td>${cliente.name}</td>
				<td>${cliente.national_id}</td>
				<td>${cliente.address}</td>
			</tr>
		`;

	});
}

async function loadPaquetes() {
	const result = await getPaquetes();

	if (!result.ok) {
		alert("Ocurrio un error al cargar los paquetes");
		return;
	}
	const content = result.content;
	let tableBody = document.getElementById("paquetes-list-tbody");
	tableBody.innerHTML = "";

	content.forEach(paquete => {
		const totalGeneral = Object.values(paquete.services)
			.flat()
			.reduce((sum, item) => sum + item.total, 0);

		tableBody.innerHTML += `
		    <tr data-paquete-id="${paquete.id}" onclick="selectPaquete(${paquete.id})">
				<td>${paquete.name}</td>
				<td>${paquete.description}</td>
				<td>${totalGeneral}</td>
			</tr>
		`;
	});
}

async function loadEstados() {
	const result = await getReservationStatuses();

	if (!result.ok) {
		alert("Ocurrio un error al cargar los estados de reserva");
		return;
	}
	const content = result.content;
	let select = document.getElementById("estado-reserva");
	select.innerHTML = "<option value=''>Seleccione un estado</option>";

	content.forEach(estado => {
		select.innerHTML += `
		    <option value="${estado.id}">${estado.name}</option>
		`;
	});
}

let reservas = null
async function loadReservas() {
	const result = await getReservas();

	if (!result.ok) {
		alert("Ocurrio un error al cargar las reservas");
		return;
	}
	const content = result.content;
	reservas = content;
	let tableBody = document.getElementById("reservas-table-body");
	tableBody.innerHTML = "";

	content.forEach(reserva => {
		tableBody.innerHTML += `
		    <tr data-reserva-id="${reserva.id}" >
				<td>${reserva.client_name}</td>
				<td>${reserva.package_name}</td>
				<td>${reserva.total}</td>
				<td>${reserva.current_status.name}</td>
				<td>
					<button class="row_action btn btn-primary btn-sm" onclick="selectReserva(${reserva.id})">Editar</button>
				</td>
			</tr>
		`;

	});
}


let cliente = null;
window.selectCliente = selectCliente;
function selectCliente(clienteId) {
	if (!clienteId) {
		previewDiv.innerHTML = '<p class="preview-empty">Selecciona un cliente</p>';
		return;
	}

	const fila = document.querySelector(`tr[data-cliente-id="${clienteId}"]`);
	if (!fila) {
		alert("No se encontró el cliente seleccionado");
		return;
	}

	const celdas = fila.querySelectorAll('td');

	cliente = {
		id: clienteId,
		name: celdas[0].textContent.trim(),
		national_id: celdas[1].textContent.trim(),
		address: celdas[2].textContent.trim()
	};

	showCliente(cliente)
}

function showCliente(cliente) {
	const previewDiv = document.getElementById('cliente-preview-block');


	previewDiv.innerHTML = `
		<div class="preview-info">
			<div class="preview-info-item">
				<span class="preview-info-label">Nombre:</span>
				<span class="preview-info-value">${cliente.name || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">DNI/Cédula:</span>
				<span class="preview-info-value">${cliente.national_id || 'N/A'}</span>
			</div>
			<div class="preview-info-item" style="border-bottom: none;">
				<span class="preview-info-label">Municipio:</span>
				<span class="preview-info-value">${cliente.address || 'N/A'}</span>
			</div>
		</div>
	`;
}

let paquete = null;
window.selectPaquete = selectPaquete;
function selectPaquete(paqueteId) {

	if (!paqueteId) {
		previewDiv.innerHTML = '<p class="preview-empty">Selecciona un paquete</p>';
		return;
	}


	const fila = document.querySelector(`tr[data-paquete-id="${paqueteId}"]`);
	if (!fila) {
		alert("No se encontró el paquete seleccionado");
		return;
	}

	const celdas = fila.querySelectorAll('td');

	paquete = {
		id: paqueteId,
		titulo: celdas[0].textContent.trim(),
		descripcion: celdas[1].textContent.trim(),
		precio: celdas[2].textContent.trim()
	};


	showPaquete(paquete)

}

function showPaquete(paquete) {
	const previewDiv = document.getElementById('paquete-preview-block');



	previewDiv.innerHTML = `
		<div class="preview-info">
			<div class="preview-info-item">
				<span class="preview-info-label">Título:</span>
				<span class="preview-info-value">${paquete.titulo || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">Descripción:</span>
				<span class="preview-info-value">${paquete.descripcion || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">Precio:</span>
				<span class="preview-info-value">${paquete.precio || 'N/A'}</span>
			</div>
		</div>
	`;
}


let reservaId = null;
let reserva = null;
window.selectReserva = selectReserva;
async function selectReserva(reservaId) {
	const resultReserva = await getReservaById(reservaId);
	if (!resultReserva.ok) {
		alert("Oucrrio un error al seleccionar la reserva")
		return;
	}

	reserva = resultReserva.content;

	const resultCliente = await getClienteById(reserva.client)
	if (!resultCliente.ok) {
		alert("Ocurrio un error al encontrar el cliente de esta reserva")
		return;
	}

	let clienteContent = resultCliente.content;

	cliente = {
		id: clienteContent.id,
		name: clienteContent.name,
		national_id: clienteContent.national_id,
		address: clienteContent.address
	};


	const resultPaquete = await getPaqueteById(reserva.package_reserved_id)
	if (!resultPaquete.ok) {
		alert("Ocurrrió un error al encontrar el paquete de esta reserva.")
		return;
	}

	let paqueteContent = resultPaquete.content;

	paquete = {
		id: paqueteContent.id,
		titulo: paqueteContent.name,
		descripcion: paqueteContent.description,
		precio: Object.values(paqueteContent.services).flat().reduce((sum, item) => sum + item.total, 0)
	};

	fieldTipoPago.value = reserva.payment_type;
	fieldEstadoReserva.value = reserva.current_status.id
	showCliente(cliente)
	showPaquete(paquete)

}

async function actualizarReserva() {
	if (!validarCampos()) return;

	if (reserva == null) {
		alert("No has seleccionado ninguna reserva para actualizar")
		return;
	};

	const update = {
		client: cliente.id,
		payment_type: fieldTipoPago.value,
		seller_user: 1,
		// active: true es opcional este campo
		package_id: paquete.id
	}

	if (reserva.current_status.id != fieldEstadoReserva.value) {
		let resultadoActualizacionEstado = await updateReservaStatus(
			reserva.id,
			{ status_id: fieldEstadoReserva.value }
		)

		if(!resultadoActualizacionEstado.ok)
		{
			alert("Ocurrió un error al actualizar el estado de la reservacion. detalle: "+resultadoActualizacionEstado.content.error);
			return;
		}
	}



	// FALTA ACTUALIZAR EL ESTADO DE LA reserva
	// ESTE SE HACE CON UN ENDPOINT DIFERENTE
	// hiasdsdjkldafjkljlkdfAKLSDFa
	// dfASJKSDFK

	const resultUpdateReserva = await updateReserva(reserva.id, update);
	if (!resultUpdateReserva.ok) {
		alert("Ocurrió un error al actualizar la reserva.")
		return;
	}

	alert("Reserva actualizada exitosamente")
	await clean()
	await loadData();


}

function validarCampos() {

	if (cliente == null) {
		alert("Selecciona a un cliente para realizar la reserva")
		return false;
	}

	if (paquete == null) {
		alert("Selecciona un paquete para realizar la reserva")
		return false;
	}

	if (fieldEstadoReserva.value === "") {
		alert("Necesitas especificar el estado de la reserva.")
		return false;
	}

	if (fieldTipoPago.value === "") {
		alert("Selecciona el tipo de pago")
		return false;
	}

	return true;
}


async function crearReserva() {
	if (!validarCampos()) return;

	const newReserva = {
		client_id: cliente.id,
		package_id: paquete.id,
		payment_type_id: fieldTipoPago.value,
		seller_user_id: 1,
		status_id: fieldEstadoReserva.value
	}

	const result = await createReserva(newReserva)
	if (!result.ok) {
		alert("Ocurrió un error al crear la reserva")
		return;
	}

	alert("Reserva creada exitosamente.")
	await clean();
	await loadData()
}

async function clean() {
	cliente = null;
	paquete = null;
	previewDivCliente.innerHTML = "";
	previewDivPaquete.innerHTML = "";
	fieldEstadoReserva.value = ""
	fieldTipoPago.value = ""

}
