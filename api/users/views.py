from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminOrSuperuser
from .serializers import EmployeeCreateSerializer, EmployeeListSerializer


class LoginAPIView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')

		if not username or not password:
			return Response(
				{'error': 'Debe enviar username y password.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		user = authenticate(request, username=username, password=password)
		if not user:
			return Response(
				{'error': 'Credenciales invalidas.'},
				status=status.HTTP_401_UNAUTHORIZED,
			)

		token, _ = Token.objects.get_or_create(user=user)
		return Response({'token': token.key}, status=status.HTTP_200_OK)


class EmployeeCreateAPIView(APIView):
	permission_classes = [IsAdminOrSuperuser]

	def get(self, request):
		employees = (
			request.user.__class__.objects.filter(is_staff=True)
			.prefetch_related('groups')
			.order_by('id')
		)
		serializer = EmployeeListSerializer(employees, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = EmployeeCreateSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		role_names = list(user.groups.values_list('name', flat=True))
		return Response(
			{
				'id': user.id,
				'username': user.username,
				'email': user.email,
				'is_staff': user.is_staff,
				'roles': role_names,
			},
			status=status.HTTP_201_CREATED,
		)
