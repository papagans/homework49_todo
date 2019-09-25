from django.db import models


class TypeChoice(models.Model):
    types = models.CharField(max_length=20, null=True, blank=True, verbose_name='Тип')

    def __str__(self):
        return self.types


class StatusChoice(models.Model):
    statuses = models.CharField(max_length=20, null=True, blank=True, verbose_name='Статус')

    def __str__(self):
        return self.statuses


class Todo(models.Model):
    summary = models.TextField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey(StatusChoice, related_name='status', on_delete=models.PROTECT, max_length=20)
    type = models.ForeignKey(TypeChoice, related_name='type', on_delete=models.PROTECT, max_length=20)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.summary
