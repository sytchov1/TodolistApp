from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import TodoList, Task


class MyUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(MyUserForm, self).__init__(*args, **kwargs)

        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

        self.fields['username'].label = 'Логин'
        self.fields['password2'].label = 'Повторите пароль'


class TDListCreationForm(ModelForm):
    class Meta:
        model = TodoList
        fields = ['title', 'deadline']
        labels = {'title': 'Придумайте название', 'deadline': 'Укажите крайний срок'}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class TaskCreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']
        labels = {'description': 'Опишите задачу'}
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8, 'cols': 40, 'placeholder': 'Нужно сделать...'}),
        }
