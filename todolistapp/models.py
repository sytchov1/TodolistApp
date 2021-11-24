from django.db import models
from django.conf import settings


# Create your models here.
class TodoList(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    finished = models.BooleanField(default=False)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    completion_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)


class Task(models.Model):
    todolist_id = models.ForeignKey('TodoList', on_delete=models.CASCADE)
    description = models.TextField(max_length=400)
    done = models.BooleanField(default=False)
