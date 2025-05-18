from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Worker

class WorkerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("username", "first_name", "last_name", "email")