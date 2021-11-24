from django.urls import path
from . import views


urlpatterns = [
    path('', views.userboard, name='userboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('todolist/<int:pk>', views.todolist, name='todolist'),
    path('delete_list/<int:pk>', views.delete_list, name='delete_list'),
    path('finish_list', views.finish_list, name='finish_list'),
    path('delete_task', views.delete_task, name='delete_task'),
    path('create_task', views.create_task, name='create_task'),
    path('update_task', views.update_task, name='update_task'),
    path('complete_task', views.complete_task, name='complete_task'),
]
