from django.contrib.auth.models import User

from webapp.models import Project, Todo, Team
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from webapp.forms import ProjectForm, ProjectTodoForm, SimpleSearchForm, TodoForm, ProjectAddUsersForm, KickUsersForm
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from webapp.views.base import SessionMixin
from datetime import datetime, date, timedelta

class ProjectsView(SessionMixin, ListView):
    context_object_name = 'project'
    model = Project
    template_name = 'projects/projects.html'
    ordering = ['-created_at']
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_query = self.get_search_query()
        # self.session_time(self.request)
        # self.request_path(request)
        self.login_page(request)
        # self.session_count(self.request, 'projects')
        self.session_time(self.request)
        # self.request.session.get('tie')
        # print(request.session.items())
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
                Q(name__icontains=self.search_query)
            )
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_query(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectView(DetailView):
    template_name = 'projects/project_view.html'
    context_key = 'project'
    model = Project

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        users = []
        project = pk
        teams = Team.objects.filter(project=project, end_at=None)
        for team in teams:
            users.append(team.user)
        context['teams'] = teams
        users = User.objects.filter(command__project=self.object)
        context["users"] = users
        context['form'] = ProjectTodoForm(assigned_to=users)
        project = context['project'].project.order_by('-date')
        self.paginate_comments_to_context(project, context)
        return context

    def paginate_comments_to_context(self, todos, context):
        paginator = Paginator(todos, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['todos'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/project_create.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project'
    permission_denied_message = 'Ну и какого хуя ты сюда лезешь?!'
    def form_valid(self, form):
        users = form.cleaned_data.pop('users')
        myself = self.request.user
        self.object = form.save()
        # user = self.request.user
        date = datetime.now()
        pk = self.object.pk
        for user in users:
            Team.objects.create(user=user, project=self.object, created_at=date)
        self.save_myself()
        return redirect('webapp:project_view', pk)

    def save_myself(self):
        pk = self.kwargs.get('pk')
        project = self.object
        user = self.request.user
        date = datetime.now()
        Team.objects.create(user=user, project=project, created_at=date)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')
        kwargs['project_pk'] = pk
        kwargs['my_self'] = self.request.user
        return kwargs


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    context_key = 'project'
    redirect_url = reverse_lazy('webapp:project_index')
    context_object_name = 'project'
    success_url = reverse_lazy('webapp:project_index')

    def change(self):
        pass


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    context_object_name = 'project'
    form_class = ProjectForm
    permission_required = 'webapp.edit_project'
    permission_denied_message = 'Ну и какого хуя ты сюда лезешь?!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields.pop('users')
        return form


    # def form_valid(self, form):
    #     users = form.cleaned_data.pop('users')
    #     self.object = form.save()
    #     # user = self.request.user
    #     date = datetime.now()
    #     pk = self.object.pk
    #     for user in users:
    #         Team.objects.create(user=user, project=self.object, created_at=date)
    #     # self.save_myself()
    #     return redirect('webapp:project_view', pk)

    # def save_myself(self):
    #     pk = self.kwargs.get('pk')
    #     project = self.object
    #     user = self.request.user
    #     date = datetime.now()
    #     Team.objects.create(user=user, project=project, created_at=date)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectAddUsers(PermissionRequiredMixin, CreateView):
    model = Team
    template_name = 'projects/project_add_users.html'
    form_class = ProjectAddUsersForm
    permission_required = 'webapp.add_team'
    permission_denied_message = 'Ну и какого хуя ты сюда лезешь?!'

    def form_valid(self, form):
        users = form.cleaned_data.pop('user')
        project = self.get_project()
        date = datetime.now()
        # pk = self.object.pk
        for user in users:
            Team.objects.create(user=user, project=project, created_at=date)
            # print(Team.objects.all().filter(project=pk), "Created TEAM")
        return redirect('webapp:project_view', project.pk)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project.objects.all().filter(id=pk))
        context['project'] = project
        return context

    def get_project(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)


class UserUpdateView(PermissionRequiredMixin, CreateView):
    model = Team
    template_name = 'projects/user_kick.html'
    # context_object_name = 'project'
    form_class = KickUsersForm
    permission_required = 'webapp.add_team'
    permission_denied_message = 'Ну и какого хуя ты сюда лезешь?!'

    def form_valid(self, form):
        users = form.cleaned_data.pop('user')

        project = self.get_project()
        print(users, "users")
        print(project, "PROJECT")
        date = datetime.now()
        print(date)
        # pk = self.object.pk
        for user in users:
            print('user: ', user.id)
            Team.objects.filter(user=user.user, project=project).update(end_at=date)
        return redirect('webapp:project_view', project.pk)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project.objects.all().filter(id=pk))
        context['project'] = project
        # context['form'] = KickUsersForm(project.pk)
        return context

    def get_project(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Project, pk=pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')
        kwargs['project_pk'] = pk
        kwargs['my_self'] = self.request.user
        return kwargs
