from webapp.models import Project, Todo
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'summary', 'description', 'status', 'type', 'date', 'updated_at', 'created_by', 'assigned_to')

class ProjectSerializer(serializers.ModelSerializer):
    project = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'status', 'project')

