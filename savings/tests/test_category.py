from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import Category, User

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='foopi@correo.com',
            password='clave123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': 'Comida',
            'type': 'expense'
        }

    def test_create_category(self):
        response = self.client.post(reverse('category-list-create'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories(self):
        Category.objects.create(user=self.user, **self.data)
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
