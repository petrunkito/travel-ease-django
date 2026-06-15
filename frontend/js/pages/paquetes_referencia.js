//este documento nos servira como referencia para la creacion de paquetes,
//ya que iremos modificando la logica del javascript


import { getVuelos } from '../api/vueloApi.js';
import { getHoteles } from '../api/hotelApi.js';
import { getTransportes } from '../api/transporteApi.js';

let paqueteActual = null;
let serviciosPaquete = [];

export function init() {
	initializePackages();
}

function initializePackages() {
	setupFormHandlers();
	loadAvailableServices();
	loadPackages();
}

function setupFormHandlers() {
	const form = document.getElementById('paquete-form');
	const saveBtn = document.getElementById('paquete-save-button');
	const resetBtn = document.getElementById('paquete-reset-button');
	const editBtn = document.getElementById('paquete-edit-button');
	const refreshBtn = document.getElementById('paquetes-refresh-button');

	if (saveBtn) {
		saveBtn.addEventListener('click', () => handleSavePackage());
	}

	if (resetBtn) {
		resetBtn.addEventListener('click', () => handleResetForm());
	}

	if (editBtn) {
		editBtn.addEventListener('click', () => handleEditPackage());
	}

	if (refreshBtn) {
		refreshBtn.addEventListener('click', () => loadPackages());
	}
}

function handleSavePackage() {
	const form = document.getElementById('paquete-form');
	
	if (!validateForm(form)) {
		return;
	}

	if (serviciosPaquete.length === 0) {
		showFormFeedback('error', 'Debe agregar al menos un servicio al paquete');
		return;
	}

	const formData = new FormData(form);
	const paqueteData = {
		titulo: formData.get('title'),
		descripcion: formData.get('description'),
		pais: formData.get('country'),
		ciudad: formData.get('city'),
		servicios: serviciosPaquete,
		total: calculateTotal()
	};

	console.log('Guardando paquete:', paqueteData);
	showFormFeedback('success', 'Paquete creado exitosamente');
	
	// Aquí iría la llamada al API
	setTimeout(() => {
		handleResetForm();
		loadPackages();
	}, 1500);
}

function handleEditPackage() {
	if (!paqueteActual) {
		showFormFeedback('error', 'Seleccione un paquete para editar');
		return;
	}

	const form = document.getElementById('paquete-form');
	
	if (!validateForm(form)) {
		return;
	}

	if (serviciosPaquete.length === 0) {
		showFormFeedback('error', 'Debe agregar al menos un servicio al paquete');
		return;
	}

	const formData = new FormData(form);
	const paqueteData = {
		id: paqueteActual.id,
		titulo: formData.get('title'),
		descripcion: formData.get('description'),
		pais: formData.get('country'),
		ciudad: formData.get('city'),
		servicios: serviciosPaquete,
		total: calculateTotal()
	};

	console.log('Actualizando paquete:', paqueteData);
	showFormFeedback('success', 'Paquete actualizado exitosamente');
	
	setTimeout(() => {
		handleResetForm();
		loadPackages();
	}, 1500);
}

function handleResetForm() {
	document.getElementById('paquete-form').reset();
	document.getElementById('paquete-id').value = '';
	paqueteActual = null;
	serviciosPaquete = [];
	updatePackageDetails();
	showFormFeedback('', '');
}

function validateForm(form) {
	const titulo = form.querySelector('#titulo').value.trim();
	const descripcion = form.querySelector('#descripcion').value.trim();
	const pais = form.querySelector('#pais').value.trim();
	const ciudad = form.querySelector('#ciudad').value.trim();

	if (!titulo) {
		showFormFeedback('error', 'El título es requerido');
		return false;
	}

	if (!descripcion) {
		showFormFeedback('error', 'La descripción es requerida');
		return false;
	}

	if (!pais) {
		showFormFeedback('error', 'El país es requerido');
		return false;
	}

	if (!ciudad) {
		showFormFeedback('error', 'La ciudad es requerida');
		return false;
	}

	return true;
}

function showFormFeedback(type, message) {
	const feedback = document.getElementById('paquete-form-feedback');
	feedback.textContent = message;
	feedback.className = 'form-feedback';
	
	if (type === 'success') {
		feedback.classList.add('success');
	} else if (type === 'error') {
		feedback.classList.add('error');
	}
}

async function loadAvailableServices() {
	try {
		const [vuelos, hoteles, transportes] = await Promise.all([
			getVuelos(),
			getHoteles(),
			getTransportes()
		]);

		if (vuelos.ok) {
			loadVuelosTable(vuelos.content);
		}

		if (hoteles.ok) {
			loadHotelesTable(hoteles.content);
		}

		if (transportes.ok) {
			loadTransportesTable(transportes.content);
		}
	} catch (error) {
		console.error('Error loading services:', error);
	}
}

function loadVuelosTable(vuelos) {
	const tbody = document.getElementById('vuelos-tbody');
	
	if (!vuelos || vuelos.length === 0) {
		tbody.innerHTML = '<tr class="empty-state-row"><td colspan="5" class="empty-state">No hay vuelos disponibles</td></tr>';
		return;
	}

	tbody.innerHTML = vuelos.map(vuelo => `
		<tr>
			<td>${vuelo.airline || 'N/A'}</td>
			<td>${vuelo.destination || 'N/A'}</td>
			<td>$${parseFloat(vuelo.price || 0).toFixed(2)}</td>
			<td>
				<input type="number" class="quantity-input" value="1" min="1" data-vuelo-id="${vuelo.id}">
			</td>
			<td>
				<button type="button" class="row-action" onclick="addServiceToPackage('vuelo', ${vuelo.id})">Agregar</button>
			</td>
		</tr>
	`).join('');
}

function loadHotelesTable(hoteles) {
	const tbody = document.getElementById('hoteles-tbody');
	
	if (!hoteles || hoteles.length === 0) {
		tbody.innerHTML = '<tr class="empty-state-row"><td colspan="5" class="empty-state">No hay hoteles disponibles</td></tr>';
		return;
	}

	tbody.innerHTML = hoteles.map(hotel => `
		<tr>
			<td>${hotel.name || 'N/A'}</td>
			<td>${hotel.city || 'N/A'}</td>
			<td>$${parseFloat(hotel.price || 0).toFixed(2)}</td>
			<td>
				<input type="number" class="quantity-input" value="1" min="1" data-hotel-id="${hotel.id}">
			</td>
			<td>
				<button type="button" class="row-action" onclick="addServiceToPackage('hotel', ${hotel.id})">Agregar</button>
			</td>
		</tr>
	`).join('');
}

function loadTransportesTable(transportes) {
	const tbody = document.getElementById('transportes-tbody');
	
	if (!transportes || transportes.length === 0) {
		tbody.innerHTML = '<tr class="empty-state-row"><td colspan="5" class="empty-state">No hay transportes disponibles</td></tr>';
		return;
	}

	tbody.innerHTML = transportes.map(transporte => `
		<tr>
			<td>${transporte.name || 'N/A'}</td>
			<td>${transporte.destination || 'N/A'}</td>
			<td>$${parseFloat(transporte.price || 0).toFixed(2)}</td>
			<td>
				<input type="number" class="quantity-input" value="1" min="1" data-transport-id="${transporte.id}">
			</td>
			<td>
				<button type="button" class="row-action" onclick="addServiceToPackage('transporte', ${transporte.id})">Agregar</button>
			</td>
		</tr>
	`).join('');
}

window.addServiceToPackage = function(tipo, id) {
	let attributeName = 'vuelo-id';
	if (tipo === 'hotel') attributeName = 'hotel-id';
	if (tipo === 'transporte') attributeName = 'transport-id';
	
	const quantityInput = document.querySelector(`input[data-${attributeName}="${id}"]`);
	const cantidad = parseInt(quantityInput?.value || 1);

	// Obtener datos del servicio según el tipo
	let servicio = null;

	if (tipo === 'vuelo') {
		const row = quantityInput.closest('tr');
		servicio = {
			tipo,
			id,
			nombre: row.cells[0].textContent,
			precio: parseFloat(row.cells[2].textContent.replace('$', '')),
			cantidad,
			ciudad: row.cells[1].textContent
		};
	} else if (tipo === 'hotel') {
		const row = quantityInput.closest('tr');
		servicio = {
			tipo,
			id,
			nombre: row.cells[0].textContent,
			precio: parseFloat(row.cells[2].textContent.replace('$', '')),
			cantidad,
			ciudad: row.cells[1].textContent
		};
	} else if (tipo === 'transporte') {
		const row = quantityInput.closest('tr');
		servicio = {
			tipo,
			id,
			nombre: row.cells[0].textContent,
			precio: parseFloat(row.cells[2].textContent.replace('$', '')),
			cantidad,
			destino: row.cells[1].textContent
		};
	}

	// Verificar si el servicio ya existe
	const exists = serviciosPaquete.find(s => s.tipo === tipo && s.id === id);
	if (exists) {
		showFormFeedback('error', 'Este servicio ya ha sido agregado');
		return;
	}

	serviciosPaquete.push(servicio);
	updatePackageDetails();
	showFormFeedback('success', `${tipo.charAt(0).toUpperCase() + tipo.slice(1)} agregado al paquete`);
};

function updatePackageDetails() {
	const tbody = document.getElementById('paquete-services-tbody');
	
	if (serviciosPaquete.length === 0) {
		tbody.innerHTML = '<tr class="empty-state-row"><td colspan="6" class="empty-state">Selecciona servicios para agregarlos al paquete</td></tr>';
		document.getElementById('paquete-total').textContent = '0';
		return;
	}

	tbody.innerHTML = serviciosPaquete.map((servicio, index) => {
		const total = servicio.precio * servicio.cantidad;
		const tipoLabel = servicio.tipo.charAt(0).toUpperCase() + servicio.tipo.slice(1);
		
		return `
			<tr>
				<td>${servicio.nombre}</td>
				<td>$${servicio.precio.toFixed(2)}</td>
				<td>${servicio.cantidad}</td>
				<td>$${total.toFixed(2)}</td>
				<td>${tipoLabel}</td>
				<td>
					<button type="button" class="row-action danger-small" onclick="removeServiceFromPackage(${index})">Quitar</button>
				</td>
			</tr>
		`;
	}).join('');

	document.getElementById('paquete-total').textContent = calculateTotal().toFixed(2);
}

window.removeServiceFromPackage = function(index) {
	serviciosPaquete.splice(index, 1);
	updatePackageDetails();
};

function calculateTotal() {
	return serviciosPaquete.reduce((total, servicio) => {
		return total + (servicio.precio * servicio.cantidad);
	}, 0);
}

function loadPackages() {
	// Simulación de carga de paquetes
	const tbody = document.getElementById('paquetes-table-body');
	
	// Aquí iría la llamada al API
	const mockPaquetes = [
		{
			id: 1,
			titulo: 'Tour Madrid Clásico',
			descripcion: 'Viaje a Madrid con vuelo, hotel y transporte',
			pais: 'España',
			ciudad: 'Madrid',
			total: 3500.00
		}
	];

	if (mockPaquetes.length === 0) {
		tbody.innerHTML = '<tr class="empty-state-row"><td colspan="6" class="empty-state">No hay paquetes registrados</td></tr>';
		return;
	}

	tbody.innerHTML = mockPaquetes.map(paquete => `
		<tr>
			<td>${paquete.titulo}</td>
			<td>${paquete.descripcion}</td>
			<td>${paquete.pais}</td>
			<td>${paquete.ciudad}</td>
			<td>$${paquete.total.toFixed(2)}</td>
			<td>
				<button type="button" class="row-action" onclick="selectPackage(${paquete.id})">Editar</button>
				<button type="button" class="row-action danger-small" onclick="deletePackage(${paquete.id})">Eliminar</button>
			</td>
		</tr>
	`).join('');
}

window.selectPackage = function(id) {
	// Simulación de selección de paquete
	console.log('Seleccionar paquete:', id);
};

window.deletePackage = function(id) {
	if (confirm('¿Está seguro de que desea eliminar este paquete?')) {
		console.log('Eliminar paquete:', id);
		loadPackages();
	}
};