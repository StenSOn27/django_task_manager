from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from manager.models import Worker, Task, Position
from manager.models import TaskType

User = get_user_model()


class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "testpass123"
        self.user = Worker.objects.create_user(
            email="test@example.com",
            password=self.password
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Bugfix")
        self.position = Position.objects.create(name="Developer")
        self.task1 = Task.objects.create(
            name="Test Task 1",
            deadline="2030-01-01",
            task_type=self.task_type
        )
        self.task2 = Task.objects.create(
            name="Test Task 2",
            deadline="2030-01-01",
            task_type=self.task_type,
            is_completed=True
        )
    def test_index_view(self):
        url = reverse("manager:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/index.html")
        self.assertIn("num_workers", response.context)
        self.assertIn("num_visits", response.context)
        self.assertIn("completed_tasks", response.context)

    def test_worker_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("manager:worker-list"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('manager:worker-list')}")

    def test_worker_list_view_logged_in(self):
        response = self.client.get(reverse("manager:worker-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker-list.html")
        self.assertIn("worker_list", response.context)

    def test_task_list_view_search(self):
        response = self.client.get(reverse("manager:task-list"), {"name": "Test Task 1"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task 1")
        self.assertNotContains(response, "Test Task 2")

    def test_toggle_task_status(self):
        response = self.client.post(reverse("manager:toggle-task-status", kwargs={"pk": self.task1.pk}))
        self.assertEqual(response.status_code, 200)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)

    def test_toggle_task_status_404(self):
        response = self.client.post(reverse("manager:toggle-task-status", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)

def test_create_task_view(self):
    response = self.client.post(
        reverse("manager:task-create"),
        {
            "name": "New Task",
            "description": "Test desc",
            "deadline": "2030-01-01",
            "priority": "MEDIUM",  # <-- виправлено
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],  # <-- додано
        }
    )
    self.assertEqual(response.status_code, 302)
    self.assertTrue(Task.objects.filter(name="New Task").exists())


def test_update_task_view(self):
    response = self.client.post(
        reverse("manager:task-update", kwargs={"pk": self.task1.pk}),
        {
            "name": "Updated Task",
            "description": "Updated desc",
            "deadline": "2030-01-01",
            "priority": "HIGH",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }
    )
    self.assertEqual(response.status_code, 302)
    self.task1.refresh_from_db()
    self.assertEqual(self.task1.name, "Updated Task")


    def test_delete_task_view(self):
        response = self.client.post(reverse("manager:task-delete", kwargs={"pk": self.task1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
