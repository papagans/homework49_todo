from django.contrib import admin
from django.urls import path
from webapp.views import TodoCreateView, TodoUpdateView, TodoDeleteView, \
    StatusesView, TypesView, StatusUpdateView, TypeUpdateView, StatusDeleteView, \
    StatusCreateView, TypeDeleteView, TypeCreateView, IndexView, TodoView, ProjectsView, ProjectView, ProjectCreateView, \
    ProjectUpdateView, ProjectDeleteView, TodoForProjectCreateView


app_name ='webapp'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='todo_index'),
    path('todo/<int:pk>/', TodoView.as_view(), name='todo_view'),
    path('todo/add/', TodoCreateView.as_view(), name='todo_add'),
    path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name='todo_update'),
    path('todo/<int:pk>/delete/',  TodoDeleteView.as_view(), name='todo_delete'),
    path('statuses/', StatusesView.as_view(), name='status'),
    path('types/', TypesView.as_view(), name='type'),
    path('status/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type_update'),
    path('status/<int:pk>/delete/',  StatusDeleteView.as_view(), name='status_delete'),
    path('status/add/', StatusCreateView.as_view(), name='status_add'),
    path('type/<int:pk>/delete/',  TypeDeleteView.as_view(), name='type_delete'),
    path('type/add/', TypeCreateView.as_view(), name='type_add'),
    path('projects/', ProjectsView.as_view(), name='project_index'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('project/add/', ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/delete/',  ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/add-todo/', TodoForProjectCreateView.as_view(), name='project_todo_create'),
    path('todo/<int:pk>/add/', TodoCreateView.as_view(), name='todo_add'),
    ]