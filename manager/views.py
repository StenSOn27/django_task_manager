from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Worker, Task


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