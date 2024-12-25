from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(max_length=180, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks_created'
    )
    processed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_processed'
    )

    def __str__(self):
        return f'Task {self.id} - {self.status}'

    def assign_to_operator(self, operator):
        """
        Назначьте задачу оператору и измените статус на 'in_progress'.
        """
        if self.status != 'pending':
            raise ValidationError("Назначать можно только задачи со статусом 'pending'.")
        if operator.role != 'operator':
            raise ValidationError("Только пользователи с ролью 'operator' могут обрабатывать задачи.")
        self.processed_by = operator
        self.status = 'in_progress'
        self.save()

    def mark_as_completed(self):
        """
        Пометить задачу как выполненную.
        """
        if self.status != 'in_progress':
            raise ValidationError("Только задачи со статусом 'in_progress' могут быть завершены.")
        self.status = 'completed'
        self.processed_by = None
        self.save()

    def mark_as_rejected(self):
        """
        Пометить задачу как отклоненную.
        """
        if self.status != 'in_progress':
            raise ValidationError("Только задачи со статусом 'in_progress' могут быть отклонены.")
        self.status = 'rejected'
        self.processed_by = None
        self.save()

    def return_to_pending(self):
        """
        Вернуть задачу в статус ожидания.
        """
        if self.status != 'in_progress':
            raise ValidationError("Только задачи со статусом 'in_progress' могут быть возвращены в ожидание.")
        self.status = 'pending'
        self.processed_by = None
        self.save()


class Image(models.Model):
    task = models.ForeignKey(Task, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True, upload_to='images/')

    def __str__(self):
        return f'Image {self.id} for Task {self.task.id}'
