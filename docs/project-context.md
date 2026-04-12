# Project Context - Travel Ease API

## 1. Que problema resuelve
Esta API permitira gestionar funcionalidades de un sistema de viajes para un proyecto universitario.

## 2. Dominio (basado en SQL)
Entidades principales actuales:
- Usuario, Rol, UsuarioRol
- Departamento, Municipio, Cliente
- Vuelo, Hotel, TipoTransporte, Transporte
- PaqueteTuristico, DetallePaquete, HistorialPrecio
- Reserva, DetalleReserva, EstadoReserva, HistorialEstadoReserva
- Pago, Factura

Ejemplo de regla de negocio:
- Una reserva no puede confirmarse si no hay cupos disponibles.

Ver detalle del esquema y relaciones en `docs/database-context.md`.

## 3. Estado actual
- Proyecto Django creado.
- DRF instalado y configurado.
- Endpoint de salud activo en /api/.

## 4. Roadmap corto
1. Modelar entidades base.
2. Crear serializers y endpoints CRUD iniciales.
3. Agregar autenticacion y permisos.
4. Escribir tests de endpoints criticos.

## 5. Decisiones tecnicas
- Entorno local: SQLite.
- API REST con DRF.
- Python 3.12.

## 6. Convenciones de equipo
- Codigo en ingles.
- Commits con mensaje claro por funcionalidad.
- No mezclar refactor grande con nueva feature en el mismo commit.

## 7. Personalizacion
Actualiza este archivo en cada entrega con:
- Lo implementado.
- Decisiones nuevas.
- Riesgos pendientes.
