from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime, date, timedelta
import time

class SessionMixin:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    def session_count(self, request, name):
        count = request.session.get(name, 0)
        request.session[name] = count + 1

    def session_time(self, request, time_session):
        now = datetime.today()
        request.session[time_session] = str(now)

    def session_total_time(self,request):
        total1 = request.session.get('time_project')
        total2 = request.session.get('time_index')

        if total1:
            time1 = datetime.strptime(total1, self.DATE_FORMAT)
            time2 = datetime.strptime(total2, self.DATE_FORMAT)
            diff = time2 - time1
            print(diff.total_seconds())


class DetailView(TemplateView):
    context_key = 'objects'
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        context[self.context_key] = get_object_or_404(self.model, pk=pk)
        return context


class UpdateView(View):
    form_class = None
    template_name = None
    redirect_url = ''
    model = None
    pk_url_kwarg = 'pk'
    context_object_name = None

    def get(self, request, *args, **kwargs):
        self.object = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=self.object)
        context = {'form': form, self.context_object_name: self.object}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.object = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=self.object, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_redirect_url(self):
        return self.redirect_url

    def form_valid(self, form):
        form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={'form': form})


class DeleteView(View):
    template_name = None
    redirect_url = ''
    model = None
    pk_url_kwarg = 'pk'
    context_object_name = None
    confirm_delete = False

    def get(self, request, *args, **kwargs):
        if self.confirm_delete:
            self.object = self.model.objects.get(id=kwargs['pk'])
            context = {self.context_object_name: self.object}
            return render(request, self.template_name, context)
        else:
            self.object = self.model.objects.get(id=kwargs['pk'])
            self.object.delete()
            return redirect(self.get_redirect_url())
    def post(self, request, *args, **kwargs):
        self.object = self.model.objects.get(id=kwargs['pk'])
        self.object.delete()
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return self.redirect_url

# class TodoDeleteView(View):
#     def get(self, request, pk):
#         todo = get_object_or_404(Todo, pk=pk)
#         return render(request, 'types/delete.html', context={'todo': todo})
#
#     def post(self, request, pk):
#         todo = get_object_or_404(Todo, pk=pk)
#         todo.delete()
#         return redirect('todo_index')