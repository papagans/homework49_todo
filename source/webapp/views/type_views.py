from webapp.models import TypeChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView,  UpdateView, DeleteView
from webapp.forms import TypeForm
from django.urls import reverse, reverse_lazy
# from .base import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from webapp.views.base import SessionMixin


class TypesView(SessionMixin, ListView):
    context_object_name = 'type'
    model = TypeChoice
    template_name = 'types/type.html'

    def get(self, request, *args, **kwargs):
        self.login_page(request)
        # self.request_path(self.request)
        print(request.session.items())
        return super().get(request, *args, **kwargs)


class TypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TypeChoice
    template_name = 'types/type_update.html'
    context_object_name = 'type'
    form_class = TypeForm

    def get_success_url(self):
        return reverse('webapp:type')

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:                  ПРИГОДИТСЯ!!!
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)


# class TypeUpdateView(UpdateView):
#     form_class = TypeForm
#     template_name = 'types/type_update.html'
#     # redirect_url = 'todos/todo_view.html'
#     model = TypeChoice                                    ПРИГОДИТСЯ
#     pk_url_kwarg = 'pk'
#     context_object_name = 'type'
#
#     def get_redirect_url(self):
#         return reverse('type')


class TypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TypeChoice
    template_name = 'types/type_delete.html'
    context_key = 'type'
    redirect_url = reverse_lazy('webapp:type')
    context_object_name = 'type'
    success_url = reverse_lazy('webapp:type')

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:             ПРИГОДИТСЯ
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)


# class TypeDeleteView(DeleteView):
#     template_name = 'types/type_delete.html'
#     # redirect_url = 'todos/todo_view.html'
#     model = TypeChoice
#     pk_url_kwarg = 'pk'                               ПРИГОДИТСЯ
#     context_object_name = 'type'
#     confirm_delete = True
#
#     def get_redirect_url(self):
#         return reverse('type')


class TypeCreateView(LoginRequiredMixin, CreateView):
    model = TypeChoice
    template_name = 'types/type_create.html'
    form_class = TypeForm

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:                 ПРИГОДИТСЯ
    #         return redirect('accounts:login')
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:type')
