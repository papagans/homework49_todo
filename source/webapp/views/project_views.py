from webapp.models import Project
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from webapp.forms import ProjectForm, ProjectTodoForm
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator


class ProjectsView(ListView):
    context_object_name = 'project'
    model = Project
    template_name = 'projects/projects.html'
    ordering = ['-created_at']
    paginate_by = 5
    paginate_orphans = 1


class ProjectView(DetailView):
    template_name = 'projects/project_view.html'
    context_key = 'project'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectTodoForm()
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


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/project_create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    context_key = 'project'
    redirect_url = reverse_lazy('project_index')
    context_object_name = 'project'
    success_url = reverse_lazy('project_index')


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    context_object_name = 'project'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})
