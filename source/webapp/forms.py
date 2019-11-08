from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import StatusChoice, TypeChoice, Todo, Project, User, Team


# class TodoForm(forms.Form):
#     summary = forms.CharField(max_length=40, label='Summary', required=True)
#     description = forms.CharField(max_length=3000, label='Description', required=True, widget=widgets.Textarea)
#     type = forms.ModelChoiceField(queryset=TypeChoice.objects.all(), label='Type')
#     status = forms.ModelChoiceField(queryset=StatusChoice.objects.all(), label='Status')


# class StatusForm(forms.Form):
#     status = forms.CharField(max_length=50, label=None)


# class TypeForm(forms.Form):
#     type = forms.CharField(max_length=50, label=None)

class TodoForm(forms.ModelForm):
    def __init__(self, assigned_to, **kwargs):
        super().__init__(**kwargs)
        print(assigned_to)
        self.fields['assigned_to'].queryset = User.objects.filter(id__in=assigned_to)

    # assigned_to = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Todo
        fields = ['summary', 'description', 'status', 'type', 'assigned_to']


class StatusForm(forms.ModelForm):
    class Meta:
        model = StatusChoice
        fields = ['statuses']


class TypeForm(forms.ModelForm):
    class Meta:
        model = TypeChoice
        fields = ['types']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


class ProjectTodoForm(forms.ModelForm):
    def __init__(self, assigned_to, **kwargs):
        super().__init__(**kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(id__in=assigned_to)
    #     self.fields['assigned_to'].queryset = assigned_to
    # assigned_to = forms.ModelChoiceField(queryset=Team.objects.all())

    class Meta:
        model = Todo
        fields = ['summary', 'description', 'status', 'type', 'assigned_to']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="")