from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('index')


@login_required
class MyLogoutView(TemplateView):
    template_name = 'registration/logout.html'


@login_required
def store_tasks_view(request):
    """
    View для отображения задач пользователя с ролью store.
    """
    if request.user.role != 'store':
        return redirect('role_redirect')  # Перенаправляем, если роль не store

    return render(request, 'users/store_index.html')


@login_required
def operator_tasks_view(request):
    """
    View для отображения задач для пользователей с ролью operator.
    """
    if request.user.role != 'operator':
        return redirect('role_redirect')  # Перенаправляем, если роль не operator

    return render(request, 'users/operator_index.html')


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
