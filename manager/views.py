from dis import Positions
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from manager.forms import (
    TaskForm,
    WorkerUsernameSearchForm,
    TaskNameSearchForm,
    WorkerCreationForm,
)
from .models import Worker, Task
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST


def index(request):
    """View function for the home page of the site."""
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "manager/index.html", context=context)


class WorkerListView(generic.ListView):
    """Generic class-based view for a list of workers."""

    model = Worker
    template_name = "manager/worker-list.html"
    context_object_name = "worker_list"
    paginate_by = 5
    queryset = Worker.objects.select_related()

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerUsernameSearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerUsernameSearchForm(initial={"username": username})

        # Список кольорів для аватарів
        colors = [
            "#f97316", "#84cc16", "#06b6d4", "#ef4444",
            "#8b5cf6", "#f59e0b", "#10b981", "#3b82f6"
        ]

        # Присвоюємо кожному робітнику ініціали та колір
        workers = context.get("worker_list")
        if workers:
            for idx, worker in enumerate(workers):
                worker.initials = worker.username[:2].upper()
                worker.color = colors[idx % len(colors)]

        return context


class WorkerDetailView(generic.DetailView):
    """Generic class-based view for a worker's detail."""

    model = Worker
    template_name = "manager/worker-detail.html"
    context_object_name = "worker"
    queryset = Worker.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object  # type: ignore

        context["total_tasks_count"] = worker.tasks.count()
        context["completed_tasks_count"] = worker.tasks.filter(is_completed=True).count()
        context["in_progress_tasks_count"] = worker.tasks.filter(is_completed=False).count()

        return context

class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "manager/worker-form.html"
    success_url = reverse_lazy("manager:worker-list")


class WorkerUpdateView(generic.UpdateView):
    """Generic class-based view for updating a worker's details."""

    model = Worker
    template_name = "manager/worker-update.html"
    fields = ["username", "first_name", "last_name", "email", "position"]
    success_url = reverse_lazy("manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from manager.models import Position  # імпортуй, якщо потрібно
        context["positions"] = Position.objects.all()
        context["is_object"] = True

        return context


class WorkerDeleteView(generic.DeleteView):
    """Generic class-based view for deleting a worker."""

    model = Worker
    template_name = "manager/worker_confirm_delete.html"
    success_url = reverse_lazy("manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of tasks."""

    model = Task
    template_name = "manager/task-list.html"
    context_object_name = "task_list"
    paginate_by = 5
    queryset = Task.objects.prefetch_related()
    ordering = ["-is_completed", "deadline"]

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskNameSearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based view for a task's detail."""

    model = Task
    template_name = "manager/task-detail.html"
    context_object_name = "task"


User = get_user_model()

class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """Generic class-based view for creating a new task."""

    model = Task
    form_class = TaskForm
    template_name = "manager/task-form.html"
    success_url = reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context['users'] = User.objects.filter(email__isnull=False).exclude(email='').order_by('email')
        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Generic class-based view for updating a task's details."""

    model = Task
    form_class = TaskForm
    template_name = "manager/task-form.html"
    success_url = reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_object'] = True  # тут об'єкт існує — редагування
        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Generic class-based view for deleting a task."""

    model = Task
    template_name = "manager/task_confirm_delete.html"
    success_url = reverse_lazy("manager:task-list")

@require_POST
def toggle_task_status(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({
            "status": "success",
            "is_completed": task.is_completed,
        })
    except Task.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Task not found"
        }, status=404)