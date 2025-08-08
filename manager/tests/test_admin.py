from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminPanelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="admin123"
        )
        self.client.login(email="admin@example.com", password="admin123")

        self.worker = get_user_model().objects.create_user(
            email="user@example.com",
            password="test123",
            username="testuser",
            position=None
        )

    def test_worker_list_display_in_admin(self):

        url = reverse("admin:manager_worker_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Position")
        self.assertContains(response, self.worker.username)

    def test_worker_form_contains_position(self):
        url = reverse("admin:manager_worker_change", args=[self.worker.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name=\"position\"")

    def test_worker_add_form_contains_position(self):
        url = reverse("admin:manager_worker_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="position"')
