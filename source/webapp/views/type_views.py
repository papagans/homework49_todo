from webapp.models import TypeChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView
from webapp.forms import TypeForm
from django.urls import reverse
from .base import UpdateView


class TypesView(ListView):
    context_object_name = 'type'
    model = TypeChoice
    template_name = 'types/type.html'


class TypeUpdateView(UpdateView):
    form_class = TypeForm
    template_name = 'types/type_update.html'
    # redirect_url = 'todos/todo_view.html'
    model = TypeChoice
    pk_url_kwarg = 'pk'
    context_object_name = 'type'

    def get_redirect_url(self):
        return reverse('type')


# class TypeUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         type = get_object_or_404(TypeChoice, pk=pk)
#         form = TypeForm(data={'type': type.types})
#         return render(request, 'types/type_update.html', context={'form': form, 'type': type})
#
#     def post(self, request, *args, **kwargs):
#         form = TypeForm(data=request.POST)
#         pk = kwargs.get('pk')
#         todo = get_object_or_404(TypeChoice, pk=pk)
#         if form.is_valid():
#             todo.types = form.cleaned_data['type']
#             todo.save()
#             return redirect('type')
#         else:
#             return render(request, 'types/type_update.html', context={'form': form, 'type': todo.pk})


class TypeDeleteView(View):
    def get(self, request, pk):
        type = get_object_or_404(TypeChoice, pk=pk)
        return render(request, 'types/type_delete.html', context={'type': type})

    def post(self, request, pk):
        type = get_object_or_404(TypeChoice, pk=pk)
        type.delete()
        return redirect('type')


class TypeCreateView(CreateView):
    model = TypeChoice
    template_name = 'types/type_create.html'
    form_class = TypeForm

    def get_success_url(self):
        return reverse('type')
