from django.test import TestCase
from django.utils.timezone import now, timedelta
from manager.models import Position, Worker, TaskType, Task


class ModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug Fix")

    def test_position_str(self):
        self.assertEqual(str(self.position), "Developer")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "testuser")

    def test_worker_absolute_url(self):
        self.assertEqual(self.worker.get_absolute_url(), f"/workers/{self.worker.pk}/")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Bug Fix")

    def test_task_creation_and_str(self):
        task = Task.objects.create(
            name="Fix login bug",
            description="Fix OAuth error",
            deadline=now().date() + timedelta(days=3),
            task_type=self.task_type,
            priority="HIGH"
        )
        task.assignees.add(self.worker)
        self.assertEqual(str(task), "Fix login bug")
        self.assertIn(self.worker, task.assignees.all())

