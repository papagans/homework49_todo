from webapp.models import Todo
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView
from webapp.forms import TodoForm
from .base import DetailView, UpdateView, DeleteView
from django.urls import reverse


class IndexView(ListView):
    context_object_name = 'todos'
    model = Todo
    template_name = 'todos/index.html'
    ordering = ['-date']
    paginate_by = 5
    paginate_orphans = 1


class TodoView(DetailView):
    template_name = 'todos/todo_view.html'
    context_key = 'todo'
    model = Todo


class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todos/create.html'
    form_class = TodoForm

    def get_success_url(self):
        return reverse('todo_view', kwargs={'pk': self.object.pk})


class TodoDeleteView(DeleteView):
    template_name = 'todos/delete.html'
    # redirect_url = 'todos/todo_view.html'
    model = Todo
    pk_url_kwarg = 'pk'
    context_object_name = 'todo'
    confirm_delete = True

    def get_redirect_url(self):
        return reverse('todo_index')


class TodoUpdateView(UpdateView):
    form_class = TodoForm
    template_name = 'todos/update.html'
    # redirect_url = 'todos/todo_view.html'
    model = Todo
    pk_url_kwarg = 'pk'
    context_object_name = 'todo'

    def get_redirect_url(self):
        return reverse('todo_view', kwargs={'pk': self.object.pk})
