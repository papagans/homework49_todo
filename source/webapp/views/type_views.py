from webapp.models import TypeChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView
from webapp.forms import TypeForm
from django.urls import reverse
from .base import UpdateView, DeleteView


class TypesView(ListView):
    context_object_name = 'type'
    model = TypeChoice
    template_name = 'types/type.html'


class TypeUpdateView(UpdateView):
    form_class = TypeForm
    template_name = 'types/type_update.html'
    # redirect_url = 'todos/todo_view.html'
    model = TypeChoice
    pk_url_kwarg = 'pk'
    context_object_name = 'type'

    def get_redirect_url(self):
        return reverse('type')


class TypeDeleteView(DeleteView):
    template_name = 'types/type_delete.html'
    # redirect_url = 'todos/todo_view.html'
    model = TypeChoice
    pk_url_kwarg = 'pk'
    context_object_name = 'type'
    confirm_delete = True

    def get_redirect_url(self):
        return reverse('type')


class TypeCreateView(CreateView):
    model = TypeChoice
    template_name = 'types/type_create.html'
    form_class = TypeForm

    def get_success_url(self):
        return reverse('type')
