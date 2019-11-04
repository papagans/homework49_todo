"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from webapp.views import TodoCreateView, TodoUpdateView, TodoDeleteView, \
#     StatusesView, TypesView, StatusUpdateView, TypeUpdateView, StatusDeleteView, \
#     StatusCreateView, TypeDeleteView, TypeCreateView, IndexView, TodoView, ProjectsView, ProjectView, ProjectCreateView, \
#     ProjectUpdateView, ProjectDeleteView, TodoForProjectCreateView
# from accounts.views import login_view, logout_view
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', IndexView.as_view(), name='todo_index'),
#     path('todo/<int:pk>/', TodoView.as_view(), name='todo_view'),
#     path('todo/add/', TodoCreateView.as_view(), name='todo_add'),
#     path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name='todo_update'),
#     path('todo/<int:pk>/delete/',  TodoDeleteView.as_view(), name='todo_delete'),
#     path('statuses/', StatusesView.as_view(), name='status'),
#     path('types/', TypesView.as_view(), name='type'),
#     path('status/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
#     path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type_update'),
#     path('status/<int:pk>/delete/',  StatusDeleteView.as_view(), name='status_delete'),
#     path('status/add/', StatusCreateView.as_view(), name='status_add'),
#     path('type/<int:pk>/delete/',  TypeDeleteView.as_view(), name='type_delete'),
#     path('type/add/', TypeCreateView.as_view(), name='type_add'),
#     path('projects/', ProjectsView.as_view(), name='project_index'),
#     path('projects/<int:pk>/', ProjectView.as_view(), name='project_view'),
#     path('project/add/', ProjectCreateView.as_view(), name='project_add'),
#     path('project/<int:pk>/delete/',  ProjectDeleteView.as_view(), name='project_delete'),
#     path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
#     path('project/<int:pk>/add-todo/', TodoForProjectCreateView.as_view(), name='project_todo_create'),
#     path('login', login_view, name='login'),
#     path('accounts/logout/', logout_view, name='logout')
# ]

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
urlpatterns = [
   path('admin/', admin.site.urls),
   path('accounts/', include('accounts.urls')),
   path('', include('webapp.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

