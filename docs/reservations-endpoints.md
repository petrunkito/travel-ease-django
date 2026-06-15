# Endpoints de Reservas - TravelEase API

## Base URL
```
http://localhost:8000/api/reservations/
```

## Endpoints disponibles

### 1. **Listar tipos de pago**
```
GET /api/reservations/payment-types/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "EFECTIVO",
    "code": "EFEC",
    "active": true
  }
]
```

---

### 2. **Listar estados de reserva**
```
GET /api/reservations/reservation-statuses/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Pendiente",
    "code": "PEND"
  },
  {
    "id": 2,
    "name": "Pagado",
    "code": "PAG"
  },
  {
    "id": 3,
    "name": "Cancelado",
    "code": "CANC"
  }
]
```

---

### 3. **Crear una nueva reserva**
```
POST /api/reservations/reservations/
```

**Body:**
```json
{
  "client_id": 1,
  "package_id": 1,
  "payment_type_id": 1,
  "seller_user_id": 1
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "client": 1,
  "client_name": "Juan Perez",
  "payment_type": 1,
  "payment_type_name": "EFECTIVO",
  "seller_user": 1,
  "seller_user_name": "Aurelio Obando",
  "date": "2026-05-10T15:30:00Z",
  "total": "500.00",
  "active": true,
  "details": [
    {
      "id": 1,
      "service_type": "VUELO",
      "service_type_display": "Vuelo",
      "service_id": 1,
      "quantity": 2,
      "unit_price": "150.00",
      "total": "300.00"
    },
    {
      "id": 2,
      "service_type": "HOTEL",
      "service_type_display": "Hotel",
      "service_id": 1,
      "quantity": 3,
      "unit_price": "66.67",
      "total": "200.00"
    }
  ],
  "status_history": [
    {
      "id": 1,
      "status": 1,
      "status_display": "Pendiente",
      "date": "2026-05-10T15:30:00Z"
    }
  ],
  "current_status": {
    "id": 1,
    "name": "Pendiente",
    "code": "PEND"
  },
  "invoice": {
    "id": 1,
    "invoice_number": "FAC-000001",
    "issue_date": "2026-05-10T15:30:00Z",
    "total": "500.00"
  }
}
```

**Nota:** La factura se crea automáticamente al crear la reserva.

---

### 4. **Listar todas las reservas**
```
GET /api/reservations/reservations/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "client": 1,
    "client_name": "Juan Perez",
    "payment_type": 1,
    "payment_type_name": "EFECTIVO",
    "seller_user": 1,
    "seller_user_name": "Aurelio Obando",
    "date": "2026-05-10T15:30:00Z",
    "total": "500.00",
    "active": true,
    "details": [...],
    "status_history": [...],
    "current_status": {...},
    "invoice": null
  }
]
```

---

### 5. **Obtener detalle de una reserva**
```
GET /api/reservations/reservations/{id}/
```

**Respuesta:**
```json
{
  "id": 1,
  "client": 1,
  "client_name": "Juan Perez",
  "payment_type": 1,
  "payment_type_name": "EFECTIVO",
  "seller_user": 1,
  "seller_user_name": "Aurelio Obando",
  "date": "2026-05-10T15:30:00Z",
  "total": "500.00",
  "active": true,
  "details": [
    {
      "id": 1,
      "service_type": "VUELO",
      "service_type_display": "Vuelo",
      "service_id": 1,
      "quantity": 2,
      "unit_price": "150.00",
      "total": "300.00"
    }
  ],
  "status_history": [
    {
      "id": 1,
      "status": 1,
      "status_display": "Pendiente",
      "date": "2026-05-10T15:30:00Z"
    }
  ],
  "current_status": {
    "id": 1,
    "name": "Pendiente",
    "code": "PEND"
  },
  "invoice": null
}
```

---

### 6. **Actualizar el estado de una reserva**
```
PUT /api/reservations/reservations/{id}/update_status/
```

**Body:**
```json
{
  "status_id": 2
}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "client": 1,
  "client_name": "Juan Perez",
  "payment_type": 1,
  "payment_type_name": "EFECTIVO",
  "seller_user": 1,
  "seller_user_name": "Aurelio Obando",
  "date": "2026-05-10T15:30:00Z",
  "total": "500.00",
  "active": true,
  "details": [...],
  "status_history": [
    {
      "id": 1,
      "status": 1,
      "status_display": "Pendiente",
      "date": "2026-05-10T15:30:00Z"
    },
    {
      "id": 2,
      "status": 2,
      "status_display": "Pagado",
      "date": "2026-05-10T15:35:00Z"
    }
  ],
  "current_status": {
    "id": 2,
    "name": "Pagado",
    "code": "PAG"
  },
  "invoice": null
}
```

---

### 7. **Obtener historial de cambios de estado**
```
GET /api/reservations/reservations/{id}/status_history/
```

**Respuesta:**
```json
[
  {
    "id": 2,
    "status": 2,
    "status_display": "Pagado",
    "date": "2026-05-10T15:35:00Z"
  },
  {
    "id": 1,
    "status": 1,
    "status_display": "Pendiente",
    "date": "2026-05-10T15:30:00Z"
  }
]
```

---

### 8. **Desactivar una reserva (DELETE)**
```
DELETE /api/reservations/reservations/{id}/
```

**Respuesta (204 No Content):**
```json
{
  "message": "Reserva desactivada correctamente."
}
```

---

## Códigos de error

| Código | Descripción |
|--------|-------------|
| 400 | Solicitud inválida (validación de datos) |
| 404 | Reserva no encontrada |
| 409 | Operación no permitida (ej: cambiar estado de reserva cancelada) |

---

## Ejemplos con cURL

### Crear una reserva:
```bash
curl -X POST http://localhost:8000/api/reservations/reservations/ \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "package_id": 1,
    "payment_type_id": 1,
    "seller_user_id": 1
  }'
```

### Cambiar estado a Pagado:
```bash
curl -X PUT http://localhost:8000/api/reservations/reservations/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status_id": 2
  }'
```

### Obtener historial de estados:
```bash
curl -X GET http://localhost:8000/api/reservations/reservation-statuses/
```

---

## Notas importantes

1. **Estados por defecto:** Al iniciar la aplicación, se crean automáticamente tres estados:
   - Pendiente (PEND)
   - Pagado (PAG)
   - Cancelado (CANC)

2. **Tipo de pago:** Por defecto solo existe EFECTIVO (EFEC)

3. **Restricción de cambio de estado:** No se puede cambiar el estado de una reserva si ya está en estado "Pagado" o "Cancelado"

4. **Detalles de reserva:** Se crean automáticamente a partir de los detalles del paquete turístico

5. **Factura automática:** Se crea automáticamente al crear la reserva, con un número secuencial único
