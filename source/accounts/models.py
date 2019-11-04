from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from webapp.models import Project


class Token(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             verbose_name='user', related_name='registration_tokens')
    token = models.UUIDField(verbose_name='Token', default=uuid4)

    def __str__(self):
        return str(self.token)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    about_me = models.TextField(null=True, blank=True, verbose_name='Обо мне')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    github = models.URLField(null=True, blank=True, verbose_name='Github')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Command(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Программист', related_name='command')
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.PROTECT)
    created_at = models.DateField(verbose_name='Дата начала работы')
    end_at = models.DateField(verbose_name='Дата окончания работы')


    def __str__(self):
        return str(self.user)