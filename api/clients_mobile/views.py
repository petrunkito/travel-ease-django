from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

class ClienteBaseAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        # Ejecuta la validación estándar de DRF
        super().initial(request, *args, **kwargs)

        # 1. Validar grupo "Cliente"
        if not request.user.groups.filter(name='Cliente').exists():
            raise PermissionDenied('Acceso denegado: No pertenece al grupo Cliente.')

        # 2. Adjuntar los datos del cliente a la petición
        try:
            request.cliente = request.user.client_account
        except AttributeError:
            raise NotFound('Perfil de cliente no encontrado para este usuario.')

# api/clientes/views.py


class PerfilClienteView(ClienteBaseAPIView):
    def get(self, request):
        # 'request.cliente' ya está disponible automáticamente
        cliente = request.cliente 
        
        return Response({
            'id': cliente.id,
            'telefono': cliente.phone_number,
            'direccion': cliente.address, 
            "cedula": cliente.national_id
        })