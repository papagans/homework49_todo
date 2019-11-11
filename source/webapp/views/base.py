from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime, date, timedelta
import time

class SessionMixin:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
    TIME_FORMAT = '%H:%M:%S.%f'
    page_visit_times = {}
    time_counter = {}

    def session_count(self, request, name):
        count = request.session.get(name, 0)
        request.session[name] = count + 1

    def session_time(self, request):
        start = datetime.now()
        request.session[request.path] = str(start)
        if len(self.time_counter) > 0:
            key_name = list(self.time_counter.keys())[0]
            prev_page_time = datetime.strptime(request.session[key_name], self.DATE_FORMAT)
            self.get_total_time(request, key_name, start, prev_page_time)
            self.time_counter.clear()
        self.time_counter.update({request.path: str(start)})

    def get_total_time(self, request, key, start, prev):
        result = start - prev
        if f'{key}_result' in request.session.keys():
            time = request.session[f'{key}_result'].split(' ')
            if len(time) > 1:
                time = time[1]
            old_time = datetime.strptime(time, self.TIME_FORMAT)
            old_time += result
            request.session[f'{key}_result'] = str(old_time)

        print(request.session.items())

            # print(request.session.items())
        # print(request.session.items())




        # print(request.path, 'REQUEST')
        # request.session[request] = str(now)
        # self.time_counter[request.path] = str(now)
        # print(self.time_counter)
        # print(request.session[request])


    def login_page(self, request):
        self.session_total_time(request)
        self.request = request
        self.visit_times()
        self.request.session['path'] = self.page_visit_times
        # print(request.session.get('path'), 'REQUESTION DICT PATH')


    def session_total_time(self, request):
        total1 = request.session.get('time_projects')
        total2 = request.session.get('time_index')

        # time1 = datetime.strptime(total1, self.DATE_FORMAT)
        # time2 = datetime.strptime(total2, self.DATE_FORMAT)
        # diff = time2 - time1

        if total1:
            time1 = datetime.strptime(total1, self.DATE_FORMAT)
            time2 = datetime.strptime(total2, self.DATE_FORMAT)
            diff = time2 - time1

        counter = 1

        time_counter = datetime.strptime(str(datetime.now()), self.DATE_FORMAT)
        # if self.request.path in self.time_counter.keys():
        #     self.time_counter[self.request.path] = diff.total_seconds()
        # if self.request.path not in self.page_visit_times.keys():
        #     self.time_counter[self.request.path] = time_counter

    def request_path(self, request):
        self.request = request

    def visit_times(self):
        counter = 1
        if self.request.path in self.page_visit_times.keys():
            self.page_visit_times[self.request.path] += 1
        if self.request.path not in self.page_visit_times.keys():
            self.page_visit_times[self.request.path] = counter
        # print(self.page_visit_times)

    def save_session(self):
        pass




        # name = request.path
        # print(name, "name path")
        #
        # path_list = {}
        # path_list[name] = count + 1
        # print(path_list, 'PATH_LIST')




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