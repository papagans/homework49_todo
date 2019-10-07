from webapp.models import Todo
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView
from webapp.forms import TodoForm
from .base import DetailView, UpdateView
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


# class TodoUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         todo = get_object_or_404(Todo, pk=pk)
#         form = TodoForm(data={'summary': todo.summary, 'description': todo.description, 'status': todo.status,
#                               'type': todo.type})
#         return render(request, 'todos/update.html', context={'form': form, 'todo': todo})
#
#     def post(self, request, *args, **kwargs):
#         form = TodoForm(data=request.POST)
#         pk = kwargs.get('pk')
#         todo = get_object_or_404(Todo, pk=pk)
#         if form.is_valid():
#             todo.summary = form.cleaned_data['summary']
#             todo.description = form.cleaned_data['description']
#             todo.status = form.cleaned_data['status']
#             todo.type = form.cleaned_data['type']
#             todo.save()
#             return redirect('todo_view', pk=todo.pk)
#         else:
#             return render(request, 'todos/update.html', context={'form': form, 'todo': todo.pk})


class TodoDeleteView(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'types/delete.html', context={'todo': todo})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('todo_index')


class TodoUpdateView(UpdateView):
    form_class = TodoForm
    template_name = 'todos/update.html'
    # redirect_url = 'todos/todo_view.html'
    model = Todo
    pk_url_kwarg = 'pk'
    context_object_name = 'todo'

    def get_redirect_url(self):
        return reverse('todo_view', kwargs={'pk': self.object.pk})
