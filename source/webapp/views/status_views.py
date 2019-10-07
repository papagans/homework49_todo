from webapp.models import StatusChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView
from webapp.forms import StatusForm
from django.urls import reverse
from .base import UpdateView, DeleteView


class StatusesView(ListView):
    context_object_name = 'status'
    model = StatusChoice
    template_name = 'statuses/status.html'

class StatusUpdateView(UpdateView):
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    # redirect_url = 'todos/todo_view.html'
    model = StatusChoice
    pk_url_kwarg = 'pk'
    context_object_name = 'status'

    def get_redirect_url(self):
        return reverse('status')


class StatusDeleteView(DeleteView):
    template_name = 'statuses/status_delete.html'
    # redirect_url = 'todos/todo_view.html'
    model = StatusChoice
    pk_url_kwarg = 'pk'
    context_object_name = 'status'
    confirm_delete = True

    def get_redirect_url(self):
        return reverse('status')


class StatusCreateView(CreateView):
    model = StatusChoice
    template_name = 'statuses/status_create.html'
    form_class = StatusForm

    def get_success_url(self):
        return reverse('status')



