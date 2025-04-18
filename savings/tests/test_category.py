from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import Category, User

class CategoryTests(APITestCase):
    def setUp(self):
        Category.objects.all().delete()  # Opcional, para asegurar limpieza total
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.valid_data = {
            "name": "Comida",
            "type": "expense"
        }

    def test_create_category_success(self):
        response = self.client.post(reverse('category-list-create'), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, "Comida")

    def test_create_category_missing_name(self):
        data = {"type": "expense"}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_invalid_type(self):
        data = {"name": "Viaje", "type": "invalid_type"}
        response = self.client.post(reverse('category-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_category(self):
        self.client.post(reverse('category-list-create'), self.valid_data)
        response = self.client.post(reverse('category-list-create'), self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_category_list(self):
        Category.objects.filter(user=self.user).delete()
        Category.objects.create(user=self.user, **self.valid_data)

        response = self.client.get(reverse('category-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]['name'], "Comida")

    def test_get_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('category-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_category(self):
        category = Category.objects.create(user=self.user, **self.valid_data)
        url = reverse('category-detail', args=[category.id])
        response = self.client.patch(url, {"name": "Supermercado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, "Supermercado")

    def test_delete_category(self):
        category = Category.objects.create(user=self.user, **self.valid_data)
        url = reverse('category-detail', args=[category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.exists())