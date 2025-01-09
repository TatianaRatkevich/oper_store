from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from task.models import Task


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('index')


@login_required
class MyLogoutView(TemplateView):
    template_name = 'registration/logout.html'


@login_required
def store_tasks_view(request):
    """
    View для отображения задач пользователя с ролью store с фильтрацией по дате.
    """
    if request.user.role != 'store':
        return redirect('role_redirect')  # Перенаправляем, если роль не store

    # Получение дат фильтрации из запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Фильтруем задачи по дате, если заданы start_date и end_date
    user = request.user
    tasks = Task.objects.filter(created_by=user)
    if start_date and end_date:
        tasks = tasks.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )

    tasks = tasks.order_by('-created_at')  # Сортировка от новых к старым

    return render(request, 'users/store_index.html', {
        'tasks': tasks,
        'start_date': start_date,
        'end_date': end_date
    })


@login_required
def operator_tasks_view(request):
    """
    View для отображения задач для пользователей с ролью operator.
    """
    if request.user.role != 'operator':
        return redirect('role_redirect')  # Перенаправляем, если роль не operator

    # Получение дат фильтрации из запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Фильтруем задачи по дате, если заданы start_date и end_date
    tasks = Task.objects.all()
    if start_date and end_date:
        tasks = tasks.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )

    tasks = tasks.order_by('created_at')  # Сортировка от новых к старым

    return render(request, 'users/operator_index.html', {
        'tasks': tasks,
        'start_date': start_date,
        'end_date': end_date
    })


@login_required
def role_based_redirect_view(request):
    """
    Редирект после логина в зависимости от роли пользователя.
    """
    if request.user.role == 'store':
        return redirect('store_index')
    elif request.user.role == 'operator':
        return redirect('operator_index')
    elif request.user.is_superuser:
        return redirect('admin/')


def index_view(request):
    """
    Главная страница: проверяет авторизацию пользователя и перенаправляет
    на страницу, соответствующую его роли. Если пользователь не залогинен,
    перенаправляет на страницу логина.
    """
    if not request.user.is_authenticated:
        return redirect('login')  # Редирект на страницу логина

    # Если пользователь залогинен, проверяем его роль
    if request.user.role == 'store':
        return redirect('store_index')  # Редирект для роли 'store'
    elif request.user.role == 'operator':
        return redirect('operator_index')  # Редирект для роли 'operator'
    elif request.user.is_superuser:
        return redirect('admin/')
