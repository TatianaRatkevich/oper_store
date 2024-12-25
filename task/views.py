from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import TaskForm
from .models import Image


@login_required
def create_task(request):
    if request.user.role != 'store':
        messages.error(request, 'Только магазины могут создавать задачи.')
        return redirect('role_redirect')  # Перенаправление в случае отсутствия прав

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.created_by = request.user
            task.save()

            images = request.FILES.getlist('images')  # Получаем все загруженные изображения
            for img in images:
                Image.objects.create(task=task, image=img)

            messages.success(request, 'Задача успешно создана.')
            return redirect('store_index')  # Перенаправление после успешного создания задачи
    else:
        task_form = TaskForm()

    context = {'task_form': task_form}
    return render(request, 'task/create_task.html', context)
