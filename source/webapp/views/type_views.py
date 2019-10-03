from webapp.models import TypeChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView
from webapp.forms import TypeForm


class TypesView(ListView):
    context_object_name = 'type'
    model = TypeChoice
    template_name = 'types/type.html'


class TypeUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        type = get_object_or_404(TypeChoice, pk=pk)
        form = TypeForm(data={'type': type.types})
        return render(request, 'types/type_update.html', context={'form': form, 'type': type})

    def post(self, request, *args, **kwargs):
        form = TypeForm(data=request.POST)
        pk = kwargs.get('pk')
        todo = get_object_or_404(TypeChoice, pk=pk)
        if form.is_valid():
            todo.types = form.cleaned_data['type']
            todo.save()
            return redirect('type')
        else:
            return render(request, 'types/type_update.html', context={'form': form, 'type': todo.pk})


class TypeDeleteView(View):
    def get(self, request, pk):
        type = get_object_or_404(TypeChoice, pk=pk)
        return render(request, 'types/type_delete.html', context={'type': type})

    def post(self, request, pk):
        type = get_object_or_404(TypeChoice, pk=pk)
        type.delete()
        return redirect('type')


class TypeCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TypeForm()
        return render(request, 'types/type_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = TypeForm(data=request.POST)
        if form.is_valid():
            type = TypeChoice.objects.create(
                types=form.cleaned_data['type']
            )
            return redirect('type')
        else:
            return render(request, 'types/type_create.html', context={'form': form})