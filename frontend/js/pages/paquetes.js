
import { getVuelos } from "../api/vueloApi.js"
import { getHoteles } from "../api/hotelApi.js"
import { getTransportes } from "../api/transporteApi.js"
import { createPaquete, deletePaquete, getPaqueteById, getPaquetes, updatePaquete } from "../api/paqueteApi.js"

export { init }


let fieldPaqueteTitle = null
let fieldPaqueteDescription = null
let fieldPaqueteCountry = null
let fieldPaqueteCity = null
let fieldButtonSave = null
let fieldButtonClear = null
let fieldButtonEdit = null
let fieldTotalPrice = null;
async function init() {
	fieldPaqueteTitle = document.getElementById('titulo');
	fieldPaqueteDescription = document.getElementById('descripcion');
	fieldPaqueteCountry = document.getElementById('pais');
	fieldPaqueteCity = document.getElementById('ciudad');
	fieldButtonSave = document.getElementById('paquete-save-button');
	fieldButtonClear = document.getElementById('paquete-reset-button');
	fieldButtonEdit = document.getElementById('paquete-edit-button');
	fieldTotalPrice = document.getElementById('paquete-total');
	await loadServices();


	fieldButtonClear.addEventListener("click", clean);
	fieldButtonSave.addEventListener("click", createPackage);
	fieldButtonEdit.addEventListener("click", async (e) => {
		e.preventDefault();
		updatePackage();
	})
}

async function loadServices() {
	await loadVuelos();
	await loadHoteles();
	await loadTransportes();
	await loadPaquetes();
}

async function loadVuelos() {
	const result = await getVuelos();

	if (!result.ok) {
		alert("Ocurrió un error al cargar los vuelos");
		return;
	}

	const vuelos = result.content;
	const tableBody = document.getElementById("vuelos-tbody");
	tableBody.innerHTML = "";


	vuelos.forEach(vuelo => {
		const row = document.createElement("tr");
		row.dataset.vueloId = vuelo.id

		const cellAerolinea = document.createElement("td");
		cellAerolinea.textContent = vuelo.airline;
		row.appendChild(cellAerolinea);

		const cellDestination = document.createElement("td");
		cellDestination.textContent = vuelo.destination;
		row.appendChild(cellDestination);

		const cellPrecio = document.createElement("td");
		cellPrecio.textContent = `${vuelo.current_price.toFixed(2)}`;
		row.appendChild(cellPrecio);

		let amountCell = document.createElement("td");
		let amountInput = document.createElement("input");
		amountInput.type = "number";
		amountInput.classList.add("quantity-input");
		amountInput.value = 1;
		amountInput.min = 1;
		amountInput.dataset.vueloId = vuelo.id;
		amountCell.appendChild(amountInput);
		row.appendChild(amountCell);


		let addButtonCell = document.createElement("td");
		let addButton = document.createElement("button");
		addButton.textContent = "Agregar";
		addButton.classList.add("row-action");
		addButton.addEventListener("click", (e) => {
			const row = e.target.closest("tr");

			const detalle = row.cells[0].textContent;
			const precio = Number(row.cells[2].textContent);
			const cantidad = Number(
				row.querySelector(".quantity-input").value || 1
			);

			const item = {
				id: row.dataset.vueloId,
				detalle,
				precio,
				cantidad,
				tipo_servicio: "Vuelo"
			};
			addServiceToPackage(item);
		});
		addButtonCell.appendChild(addButton);
		row.appendChild(addButtonCell);



		tableBody.appendChild(row);

	})
}

async function loadHoteles() {
	const result = await getHoteles();
	if (!result.ok) {
		alert("Ocurrió un error al cargar los hoteles");
		return;
	}

	const hoteles = result.content;
	const tableBody = document.getElementById("hoteles-tbody");
	tableBody.innerHTML = "";

	hoteles.forEach(hotel => {
		const row = document.createElement("tr");
		row.dataset.hotelId = hotel.id

		const cellName = document.createElement("td");
		cellName.textContent = hotel.name;
		row.appendChild(cellName);

		const cellCity = document.createElement("td");
		cellCity.textContent = hotel.city;
		row.appendChild(cellCity);

		const cellPrecio = document.createElement("td");
		cellPrecio.textContent = `${hotel.current_price.toFixed(2)}`;
		row.appendChild(cellPrecio);

		let amountCell = document.createElement("td");
		let amountInput = document.createElement("input");
		amountInput.type = "number";
		amountInput.classList.add("quantity-input");
		amountInput.value = 1;
		amountInput.min = 1;
		amountInput.dataset.hotelId = hotel.id;
		amountCell.appendChild(amountInput);
		row.appendChild(amountCell);

		let addButtonCell = document.createElement("td");
		let addButton = document.createElement("button");
		addButton.textContent = "Agregar";
		addButton.classList.add("row-action");
		addButton.addEventListener("click", (e) => {
			const row = e.target.closest("tr");

			const item = {
				id: row.dataset.hotelId,
				detalle: row.cells[0].textContent,
				precio: Number(row.cells[2].textContent),
				cantidad: Number(
					row.querySelector(".quantity-input").value || 1
				),
				tipo_servicio: "Hotel"
			};

			addServiceToPackage(item);
		});
		addButtonCell.appendChild(addButton);
		row.appendChild(addButtonCell);

		tableBody.appendChild(row);


	})
}

async function loadTransportes() {
	const result = await getTransportes();
	if (!result.ok) {
		alert("Ocurrió un error al cargar los transportes");
		return;
	}

	const transportes = result.content;
	const tableBody = document.getElementById("transportes-tbody");
	tableBody.innerHTML = "";

	transportes.forEach(transporte => {
		const row = document.createElement("tr");
		row.dataset.transporteId = transporte.id

		const cellName = document.createElement("td");
		cellName.textContent = transporte.type_transport_code;
		row.appendChild(cellName);

		const cellDestination = document.createElement("td");
		cellDestination.textContent = transporte.destination;
		row.appendChild(cellDestination);

		const cellPrecio = document.createElement("td");
		cellPrecio.textContent = `${transporte.current_price.toFixed(2)}`;
		row.appendChild(cellPrecio);

		let amountCell = document.createElement("td");
		let amountInput = document.createElement("input");
		amountInput.type = "number";
		amountInput.classList.add("quantity-input");
		amountInput.value = 1;
		amountInput.min = 1;
		amountInput.dataset.transporteId = transporte.id;
		amountCell.appendChild(amountInput);
		row.appendChild(amountCell);

		let addButtonCell = document.createElement("td");
		let addButton = document.createElement("button");
		addButton.textContent = "Agregar";
		addButton.classList.add("row-action");
		addButton.addEventListener("click", (e) => {
			// addServiceToPackage("vuelo", vuelo.id);
			const row = e.target.closest("tr");

			const item = {
				id: row.dataset.transporteId,
				detalle: row.cells[1].textContent,
				precio: Number(row.cells[2].textContent),
				cantidad: Number(
					row.querySelector(".quantity-input").value || 1
				),
				tipo_servicio: "Transporte"
			};
			addServiceToPackage(item);
		});
		addButtonCell.appendChild(addButton);
		row.appendChild(addButtonCell);

		tableBody.appendChild(row);

	})
}

async function loadPaquetes() {
	const result = await getPaquetes();
	if (!result.ok) {
		alert("Ocurrió un error al cargar los paquetes");
		return;
	}

	const paquetes = result.content;
	const tableBody = document.getElementById("paquetes-table-body");
	tableBody.innerHTML = "";

	paquetes.forEach(paquete => {
		const row = document.createElement("tr");
		row.dataset.paqueteId = paquete.id

		const cellTitle = document.createElement("td");
		cellTitle.textContent = paquete.name;
		row.appendChild(cellTitle);

		const cellDescription = document.createElement("td");
		cellDescription.textContent = paquete.description;
		row.appendChild(cellDescription);

		const cellCountry = document.createElement("td");
		cellCountry.textContent = paquete.destination.country;
		row.appendChild(cellCountry);

		const cellCity = document.createElement("td");
		cellCity.textContent = paquete.destination.city;
		row.appendChild(cellCity);


		const totalGeneral = Object.values(paquete.services)
			.flat()
			.reduce((sum, item) => sum + item.total, 0);
			

		const cellTotal = document.createElement("td");
		cellTotal.textContent = `${totalGeneral.toFixed(2)}`;
		row.appendChild(cellTotal);

		let editButtonCell = document.createElement("td");
		let editButton = document.createElement("button");
		editButton.textContent = "Editar";
		editButton.classList.add("row-action");
		editButton.addEventListener("click", () => {
			selectPackage(paquete.id);
		});
		editButtonCell.appendChild(editButton);
		row.appendChild(editButtonCell);

		let deleteButtonCell = document.createElement("td");
		let deleteButton = document.createElement("button");
		deleteButton.textContent = "Desactivar";
		deleteButton.classList.add("row-action", "danger-small");
		deleteButton.addEventListener("click", () => {
			deletePackage(paquete.id);
		});
		deleteButtonCell.appendChild(deleteButton);
		row.appendChild(deleteButtonCell);

		tableBody.appendChild(row);

	})
}

async function deletePackage(paqueteId) {
	if (!confirm("¿Está seguro de que desea eliminar este paquete?")) {
		return;
	}

	const result = await deletePaquete(paqueteId);
	if (!result.ok) {
		alert("Ocurrió un error al eliminar el paquete");
		return;
	}
	
	alert("Paquete eliminado exitosamente");
	await loadPaquetes();
}


let selectedId = null;
async function selectPackage(paqueteId) {
	clean();
	let resultadoPaquete = await getPaqueteById(paqueteId);
	if (!resultadoPaquete.ok) {
		alert("Ocurrió un error al obtener el paquete");
		return;
	}
	selectedId = paqueteId;
	const paquete = resultadoPaquete.content;
	fieldPaqueteTitle.value = paquete.name;
	fieldPaqueteDescription.value = paquete.description;
	fieldPaqueteCountry.value = paquete.destination.country;
	fieldPaqueteCity.value = paquete.destination.city;

	let flightServices = paquete.services.flights.map(x => ({id: x.service.id, detalle:x.service.airline, precio: x.unit_price, cantidad: x.quantity, tipo_servicio: x.service_type}));
	let hotelServices = paquete.services.hotels.map(x => ({ id: x.service.id, detalle:x.service.name, precio: x.unit_price, cantidad: x.quantity, tipo_servicio: x.service_type }));
	let transportServices = paquete.services.transportation.map(x => ({ id: x.service.id, detalle:x.service.destination, precio: x.unit_price, cantidad: x.quantity, tipo_servicio: x.service_type }));
	nuevosServicios = [...flightServices, ...hotelServices, ...transportServices];
	await reloadSelectedServices();

}


//hay que hacer la funcionalidad de eliminar los servicios seleccionados
let nuevosServicios = [];
async function addServiceToPackage(element) {

	if (element.cantidad <= 0) {
		alert("La cantidad debe ser mayor a 0");
		return;
	}
	let existElement = nuevosServicios.find(x => x.id === element.id)
	if (existElement) {
		existElement.cantidad += element.cantidad;
	} else {
		nuevosServicios.push(element);
	}

	await reloadSelectedServices();

}

async function reloadSelectedServices() {
	const tableBody = document.getElementById("paquete-services-tbody");
	tableBody.innerHTML = "";
	let total = 0;
	nuevosServicios.forEach((servicio, index) => {
		const row = document.createElement("tr");
		
		let totalElement = servicio.precio * servicio.cantidad;
		total += servicio.precio * servicio.cantidad;

		const cellDetalle = document.createElement("td");
		cellDetalle.textContent = servicio.detalle;
		row.appendChild(cellDetalle);

		const cellPrecio = document.createElement("td");
		cellPrecio.textContent = `$${servicio.precio.toFixed(2)}`;
		row.appendChild(cellPrecio);

		const cellCantidad = document.createElement("td");
		cellCantidad.textContent = servicio.cantidad;
		row.appendChild(cellCantidad);

		const cellTotal = document.createElement("td");
		cellTotal.textContent = `$${totalElement.toFixed(2)}`;
		row.appendChild(cellTotal);

		const cellTipo = document.createElement("td");
		cellTipo.textContent = servicio.tipo_servicio;
		row.appendChild(cellTipo);

		let removeButtonCell = document.createElement("td");
		let removeButton = document.createElement("button");
		removeButton.textContent = "Quitar";
		removeButton.classList.add("row-action", "danger-small");
		removeButton.addEventListener("click", async () => {
			nuevosServicios.splice(index, 1);
			await reloadSelectedServices(); // Recargar la tabla
		});
		removeButtonCell.appendChild(removeButton);
		row.appendChild(removeButtonCell);

		tableBody.appendChild(row);
	});
	fieldTotalPrice.textContent = total.toFixed(2);
}

async function clean() {
	nuevosServicios = [];
	fieldPaqueteTitle.value = "";
	fieldPaqueteDescription.value = "";
	fieldPaqueteCountry.value = "";
	fieldPaqueteCity.value = "";
	selectedId = null;
	await reloadSelectedServices();
}

async function createPackage() {
	if(!verifyFields())	return;

	const newPackage = {
		destination:{
			country: fieldPaqueteCountry.value,
			city: fieldPaqueteCity.value
		},
		name: fieldPaqueteTitle.value,
		description: fieldPaqueteDescription.value,
		details: nuevosServicios
		.map(x=>({service_type: x.tipo_servicio, service_id: x.id, quantity:x.cantidad}))
	}
	
	const result = await createPaquete(newPackage);
	if (!result.ok) {
		alert("Ocurrió un error al crear el paquete");
		return;
	}

	alert("Paquete creado exitosamente");
	await clean();
	await loadPaquetes();

}

async function updatePackage() {
	if(!verifyFields())	return;
	if(!selectedId){
		alert("No se ha seleccionado ningún paquete para editar");
		return;
	}
	
	const updatedPackage = {
		destination:{
			country: fieldPaqueteCountry.value,
			city: fieldPaqueteCity.value
		},
		name: fieldPaqueteTitle.value,
		description: fieldPaqueteDescription.value,
		details: nuevosServicios
		.map(x=>({service_type: x.tipo_servicio, service_id: x.id, quantity:x.cantidad}))
	}

	console.log(updatedPackage);
	
	const result = await updatePaquete(selectedId, updatedPackage);
	if (!result.ok) {
		alert("Ocurrió un error al actualizar el paquete");
		return;
	}

	alert("Paquete actualizado exitosamente");
	await clean();
	await loadPaquetes();
}

function verifyFields()
{
	if(fieldPaqueteTitle.value.trim() === ""){
		alert("El título es requerido");
		return false;
	}

	if(fieldPaqueteDescription.value.trim() === ""){
		alert("La descripción es requerida");
		return false;
	}
	
	if(fieldPaqueteCountry.value.trim() === ""){
		alert("El país es requerido");
		return false;
	}

	if(fieldPaqueteCity.value.trim() === ""){
		alert("La ciudad es requerida");
		return false;
	}

	if(nuevosServicios.length === 0){
		alert("Debe agregar al menos un servicio al paquete");
		return false;
	}

	return true;
}
