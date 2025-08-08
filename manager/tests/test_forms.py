import datetime
from django.test import TestCase
from manager.forms import (
    TaskForm,
    WorkerCreationForm,
    WorkerUsernameSearchForm,
    TaskNameSearchForm,
)
from manager.models import TaskType, Worker, Position


class TaskFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            email="test@example.com", password="pass1234", position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_form_valid_data(self):
        data = {
            "name": "Test Task",
            "description": "Test Description",
            "deadline": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "priority": "MEDIUM",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_task_form_past_deadline(self):
        data = {
            "name": "Past Task",
            "description": "Should fail",
            "deadline": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            "priority": "HIGH",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Deadline cannot be earlier than today.", form.errors.get("deadline", []))

    def test_task_form_invalid_priority(self):
        data = {
            "name": "Invalid Priority",
            "description": "Test",
            "deadline": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            "priority": "INVALID",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)


class WorkerCreationFormTest(TestCase):
    def test_worker_form_generates_username(self):
        form_data = {
            "email": "newuser@example.com",
            "password1": "SecurePass123",
            "password2": "SecurePass123",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        worker = form.save()
        self.assertTrue(worker.username.startswith("user_"))
        self.assertEqual(worker.email, "newuser@example.com")

    def test_worker_form_password_mismatch(self):
        form_data = {
            "email": "user@example.com",
            "password1": "pass1",
            "password2": "pass2",
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class WorkerUsernameSearchFormTest(TestCase):
    def test_search_form_blank(self):
        form = WorkerUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_search_form_with_value(self):
        form = WorkerUsernameSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "john")


class TaskNameSearchFormTest(TestCase):
    def test_task_search_form_blank(self):
        form = TaskNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_task_search_form_with_value(self):
        form = TaskNameSearchForm(data={"name": "Fix bug"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Fix bug")
