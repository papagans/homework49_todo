from django.shortcuts import render
from webapp.models import Todo


def todo_index(request, *args, **kwargs):
    todos = Todo.objects.all()
    return render(request, 'todo_index.html', context={
        'todos': todos,
    })
# Create your views here.
