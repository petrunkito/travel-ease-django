# Instrucciones Globales del Proyecto (Travel Ease API)

## Objetivo
Este repositorio contruye una API REST para un proyecto universitario, para la agencia de viajes TravelEase.
Entre usus principales funcionalidades se encuentran la gestion de reservas, clientes, paquetes turistico y los pagos que seran pagados inmediatamente en el local, tambien para esto es necesario uso del contexto del modelo de base de datos.

## Stack
- Python 3.12
- Django
- Django REST Framework
- Base de datos local de desarrollo: SQLite(usaremos este en el desarrollo del sistema)
- Base de datos local de desarrollo: SQL Server para posteriormente probarla en una base de datos SQL Server

## Contexto de base de datos
- Fuente SQL de referencia: `travel_ease.sql`.
- Resumen funcional del esquema: `docs/database-context.md`.
- Cuando se implementen modelos Django, priorizar consistencia con esas dos fuentes.

## Convenciones de desarrollo
- Usar nombres en ingles para codigo (modelos, serializers, endpoints, variables).
- Usar respuestas de error en español para endpoints, con mensajes claros para el cliente.
- Escribir comentarios solo cuando una decision no sea obvia.
- Tratar que las vistas sean el punto de logica de negocio, pero cuando sea necesario se pueden delegar tareas complejas a los serializers, servicios u otros
- Mantener endpoints consistentes en formato de respuesta y codigos HTTP.

## Reglas para endpoints
- No es necesario versionar la API para este proyecto, pero mantener una estructura clara de rutas (ej: /api/reservas/, /api/clientes/).
- Validar entradas con serializers.
- Responder errores de forma explicita y consistente.

## Seguridad minima
- No exponer secretos en el codigo.
- Mantener DEBUG solo para desarrollo.
- Revisar permisos/autenticacion al crear endpoints reales.

## Antes de terminar cualquier cambio
- Ejecutar check de Django.
- Ejecutar migraciones si hubo cambios en modelos.
- Verificar que rutas nuevas esten registradas.

## Personalizacion
Edita este archivo para reflejar:
- El dominio principal del proyecto son la creacion de clientes, reservas, paquetes turisticos y pagos(que estos son alli mismo en el local en efectivo disponible por el momento).
- El proyecto debe seguir el contexto de base de datos definido en `travel_ease.sql` y `docs/database-context.md`.
- El proyecto debe ser modular, ejemplo: en la creacion de los servicios tenemos esta estructura:
```- services/
    - hotel/
      - modulo python para gestion de hoteles
    - transportes
      - modulo python para gestion de transportes
    - vuelos/
      - modulo python para gestion de vuelos
```
- las reservas tendra su propia carpeta, ya que es el modulo mas importante del proyecto, y dentro de esta carpeta se tendra la gestion de reservas, como lo son los endpoints, los serializers, los modelos y los tests.
- los paquetes turisticos son armados con los servicios disponibles
- el pago se hace al momento de la creacion de la reserva, y se registra en el sistema, pero no se integra con un sistema de pago externo, ya que el pago es en efectivo en el local.
- Requisitos de la entrega final.
- el sistema debe usar una base de sql server, pero usaremos sqlite3 para el desarrollo local, y luego se migrara a sql server para la entrega final.
