from django.urls import path

from .views import (
    index,
    WorkerListView,
    WorkerDetailView,
    TaskListView,
    TaskDetailView,
    WorkerCreateView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerUpdateView,
    WorkerDeleteView,
    toggle_task_status,
    CompletedTaskListView,
    PendingTaskListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("tasks/<int:pk>/toggle-status/", toggle_task_status, name="toggle-task-status"),
    path("tasks/completed/", CompletedTaskListView.as_view(), name="completed-task-list"),
    path("tasks/pending/", PendingTaskListView.as_view(), name="pending-task-list"),
]

app_name = "manager"
