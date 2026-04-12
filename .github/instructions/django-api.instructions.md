---
applyTo: "**/*.py"
description: "Usar cuando se desarrollen archivos Python de la API Django/DRF para mantener arquitectura consistente"
---

# Guia para archivos Python (Django + DRF)

## Estructura sugerida
- Modelos en models.py
- Serializers en serializers.py
- Casos de uso simples en views.py/viewsets.py
- Rutas en urls.py
- Tests en tests/

## Estilo tecnico
- Preferir Class-Based Views o ViewSets cuando aporte claridad.
- Para endpoints sencillos, Function-Based Views tambien son validas.
- No duplicar validaciones entre serializer y view.

## Checklist por endpoint
1. Definir serializer de entrada/salida.
2. Implementar vista con manejo de errores controlado.
3. Registrar URL en la app y en el proyecto.
4. Agregar pruebas basicas (happy path + errores principales).
5. Verificar codigos HTTP correctos.

## Formato de respuesta recomendado
- Exito: datos claros y estructura estable.
- Error: mensaje util para cliente y detalle tecnico controlado.

## Personalizacion
Ajusta esta guia para incluir:
- Patrones exactos de respuesta JSON de tu curso.
- Reglas de autenticacion que te pidan.
- Niveles de cobertura de pruebas requeridos.
