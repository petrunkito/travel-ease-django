from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.catalogos.departamentos.models import Department

from .models import Municipality


class MunicipalityByDepartmentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name='Test Managua', code='TST-MAN')
        self.other_department = Department.objects.create(name='Test León', code='TST-LEO')
        Municipality.objects.create(
            department=self.department,
            name='Test Managua I',
            code='TST-MAN-01',
        )
        Municipality.objects.create(
            department=self.department,
            name='Test Managua II',
            code='TST-MAN-02',
        )
        Municipality.objects.create(
            department=self.other_department,
            name='Test León I',
            code='TST-LEO-01',
        )

    def test_get_municipalities_by_department_id(self):
        response = self.client.get(f'/api/municipios/departamento/{self.department.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        returned_codes = {item['code'] for item in response.data}
        self.assertSetEqual(returned_codes, {'TST-MAN-01', 'TST-MAN-02'})
        self.assertTrue(all(item['department'] == self.department.id for item in response.data))

    def test_get_municipalities_by_department_returns_404_when_department_does_not_exist(self):
        response = self.client.get('/api/municipios/departamento/9999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Departamento no encontrado.')