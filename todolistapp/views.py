from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from .forms import MyUserForm, TDListCreationForm, TaskCreationForm
from .models import TodoList, Task
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone


DECLENSIONS = (('день', 'дня', 'дней'),
               ('час', 'часа', 'часов'),
               ('минута', 'минуты', 'минут'))


def remaining_time(deadline):
    result = ""

    if timezone.now() < deadline:
        diff = deadline - timezone.now()
        hours, tmp = divmod(diff.seconds, 3600)
        minutes = tmp // 60

        for period in zip([diff.days, hours, minutes], [0, 1, 2]):
            if period[0]:
                result += f'{period[0]} {DECLENSIONS[period[1]][get_declension(period[0])]} '
    return result


def get_declension(number):
    b = number % 10
    a = (number % 100 - b) / 10

    if a == 0 or a >= 2:
        if b == 0 or (4 < b <= 9):
            return 2
        else:
            return 1 if b != 1 else 0
    else:
        return 2


def index(request):
    return render(request, 'todolistapp/index.html')


def register(request):
    form = MyUserForm()
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/todolistapp/login')
    context = {'form': form}
    return render(request, 'todolistapp/register.html', context)


def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('userboard'))
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            return redirect('login')
    return render(request, 'todolistapp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def userboard(request):
    user = request.user
    form = TDListCreationForm()
    if request.method == 'POST' and request.is_ajax():
        deadline = datetime.strptime(request.POST.get('deadline'), "%Y-%m-%dT%H:%M")
        tdlist = TodoList.objects.create(user_id=user, title=request.POST.get('title'), deadline=timezone.make_aware(deadline))
        tdlist.save()
        data = {
            'list_id': tdlist.id,
            'list_title': tdlist.title,
            'list_deadline': remaining_time(tdlist.deadline)
        }
        return JsonResponse(data)

    lists = TodoList.objects.filter(user_id=user.id).order_by('finished', 'deadline')

    for list in lists:
        task_amount = Task.objects.filter(todolist_id=list.id)
        list.tasks_amount = task_amount.count()
        list.completed_tasks_amount = task_amount.filter(done=True).count()
        list.rem = remaining_time(list.deadline)
    return render(request, 'todolistapp/userboard.html', {'lists': lists, 'form': form})


@login_required(login_url='login')
def todolist(request, pk):
    form = TaskCreationForm()
    tdlist = TodoList.objects.get(id=pk)
    tasks = Task.objects.filter(todolist_id=tdlist.id).order_by('-id')

    tdlist.tasks_amount = tasks.count()
    tdlist.completed_tasks_amount = tasks.filter(done=True).count()
    tdlist.rem = remaining_time(tdlist.deadline)

    contex = {
        'tdlist': tdlist,
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'todolistapp/todolist.html', contex)


def delete_list(request, pk):
    if request.method == 'POST':
        tdlist = TodoList.objects.get(id=pk)
        tdlist.delete()
        return HttpResponseRedirect(reverse('userboard'))


def create_task(request):
    if request.method == 'POST' and request.is_ajax():
        tdlist = TodoList.objects.get(id=request.POST.get('list_id'))
        task = Task.objects.create(todolist_id=tdlist, description=request.POST.get('description'))
        task.save()
        data = {
            'id': task.id,
            'description': task.description
        }
        return JsonResponse(data)


def update_task(request):
    if request.method == 'POST' and request.is_ajax():
        task = Task.objects.get(id=request.POST.get('task_id'))
        task.description = request.POST.get('task_description')
        task.save()
        data = {
            'task_id': request.POST.get('task_id'),
            'task_description': request.POST.get('task_description')
        }
        return JsonResponse(data)


def delete_task(request):
    if request.method == 'POST' and request.is_ajax():
        task = Task.objects.get(id=request.POST.get('task_id'))
        task.delete()
        data = {
            'task_id': request.POST.get('task_id')
        }
        return JsonResponse(data)


def complete_task(request):
    if request.method == 'POST' and request.is_ajax():
        task = Task.objects.get(id=request.POST.get('task_id'))
        task.done = not task.done
        task.save()

        data = {
            'task_id': request.POST.get('task_id'),
            'task_complete': task.done
        }
        return JsonResponse(data)


def finish_list(request):
    if request.method == 'POST' and request.is_ajax():
        tdlist = TodoList.objects.get(id=request.POST.get('list_id'))
        tdlist.finished = True
        tdlist.completion_date = timezone.now()
        tdlist.save()
        return JsonResponse(data={}, status=200)
