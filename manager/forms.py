from django import forms
from django.contrib.auth.forms import UserCreationForm
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
