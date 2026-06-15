# Development Checklist - Django REST API

## Antes de desarrollar
- Entender requerimiento funcional.
- Definir contrato del endpoint (request/response).
- Identificar validaciones y permisos.

## Durante el desarrollo
- Crear/ajustar serializer.
- Implementar vista o viewset.
- Registrar URL.
- Crear test minimo para caso exitoso y fallo principal.

## Antes de cerrar tarea
- Ejecutar: .venv/bin/python manage.py check
- Ejecutar pruebas de la app afectada.
- Ejecutar migraciones si hubo cambios de modelos.
- Revisar formato de respuesta y HTTP status.

## Para entrega academica
- Confirmar endpoints pedidos por el docente.
- Verificar casos borde importantes.
- Dejar README/contexto actualizado.
