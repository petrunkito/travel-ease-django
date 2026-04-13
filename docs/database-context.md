# 📊 Database Context - TravelEase

## 🧠 Contexto General
- documento de contexto tambien: travel_ease.sql
TravelEase es un sistema de gestión para una agencia de viajes que permite:

- Administrar clientes
- Gestionar servicios turísticos (vuelos, hoteles, transporte)
- Crear paquetes turísticos combinando servicios
- Registrar reservas realizadas por clientes
- Gestionar pagos y facturación
- Mantener historial de precios y estados

El sistema está diseñado bajo un enfoque **OLTP**, pero preparado para análisis futuro (OLAP / BI).

---

## 🎯 Principios del Modelo

### 1. Separación de responsabilidades

- Servicios (Vuelo, Hotel, Transporte) → Datos base
- HistorialPrecio → Evolución de precios
- DetallePaquete → Precio definido del producto
- DetalleReserva → Precio vendido (inmutable)

---

### 2. Flujo de precios (CRÍTICO)


- Nunca se consulta el precio directamente en servicios al momento de vender
- El precio se **congela en la reserva**
- HistorialPrecio → DetallePaquete → DetalleReserva

---

### 3. Modelo flexible de servicios

Se usa:

- `TipoServicio` (string)
- `IdServicio` (int)

Para permitir múltiples tipos de servicios sin acoplar el modelo.

---

## 🧭 Flujo completo del sistema

---

## 🧑‍💻 1. Crear Usuario (empleado del sistema)

- esto es solo como ejemplo ya que usaremos el auth_user propio de django
```sql
INSERT INTO Usuario (Nombre, Correo, Contrasena)
VALUES ('Aurelio Obando', 'aurelio@travelease.com', '123456');
```


- esto es solo como ejemplo ya que usaremos el auth_user propio de django

## 2. Asignar rol
```sql
SELECT Id FROM Rol WHERE Codigo = 'ASISTENTE';
```

```sql
INSERT INTO UsuarioRol (IdUsuario, IdRol)
VALUES (1, 1);
```


## 3. Crear ubicacion
```sql
INSERT INTO Departamento (Nombre, Codigo)
VALUES ('Managua', 'MAN');
```

```sql
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo)
VALUES (1, 'Managua', 'MAN-01');
```

## 4. Registrar cliente
```sql
INSERT INTO Cliente (
    IdMunicipio,
    IdUsuarioRegistro,
    Nombre,
    Cedula,
    Direccion,
    Numero
)
VALUES (
    1,
    1,
    'Juan Perez',
    '0010203031234R',
    'Centro Managua',
    '88888888'
);
```

# 5. Crear Servicios
```sql
INSERT INTO Vuelo (Aerolinea, Origen, Destino, FechaSalida, FechaLlegada)
VALUES ('Avianca', 'Managua', 'Madrid', GETDATE(), DATEADD(HOUR, 10, GETDATE()));
```

# 5. Transporte

```sql
INSERT INTO TipoTransporte (Nombre, Codigo)
VALUES ('Taxi', 'TAXI');

INSERT INTO Transporte (IdTipoTransporte, Origen, Destino)
VALUES (1, 'Aeropuerto', 'Hotel');
```

# 6. Definir Precios (HistorialPrecio)

```SQL
INSERT INTO HistorialPrecio (TipoServicio, IdServicio, Precio, FechaInicio)
VALUES 
('Vuelo', 1, 30000, GETDATE()),
('Hotel', 1, 5000, GETDATE()),
('Transporte', 1, 1000, GETDATE());
```


# 7. Crear Paquete Turístico
```sql
INSERT INTO PaqueteTuristico (IdUsuario, Nombre, Descripcion)
VALUES (1, 'Viaje Madrid', 'Vuelo + Hotel + Transporte');
```


# 8. Construir el paquete (DetallePaquete)
# obtener precios actuales

```sql
SELECT Precio 
FROM HistorialPrecio 
WHERE TipoServicio = 'Vuelo' 
AND IdServicio = 1 
AND FechaFin IS NULL;
```

# 9. Insertar detalle

```sql
INSERT INTO DetallePaquete
(IdPaquete, TipoServicio, IdServicio, Cantidad, PrecioUnitario, Total)
VALUES
(1, 'Vuelo', 1, 1, 30000, 30000),
(1, 'Hotel', 1, 1, 5000, 5000),
(1, 'Transporte', 1, 1, 1000, 1000);

```

# 9. Calcular total del paquete
```sql
SELECT SUM(Total)
FROM DetallePaquete
WHERE IdPaquete = 1;

```


# 10. Crear reserva
```sql
INSERT INTO Reserva (IdCliente, IdUsuarioVendedor, Total)
VALUES (1, 1, 36000);
```

# 11. Crear DetalleReserva (CLAVE)

```sql
INSERT INTO DetalleReserva
(IdReserva, IdPaquete, TipoServicio, IdServicio, Cantidad, PrecioUnitario, Total)
SELECT
    1,
    dp.IdPaquete,
    dp.TipoServicio,
    dp.IdServicio,
    dp.Cantidad,
    dp.PrecioUnitario,
    dp.Total
FROM DetallePaquete dp
WHERE dp.IdPaquete = 1;
```

# 12. Estado de la reserva
```sql
INSERT INTO DetalleReserva
(IdReserva, IdPaquete, TipoServicio, IdServicio, Cantidad, PrecioUnitario, Total)
SELECT
    1,
    dp.IdPaquete,
    dp.TipoServicio,
    dp.IdServicio,
    dp.Cantidad,
    dp.PrecioUnitario,
    dp.Total
FROM DetallePaquete dp
WHERE dp.IdPaquete = 1;

INSERT INTO HistorialEstadoReserva (IdReserva, IdEstado)
VALUES (1, 1);

```


# 13. Tipo de pago

```sql
INSERT INTO TipoPago (Nombre, Codigo)
VALUES ('Efectivo', 'EFEC');
```

# 14. Registrar pago
```sql
INSERT INTO Pago (IdReserva, IdTipoPago, Monto, Estado)
VALUES (1, 1, 36000, 'Pagado');
```

# 15. Generar factura
```sql
INSERT INTO Factura (IdReserva, NumeroFactura, FechaEmision, Total)
VALUES (1, 'FAC-0001', GETDATE(), 36000);
```

# Reglas importantes para desarrollo
- Nunca calcular precios en DetalleReserva
- Siempre usar DetallePaquete como fuente
- HistorialPrecio solo se usa al construir paquetes
- DetalleReserva representa una transacción histórica (no modificable)

