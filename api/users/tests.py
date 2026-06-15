from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UsersModuleTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user_model = get_user_model()

	def test_profile_is_created_when_user_is_created(self):
		user = self.user_model.objects.create_user(
			username='tester',
			email='tester@example.com',
			password='strong-pass-123',
		)

		self.assertTrue(hasattr(user, 'profile'))
		self.assertEqual(user.profile.user, user)

	def test_default_groups_exist(self):
		self.assertTrue(Group.objects.filter(name='ADMIN').exists())
		self.assertTrue(Group.objects.filter(name='ASISTENTE').exists())

	def test_login_and_create_assistant_employee(self):
		admin_user = self.user_model.objects.create_superuser(
			username='admin',
			email='admin@example.com',
			password='adminpass123',
		)

		login_response = self.client.post(
			'/api/users/login/',
			{'username': 'admin', 'password': 'adminpass123'},
			format='json',
		)
		self.assertEqual(login_response.status_code, status.HTTP_200_OK)
		token = login_response.data['token']

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
		create_response = self.client.post(
			'/api/users/employees/',
			{
				'username': 'assistant1',
				'email': 'assistant1@example.com',
				'password': 'assistantpass123',
			},
			format='json',
		)

		self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
		assistant_user = self.user_model.objects.get(username='assistant1')
		self.assertTrue(assistant_user.is_staff)
		self.assertTrue(assistant_user.groups.filter(name='ASISTENTE').exists())
		self.assertTrue(hasattr(assistant_user, 'profile'))

		self.assertTrue(admin_user.is_superuser)

	def test_non_admin_cannot_create_employee(self):
		normal_user = self.user_model.objects.create_user(
			username='normal',
			email='normal@example.com',
			password='normalpass123',
		)
		self.client.force_authenticate(user=normal_user)

		response = self.client.post(
			'/api/users/employees/',
			{
				'username': 'assistant2',
				'email': 'assistant2@example.com',
				'password': 'assistantpass123',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_admin_can_list_employees_with_roles(self):
		admin_user = self.user_model.objects.create_superuser(
			username='admin2',
			email='admin2@example.com',
			password='adminpass123',
		)
		assistant_user = self.user_model.objects.create_user(
			username='assistant3',
			email='assistant3@example.com',
			password='assistantpass123',
		)
		assistant_user.is_staff = True
		assistant_user.save()
		assistant_group = Group.objects.get(name='ASISTENTE')
		assistant_user.groups.add(assistant_group)

		self.client.force_authenticate(user=admin_user)
		response = self.client.get('/api/users/employees/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreaterEqual(len(response.data), 2)
		assistant_payload = next(
			(item for item in response.data if item['username'] == 'assistant3'),
			None,
		)
		self.assertIsNotNone(assistant_payload)
		self.assertIn('ASISTENTE', assistant_payload['roles'])

	def test_non_admin_cannot_list_employees(self):
		normal_user = self.user_model.objects.create_user(
			username='normal2',
			email='normal2@example.com',
			password='normalpass123',
		)
		self.client.force_authenticate(user=normal_user)

		response = self.client.get('/api/users/employees/')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
