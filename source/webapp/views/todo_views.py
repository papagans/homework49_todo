from django.contrib.auth.models import User

from webapp.models import Todo, Project, Counter, Team
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from webapp.forms import TodoForm, ProjectTodoForm, SimpleSearchForm
# from .base import DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        self.search_query = self.get_search_query()
        # count = self.count()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        count = self.count()
        context['count'] = count
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

    def count(self):
        counter = get_object_or_404(Counter, pk=1)
        print(counter)
        counter.counter += 1
        counter.save()
        return counter


class TodoView(DetailView):
    template_name = 'todos/todo_view.html'
    context_key = 'todo'
    model = Todo
    # form_class = TodoForm
    #
    # def get_form(self, form_class=TodoForm):
    #     form = super().get_form()
    #     user = self.request.user
    #     form.fields['created_by'].queryset = User.objects.all().filter(user=user)
    #     return form


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todos/create.html'
    form_class = TodoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')
        users = []
        project = Project.objects.get(pk=pk)
        # project = Project.objects.get(project__pk=task.pk)
        teams = Team.objects.filter(project=project)
        for team in teams:
            users.append(team.user.pk)
        kwargs['assigned_to'] = users
        return kwargs

    # def get_form(self, form_class=None):
    #     form = super().get_form()
    #     pk = self.kwargs.get('pk')
    #     form.fields['created_by'].initial = pk
    #     # print(task_pk)
    #     # form.fields['created_by'].initial = user
    #     form.fields['project'].initial = Project.objects.get(pk=pk)
    #     return form


    def get_project(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)

    def form_valid(self, form):
        project = self.get_project()
        pk = self.kwargs.get('pk')
        issue = project.project.create(**form.cleaned_data)
        issue.created_by = self.request.user
        issue.project.pk = pk
        issue.save()
        return redirect('webapp:project_index')

    #
    # def test_func(self):
    #     users = []
    #     task_pk = self.kwargs.get('pk')
    #     task = Todo.objects.get(pk=task_pk)
    #     project = Project.objects.get(project__pk=task.pk)
    #     teams = Team.objects.all().filter(project=project)
    #     print(Project.objects.get(pk=1))
    #     print(Project.objects.get(pk=1).project.all())
    #     # print(teams)
    #     for team in teams:
    #         users.append(team.user.pk)
    #         # print(team.user.pk)
    #     return self.request.user.pk in users


    def get_success_url(self):
        return reverse('webapp:todo_view', kwargs={'pk': self.object.pk})


class TodoDeleteView(UserPassesTestMixin, DeleteView):
    model = Todo
    template_name = 'todos/delete.html'
    context_key = 'todo'
    redirect_url = reverse_lazy('webapp:todo_index')
    context_object_name = 'todo'
    success_url = reverse_lazy('webapp:todo_index')

    def test_func(self):
        users = []
        task_pk = self.kwargs.get('pk')
        task = Todo.objects.get(pk=task_pk)
        project = Project.objects.get(project__pk=task.pk)
        teams = Team.objects.all().filter(project=project)
        # print(teams)
        for team in teams:
            users.append(team.user.pk)
            # print(team.user.pk)
        return self.request.user.pk in users
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)


class TodoUpdateView(UserPassesTestMixin, UpdateView):
    model = Todo
    template_name = 'todos/update.html'
    context_object_name = 'todo'
    form_class = TodoForm

    def form_valid(self, form):
        # project = self.kwargs.get('pk')
        # print(project)
        form.instance.created_by = self.request.user
        # form.fields['project'].initial = project

        # print(project)
        return super().form_valid(form)

    def get_form_kwargs(self):
        # project = self.kwargs.get('pk')
        kwargs = super().get_form_kwargs()
        kwargs['created_by'] = self.request.user
        # kwargs['project'] = self.kwargs.get('pk')
        return kwargs

    def test_func(self):
        users = []
        task_pk = self.kwargs.get('pk')
        task = Todo.objects.get(pk=task_pk)
        project = Project.objects.get(project__pk=task.pk)
        print(project)
        teams = Team.objects.all().filter(project=project)
        print(teams)
        for team in teams:
            users.append(team.user.pk)
            print(team.user.pk)
        return self.request.user.pk in users
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:todo_view', kwargs={'pk': self.object.pk})


class TodoForProjectCreateView(UserPassesTestMixin, CreateView):
    model = Todo
    template_name = 'todos/create.html'
    form_class = ProjectTodoForm

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = self.get_project()
        pk = self.kwargs.get('pk')
        issue = project.project.create(**form.cleaned_data)
        issue.created_by = self.request.user
        issue.project.pk = pk
        issue.save()
        return redirect('webapp:project_index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')
        users = []
        project = Project.objects.get(pk=pk)
        # project = Project.objects.get(project__pk=task.pk)
        teams = Team.objects.filter(project=project)
        for team in teams:
            users.append(team.user.pk)

        kwargs['assigned_to'] = users
        return kwargs

    def test_func(self):
        user = self.request.user.pk
        # print(user)
        users = []
        project = self.kwargs.get('pk')
        # print(project)
        teams = Team.objects.all().filter(project=project)
        for team in teams:
            users.append(team.user.pk)
            print(team.user.pk)
        print(users)
        print(teams, 'USER in TEAM')
        # print(projects)
        # form.fields['project'].queryset = Project.objects.all().filter(name__in=projects)

        return self.request.user.pk in users

    def get_success_url(self):
        return reverse('webapp:todo_view', kwargs={'pk': self.object.pk})

    def get_project(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)
    # def get_form(self, form_class=None):
    #     form = super().get_form()
    #     # project_test = Project.objects.get(pk=1)
    #     # print(project_test.teams.all())
    #     user = self.request.user
    #     projects = []
    #     teams = Team.objects.all().filter(user=user)
    #     for team in teams:
    #         projects.append(team.project.name)
    #     print(teams, 'USER in TEAM')
    #     form.fields['project'].queryset = Project.objects.all().filter(name__in=projects)
    #     # print(userpk)
    #     return form
# class TodoUpdateView(UpdateView):
#     form_class = TodoForm
#     template_name = 'todos/update.html'
#     # redirect_url = 'todos/todo_view.html'
#     model = Todo
#     pk_url_kwarg = 'pk'
#     context_object_name = 'todo'
# #
#     def get_redirect_url(self):
#         return reverse('todo_view', kwargs={'pk': self.object.pk})
