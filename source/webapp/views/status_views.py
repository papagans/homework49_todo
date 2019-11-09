from webapp.models import StatusChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from webapp.forms import StatusForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from webapp.views.base import SessionMixin



class StatusesView(SessionMixin, ListView):
    context_object_name = 'status'
    model = StatusChoice
    template_name = 'statuses/status.html'

    def get(self, request, *args, **kwargs):
        self.login_page(request)
        # self.request_path(self.request)
        # print(request.session.items())
        return super().get(request, *args, **kwargs)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = StatusChoice
    template_name = 'statuses/status_update.html'
    context_object_name = 'status'
    form_class = StatusForm


    def get_success_url(self):
        return reverse('webapp:status')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = StatusChoice
    template_name = 'statuses/status_delete.html'
    context_key = 'status'
    redirect_url = reverse_lazy('webapp:status')
    context_object_name = 'status'
    success_url = reverse_lazy('webapp:status')

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = StatusChoice
    template_name = 'statuses/status_create.html'
    form_class = StatusForm

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:status')



