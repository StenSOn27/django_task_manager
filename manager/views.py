from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Worker, Task
from .forms import WorkerCreateForm
from django.views import generic


@login_required
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


class WorkerDetailView(generic.DetailView):
    """Generic class-based view for a worker's detail."""
    model = Worker
    template_name = "manager/worker-detail.html"
    context_object_name = "worker"


class WorkerCreateView(generic.CreateView):
    form_class = WorkerCreateForm
    template_name = "manager/worker-form.html"
    success_url = reverse_lazy("manager:worker-list")


class TaskListView(generic.ListView):
    """Generic class-based view for a list of tasks."""
    model = Task
    template_name = "manager/task-list.html"
    context_object_name = "task_list"
    paginate_by = 5
    queryset = Task.objects.prefetch_related()


class TaskDetailView(generic.DetailView):
    """Generic class-based view for a task's detail."""
    model = Task
    template_name = "manager/task-detail.html"
    context_object_name = "task"


class TaskCreateView(generic.CreateView):
    """Generic class-based view for creating a new task."""
    model = Task
    template_name = "manager/task-form.html"
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    success_url = reverse_lazy("manager:task-list")