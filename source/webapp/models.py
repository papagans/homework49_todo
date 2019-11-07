from django.contrib.auth.models import User
from django.db import models

project_status = (
    ('active', 'Активный'),
    ('closed', 'Закрыт'),
)

class Counter(models.Model):
    counter = models.BigIntegerField(null=False, blank=False, verbose_name='Счетчик')

    def __str__(self):
        return str(self.counter)


class TypeChoice(models.Model):
    types = models.CharField(max_length=20, null=False, blank=False, verbose_name='Тип')

    def __str__(self):
        return self.types


class StatusChoice(models.Model):
    statuses = models.CharField(max_length=20, null=False, blank=False, verbose_name='Статус')

    def __str__(self):
        return self.statuses


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')
    status = models.CharField(max_length=20, default=project_status[0][0], verbose_name='Status',
                              choices=project_status)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo = None

    def __str__(self):
        return self.name


class Todo(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey(StatusChoice, related_name='status', on_delete=models.PROTECT, max_length=20)
    type = models.ForeignKey(TypeChoice, related_name='type', on_delete=models.PROTECT, max_length=20)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    project = models.ForeignKey(Project, null=True, blank=False, on_delete=models.PROTECT, max_length=50,
                                related_name='project', verbose_name='Проект')
    created_by = models.ForeignKey(User, null=True, blank=True, default=None, verbose_name='Автор',
                               on_delete=models.CASCADE, related_name='user_created')
    assigned_to = models.ForeignKey(User, null=True, blank=True, default=None, verbose_name='Исполнитель',
                               on_delete=models.CASCADE, related_name='user_assigned')

    def __str__(self):
        return self.summary


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Программист', related_name='command')
    project = models.ForeignKey(Project, related_name='teams', verbose_name='Проект', on_delete=models.PROTECT)
    created_at = models.DateField(verbose_name='Дата начала работы')
    end_at = models.DateField(verbose_name='Дата окончания работы')

    def __str__(self):
        return str(self.user)

