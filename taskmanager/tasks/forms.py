from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'status', 'description']