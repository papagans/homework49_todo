from rest_framework import viewsets
from webapp.models import Project, Todo
from api_v2.serializers import ProjectSerializer, TodoSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer


class TodoViewSet(viewsets.ModelViewSet):
   queryset = Todo.objects.all()
   serializer_class = TodoSerializer