from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import Reflection, User

class ReflectionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='reflex@correo.com',
            password='123segura',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.data = {
            'title': 'Mi reflexión',
            'content': 'Hoy fue un buen día.'
        }

    def test_create_reflection(self):
        response = self.client.post(reverse('reflection-list-create'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_reflections(self):
        Reflection.objects.create(user=self.user, **self.data)
        response = self.client.get(reverse('reflection-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
