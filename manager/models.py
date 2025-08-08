from .managers import WorkerManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
    )
    email = models.EmailField(unique=True)
    position = models.ForeignKey(
        "Position", on_delete=models.SET_NULL, null=True, related_name="workers"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = WorkerManager()  # type: ignore

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("manager:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    priority_choices = (
        ("URGENT", "Urgent"),
        ("HIGH", "High"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=priority_choices, default="MEDIUM"
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField("Worker", related_name="tasks", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager:task-detail", kwargs={"pk": self.pk})


class CompletedTask(Task):
    class Meta:
        proxy = True
        ordering = ["-deadline"]


class PendingTask(Task):
    class Meta:
        proxy = True
        ordering = ["deadline"]
