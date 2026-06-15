import { getReservas, createReserva, updateReserva, deleteReserva } from '../api/reservaApi.js';
import { getClientes, getClienteById } from '../api/clienteApi.js';
import { getPaquetes, getPaqueteById } from '../api/paqueteApi.js';

let reservaActual = null;
let clientesData = [];
let paquetesData = [];

export function init() {
	initializeReservations();
}

function initializeReservations() {
	setupFormHandlers();
	loadClientes();
	loadPaquetes();
	loadReservations();
}

function setupFormHandlers() {
	const clienteSelect = document.getElementById('cliente-select');
	const paqueteSelect = document.getElementById('paquete-select');
	const saveBtn = document.getElementById('reserva-save-button');
	const cancelBtn = document.getElementById('reserva-cancel-button');
	const editBtn = document.getElementById('reserva-edit-button');
	const refreshBtn = document.getElementById('reservas-refresh-button');

	if (clienteSelect) {
		clienteSelect.addEventListener('change', () => updatePreview());
	}

	if (paqueteSelect) {
		paqueteSelect.addEventListener('change', () => updatePreview());
	}

	if (saveBtn) {
		saveBtn.addEventListener('click', () => handleSaveReservation());
	}

	if (cancelBtn) {
		cancelBtn.addEventListener('click', () => handleResetForm());
	}

	if (editBtn) {
		editBtn.addEventListener('click', () => handleEditReservation());
	}

	if (refreshBtn) {
		refreshBtn.addEventListener('click', () => loadReservations());
	}
}

async function loadClientes() {
	try {
		const result = await getClientes();
		
		if (result.ok && result.content) {
			clientesData = result.content;
			populateClienteSelect(result.content);
		}
	} catch (error) {
		console.error('Error loading clientes:', error);
	}
}

function populateClienteSelect(clientes) {
	const select = document.getElementById('cliente-select');
	
	if (!clientes || clientes.length === 0) {
		select.innerHTML = '<option value="">No hay clientes disponibles</option>';
		return;
	}

	select.innerHTML = '<option value="">Seleccione un cliente</option>' + 
		clientes.map(cliente => `
			<option value="${cliente.id}">${cliente.name || 'Sin nombre'} - ${cliente.dni || 'Sin DNI'}</option>
		`).join('');
}

async function loadPaquetes() {
	try {
		const result = await getPaquetes();
		
		if (result.ok && result.content) {
			paquetesData = result.content;
			populatePaqueteSelect(result.content);
		}
	} catch (error) {
		console.error('Error loading paquetes:', error);
	}
}

function populatePaqueteSelect(paquetes) {
	const select = document.getElementById('paquete-select');
	
	if (!paquetes || paquetes.length === 0) {
		select.innerHTML = '<option value="">No hay paquetes disponibles</option>';
		return;
	}

	select.innerHTML = '<option value="">Seleccione un paquete</option>' + 
		paquetes.map(paquete => `
			<option value="${paquete.id}">${paquete.title || 'Sin título'} - $${parseFloat(paquete.total || 0).toFixed(2)}</option>
		`).join('');
}

function updatePreview() {
	const clienteId = document.getElementById('cliente-select').value;
	const paqueteId = document.getElementById('paquete-select').value;

	updateClientePreview(clienteId);
	updatePaquetePreview(paqueteId);
	updateTotalPreview(paqueteId);
}

function updateClientePreview(clienteId) {
	const previewDiv = document.getElementById('cliente-preview');

	if (!clienteId) {
		previewDiv.innerHTML = '<p class="preview-empty">Selecciona un cliente</p>';
		return;
	}

	const cliente = clientesData.find(c => c.id == clienteId);

	if (!cliente) {
		previewDiv.innerHTML = '<p class="preview-empty">Cliente no encontrado</p>';
		return;
	}

	previewDiv.innerHTML = `
		<div class="preview-info">
			<div class="preview-info-item">
				<span class="preview-info-label">Nombre:</span>
				<span class="preview-info-value">${cliente.name || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">DNI/Cédula:</span>
				<span class="preview-info-value">${cliente.dni || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">Teléfono:</span>
				<span class="preview-info-value">${cliente.phone || 'N/A'}</span>
			</div>
			<div class="preview-info-item" style="border-bottom: none;">
				<span class="preview-info-label">Municipio:</span>
				<span class="preview-info-value">${cliente.municipality || 'N/A'}</span>
			</div>
		</div>
	`;
}

function updatePaquetePreview(paqueteId) {
	const previewDiv = document.getElementById('paquete-preview');

	if (!paqueteId) {
		previewDiv.innerHTML = '<p class="preview-empty">Selecciona un paquete</p>';
		return;
	}

	const paquete = paquetesData.find(p => p.id == paqueteId);

	if (!paquete) {
		previewDiv.innerHTML = '<p class="preview-empty">Paquete no encontrado</p>';
		return;
	}

	previewDiv.innerHTML = `
		<div class="preview-info">
			<div class="preview-info-item">
				<span class="preview-info-label">Título:</span>
				<span class="preview-info-value">${paquete.title || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">País:</span>
				<span class="preview-info-value">${paquete.country || 'N/A'}</span>
			</div>
			<div class="preview-info-item">
				<span class="preview-info-label">Ciudad:</span>
				<span class="preview-info-value">${paquete.city || 'N/A'}</span>
			</div>
			<div class="preview-info-item" style="border-bottom: none;">
				<span class="preview-info-label">Descripción:</span>
				<span class="preview-info-value">${(paquete.description || 'N/A').substring(0, 30)}...</span>
			</div>
		</div>
	`;
}

function updateTotalPreview(paqueteId) {
	const totalSpan = document.getElementById('reserva-total-amount');

	if (!paqueteId) {
		totalSpan.textContent = '$0.00';
		return;
	}

	const paquete = paquetesData.find(p => p.id == paqueteId);

	if (!paquete) {
		totalSpan.textContent = '$0.00';
		return;
	}

	const total = parseFloat(paquete.total || 0);
	totalSpan.textContent = `$${total.toFixed(2)}`;
}

function handleSaveReservation() {
	const form = document.getElementById('reserva-form');
	const clienteId = document.getElementById('cliente-select').value;
	const paqueteId = document.getElementById('paquete-select').value;
	const estado = document.getElementById('estado-reserva').value;

	if (!validateForm(clienteId, paqueteId)) {
		return;
	}

	const reservaData = {
		cliente: parseInt(clienteId),
		paquete: parseInt(paqueteId),
		status: estado
	};

	console.log('Guardando reserva:', reservaData);
	showFormFeedback('success', 'Reserva creada exitosamente');

	setTimeout(() => {
		handleResetForm();
		loadReservations();
	}, 1500);
}

function handleEditReservation() {
	if (!reservaActual) {
		showFormFeedback('error', 'Seleccione una reserva para editar');
		return;
	}

	const clienteId = document.getElementById('cliente-select').value;
	const paqueteId = document.getElementById('paquete-select').value;
	const estado = document.getElementById('estado-reserva').value;

	if (!validateForm(clienteId, paqueteId)) {
		return;
	}

	const reservaData = {
		cliente: parseInt(clienteId),
		paquete: parseInt(paqueteId),
		status: estado
	};

	console.log('Actualizando reserva:', reservaActual.id, reservaData);
	showFormFeedback('success', 'Reserva actualizada exitosamente');

	setTimeout(() => {
		handleResetForm();
		loadReservations();
	}, 1500);
}

function handleResetForm() {
	document.getElementById('reserva-form').reset();
	document.getElementById('reserva-id').value = '';
	document.getElementById('estado-reserva').value = 'pendiente';
	reservaActual = null;
	updatePreview();
	showFormFeedback('', '');
}

function validateForm(clienteId, paqueteId) {
	if (!clienteId) {
		showFormFeedback('error', 'Debe seleccionar un cliente');
		return false;
	}

	if (!paqueteId) {
		showFormFeedback('error', 'Debe seleccionar un paquete');
		return false;
	}

	return true;
}

function showFormFeedback(type, message) {
	const feedback = document.getElementById('reserva-form-feedback');
	feedback.textContent = message;
	feedback.className = 'form-feedback';
	
	if (type === 'success') {
		feedback.classList.add('success');
	} else if (type === 'error') {
		feedback.classList.add('error');
	}
}

async function loadReservations() {
	try {
		const result = await getReservas();
		
		if (result.ok && result.content) {
			populateReservationsTable(result.content);
		}
	} catch (error) {
		console.error('Error loading reservations:', error);
	}
}

function populateReservationsTable(reservas) {
	const tbody = document.getElementById('reservas-table-body');

	if (!reservas || reservas.length === 0) {
		tbody.innerHTML = '<tr class="empty-state-row"><td colspan="6" class="empty-state">No hay reservas registradas</td></tr>';
		return;
	}

	tbody.innerHTML = reservas.map(reserva => {
		const cliente = clientesData.find(c => c.id == reserva.cliente);
		const paquete = paquetesData.find(p => p.id == reserva.paquete);
		const fechaFormato = new Date(reserva.created_at || new Date()).toLocaleDateString('es-ES');

		return `
			<tr>
				<td>${cliente?.name || 'N/A'}</td>
				<td>${paquete?.title || 'N/A'}</td>
				<td>
					<span class="status-badge ${reserva.status || 'pendiente'}">
						${(reserva.status || 'Pendiente').charAt(0).toUpperCase() + (reserva.status || 'Pendiente').slice(1)}
					</span>
				</td>
				<td>$${parseFloat(paquete?.total || 0).toFixed(2)}</td>
				<td>${fechaFormato}</td>
				<td>
					<button type="button" class="row-action" onclick="selectReservation(${reserva.id})">Editar</button>
					<button type="button" class="row-action danger-small" onclick="deleteReservation(${reserva.id})">Eliminar</button>
				</td>
			</tr>
		`;
	}).join('');
}

window.selectReservation = function(id) {
	console.log('Seleccionar reserva:', id);
	// Aquí iría la lógica para cargar los datos de la reserva en el formulario
};

window.deleteReservation = function(id) {
	if (confirm('¿Está seguro de que desea eliminar esta reserva?')) {
		console.log('Eliminar reserva:', id);
		loadReservations();
	}
};