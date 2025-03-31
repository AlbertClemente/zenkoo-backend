from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import Notification, User

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='noti@correo.com',
            password='clave123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.notification = Notification.objects.create(
            user=self.user,
            message='Tienes una nueva notificación'
        )

    def test_get_notifications(self):
        response = self.client.get(reverse('notification-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_notification_as_read(self):
        url = reverse('notification-mark-read', kwargs={'pk': self.notification.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_read'])
