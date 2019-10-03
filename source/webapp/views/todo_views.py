from webapp.models import Todo
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from webapp.forms import TodoForm

# class IndexRedirectView(RedirectView):
#    pattern_name = 'todo_index'


class MyTemplateView(TemplateView):
    template_name = 'todos/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = Todo.objects.all()
        return context


class TodoView(TemplateView):
    template_name = 'todos/todo_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['todo'] = get_object_or_404(Todo, pk=pk)
        return context


class TodoCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TodoForm()
        return render(request, 'todos/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = TodoForm(data=request.POST)
        if form.is_valid():
            todo = Todo.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                type=form.cleaned_data['type'],
                status=form.cleaned_data['status']
            )
            return redirect('todo_view', pk=todo.pk)
        else:
            return render(request, 'todos/create.html', context={'form': form})


class TodoUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        todo = get_object_or_404(Todo, pk=pk)
        form = TodoForm(data={'summary': todo.summary, 'description': todo.description, 'status': todo.status,
                              'type': todo.type})
        return render(request, 'todos/update.html', context={'form': form, 'todo': todo})

    def post(self, request, *args, **kwargs):
        form = TodoForm(data=request.POST)
        pk = kwargs.get('pk')
        todo = get_object_or_404(Todo, pk=pk)
        if form.is_valid():
            todo.summary = form.cleaned_data['summary']
            todo.description = form.cleaned_data['description']
            todo.status = form.cleaned_data['status']
            todo.type = form.cleaned_data['type']
            todo.save()
            return redirect('todo_view', pk=todo.pk)
        else:
            return render(request, 'todos/update.html', context={'form': form, 'todo': todo.pk})


class TodoDeleteView(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'types/delete.html', context={'todo': todo})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('todo_index')