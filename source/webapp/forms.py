from django import forms
from django.forms import widgets
from webapp.models import StatusChoice, TypeChoice


class TodoForm(forms.Form):
    summary = forms.CharField(max_length=40, label='Summary', required=True)
    description = forms.CharField(max_length=3000, label='Description', required=True, widget=widgets.Textarea)
    type = forms.ModelChoiceField(queryset=TypeChoice.objects.all(), label='Type')
    status = forms.ModelChoiceField(queryset=StatusChoice.objects.all(), label='Status')


# class StatusForm(forms.Form):
#     status = forms.ModelChoiceField(queryset=StatusChoice.objects.all(), label=None)


# class TypeForm(forms.Form):
#     type = forms.ModelChoiceField(queryset=TypeChoice.objects.all(), label=None)

