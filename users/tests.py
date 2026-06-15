from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase


class UsersModuleTests(TestCase):
	def test_profile_is_created_when_user_is_created(self):
		user_model = get_user_model()
		user = user_model.objects.create_user(
			username='tester',
			email='tester@example.com',
			password='strong-pass-123',
		)

		self.assertTrue(hasattr(user, 'profile'))
		self.assertEqual(user.profile.user, user)

	def test_default_groups_exist(self):
		self.assertTrue(Group.objects.filter(name='ADMIN').exists())
		self.assertTrue(Group.objects.filter(name='ASISTENTE').exists())
