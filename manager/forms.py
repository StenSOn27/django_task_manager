import random
import string
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Worker, Task
import datetime


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    is_completed = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        ),
    )
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees"
        ]
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline is None:
            return deadline

        if deadline < datetime.date.today():
            raise forms.ValidationError(
                "Deadline cannot be earlier than today."
            )
        return deadline


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
                "class": "search-input"
            }
        )
    )


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task name",
                "class": "search-input"
            }
        )
    )

class WorkerCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Worker
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = self.generate_random_username()
        if commit:
            user.save()
        return user

    def generate_random_username(self, length=10):
        return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
