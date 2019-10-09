from webapp.models import StatusChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from webapp.forms import StatusForm
from django.urls import reverse, reverse_lazy


class StatusesView(ListView):
    context_object_name = 'status'
    model = StatusChoice
    template_name = 'statuses/status.html'


class StatusUpdateView(UpdateView):
    model = StatusChoice
    template_name = 'statuses/status_update.html'
    context_object_name = 'status'
    form_class = StatusForm

    def get_success_url(self):
        return reverse('status')


class StatusDeleteView(DeleteView):
    model = StatusChoice
    template_name = 'statuses/status_delete.html'
    context_key = 'status'
    redirect_url = reverse_lazy('status')
    context_object_name = 'status'
    success_url = reverse_lazy('status')


class StatusCreateView(CreateView):
    model = StatusChoice
    template_name = 'statuses/status_create.html'
    form_class = StatusForm

    def get_success_url(self):
        return reverse('status')



