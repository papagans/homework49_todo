from webapp.models import Todo, Project
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from webapp.forms import TodoForm, ProjectTodoForm, SimpleSearchForm
# from .base import DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.db.models import Q

class IndexView(ListView):
    context_object_name = 'todos'
    model = Todo
    template_name = 'todos/index.html'
    ordering = ['-date']
    paginate_by = 5
    paginate_orphans = 1

    def query(self):
        pass

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        print(self.form)
        self.search_query = self.get_search_query()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.search_query:
            context['query'] = urlencode({'search': self.search_query})
        context['form'] = self.form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_query:
            queryset = queryset.filter(
                Q(description__icontains=self.search_query)
                | Q(summary__icontains=self.search_query)
            )
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_query(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


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
    model = Todo
    template_name = 'todos/delete.html'
    context_key = 'todo'
    redirect_url = reverse_lazy('todo_index')
    context_object_name = 'todo'
    success_url = reverse_lazy('todo_index')


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = 'todos/update.html'
    context_object_name = 'todo'
    form_class = TodoForm

    def get_success_url(self):
        return reverse('todo_view', kwargs={'pk': self.object.pk})


class TodoForProjectCreateView(CreateView):
    template_name = 'todos/create.html'
    form_class = ProjectTodoForm

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        project.project.create(**form.cleaned_data)
        return redirect('project_view', pk=project_pk)
# class TodoUpdateView(UpdateView):
#     form_class = TodoForm
#     template_name = 'todos/update.html'
#     # redirect_url = 'todos/todo_view.html'
#     model = Todo
#     pk_url_kwarg = 'pk'
#     context_object_name = 'todo'
#
#     def get_redirect_url(self):
#         return reverse('todo_view', kwargs={'pk': self.object.pk})
