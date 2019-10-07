from webapp.models import StatusChoice
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView
from webapp.forms import StatusForm
from django.urls import reverse


class StatusesView(ListView):
    context_object_name = 'status'
    model = StatusChoice
    template_name = 'statuses/status.html'


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
            return redirect('status')
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


class StatusCreateView(CreateView):
    model = StatusChoice
    template_name = 'statuses/status_create.html'
    form_class = StatusForm

    def get_success_url(self):
        return reverse('status')



