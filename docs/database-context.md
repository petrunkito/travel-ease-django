# Database Context - Travel Ease

## Source of truth
- Main script: `travel_ease.sql`
- This file is a human-readable guide for API and model decisions.

## Core domains
- Access and users: Usuario, Rol, UsuarioRol
- Geography and customers: Departamento, Municipio, Cliente
- Services: Vuelo, Hotel, TipoTransporte, Transporte
- Catalog and pricing: PaqueteTuristico, DetallePaquete, HistorialPrecio
- Sales and lifecycle: Reserva, DetalleReserva, EstadoReserva, HistorialEstadoReserva
- Billing: Pago, Factura

## Main relationships
- UsuarioRol links Usuario <-> Rol (many-to-many)
- Municipio belongs to Departamento
- Cliente belongs to Municipio and references Usuario (creator)
- PaqueteTuristico references Usuario
- DetallePaquete belongs to PaqueteTuristico
- Reserva references Cliente and Usuario (seller)
- DetalleReserva belongs to Reserva and can reference PaqueteTuristico
- HistorialEstadoReserva belongs to Reserva and EstadoReserva
- Pago and Factura belong to Reserva

## Suggested Django model map
- `Usuario` -> Custom user model or profile model (decide early)
- `Rol` + `UsuarioRol` -> role model and through table
- `Cliente` -> customer model
- `PaqueteTuristico` + `DetallePaquete` -> package aggregate
- `Reserva` + `DetalleReserva` + `HistorialEstadoReserva` -> booking aggregate
- `Pago` + `Factura` -> payment and invoice models

## SQL notes to review before migration to Django
- Table naming mismatch: `Rol` is created but inserts/references use `Roles`.
- SQL uses `IDENTITY`, `BIT`, and `GETDATE()` (SQL Server style).
- Django + SQLite equivalents:
  - `IDENTITY` -> `AutoField` / `BigAutoField`
  - `BIT` -> `BooleanField`
  - `GETDATE()` -> `auto_now_add=True` or `timezone.now`

## Rules for future development
1. Keep model names in English in Django code.
2. Preserve business meaning from SQL even if table names change.
3. Validate foreign-key flows in serializers.
4. Add tests for booking, status history, and payment flow first.

## How to keep this updated
- Update this file whenever `travel_ease.sql` changes.
- Document any intentional divergence between SQL and Django models.
