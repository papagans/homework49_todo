from webapp.models import StatusChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, ListView
from webapp.forms import StatusForm



class StatusesView(ListView):
    context_object_name = 'status'
    model = StatusChoice
    template_name = 'statuses/status.html'


class StatusView(TemplateView):
    template_name = 'statuses/status_view.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['status'] = get_object_or_404(StatusChoice, pk=pk)
        return context


class StatusUpdateView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        status = get_object_or_404(StatusChoice, pk=pk)
        form = StatusForm(data={'status': status.statuses})
        return render(request, 'statuses/status_update.html', context={'form': form, 'status': status})

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        pk = kwargs.get('pk')
        todo = get_object_or_404(StatusChoice, pk=pk)
        if form.is_valid():
            todo.statuses = form.cleaned_data['status']
            todo.save()
            return redirect('status_view', pk=todo.pk)
        else:
            return render(request, 'statuses/status_update.html', context={'form': form, 'status': todo.pk})


class StatusDeleteView(View):
    def get(self, request, pk):
        status = get_object_or_404(StatusChoice, pk=pk)
        return render(request, 'statuses/status_delete.html', context={'status': status})

    def post(self, request, pk):
        status = get_object_or_404(StatusChoice, pk=pk)
        status.delete()
        return redirect('status')

class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'statuses/status_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        if form.is_valid():
            status = StatusChoice.objects.create(
                statuses=form.cleaned_data['status']
            )
            return redirect('status_view', pk=status.pk)
        else:
            return render(request, 'statuses/status_create.html', context={'form': form})


