# from views import Todo, StatusChoice, TypeChoice
# from django.views.generic import TemplateView, RedirectView, View
# from django.shortcuts import render, get_object_or_404, redirect
# from views import TodoForm, StatusForm, TypeForm
#
#
# class IndexRedirectView(RedirectView):
#    pattern_name = 'todo_index'
#
#
#
# class MyTemplateView(TemplateView):
#     template_name = 'todos/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['todos'] = Todo.objects.all()
#         return context
#
#
# class TodoView(TemplateView):
#     template_name = 'todos/todo_view.html'
#
#     def get_context_data(self, **kwargs):
#         pk = kwargs.get('pk')
#         context = super().get_context_data(**kwargs)
#         context['todo'] = get_object_or_404(Todo, pk=pk)
#         return context
#
#
# class TodoCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = TodoForm()
#         return render(request, 'todos/create.html', context={'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = TodoForm(data=request.POST)
#         if form.is_valid():
#             todo = Todo.objects.create(
#                 summary=form.cleaned_data['summary'],
#                 description=form.cleaned_data['description'],
#                 type=form.cleaned_data['type'],
#                 status=form.cleaned_data['status']
#             )
#             return redirect('todo_view', pk=todo.pk)
#         else:
#             return render(request, 'todos/create.html', context={'form': form})
#
#
# class TodoUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         todo = get_object_or_404(Todo, pk=pk)
#         form = TodoForm(data={'summary': todo.summary, 'description': todo.description, 'status': todo.status,
#                               'type': todo.type})
#         return render(request, 'todos/update.html', context={'form': form, 'todo': todo})
#
#     def post(self, request, *args, **kwargs):
#         form = TodoForm(data=request.POST)
#         pk = kwargs.get('pk')
#         todo = get_object_or_404(Todo, pk=pk)
#         if form.is_valid():
#             todo.summary = form.cleaned_data['summary']
#             todo.description = form.cleaned_data['description']
#             todo.status = form.cleaned_data['status']
#             todo.type = form.cleaned_data['type']
#             todo.save()
#             return redirect('todo_view', pk=todo.pk)
#         else:
#             return render(request, 'todos/update.html', context={'form': form, 'todo': todo.pk})
#
#
# class TodoDeleteView(View):
#     def get(self, request, pk):
#         todo = get_object_or_404(Todo, pk=pk)
#         return render(request, 'types/delete.html', context={'todo': todo})
#
#     def post(self, request, pk):
#         todo = get_object_or_404(Todo, pk=pk)
#         todo.delete()
#         return redirect('todo_index')
#
#
# class StatusesView(TemplateView):
#     template_name = 'statuses/status.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['status'] = StatusChoice.objects.all()
#         return context
#
#
# class StatusView(TemplateView):
#     template_name = 'statuses/status_view.html'
#
#     def get_context_data(self, **kwargs):
#         pk = kwargs.get('pk')
#         context = super().get_context_data(**kwargs)
#         context['status'] = get_object_or_404(StatusChoice, pk=pk)
#         return context
#
#
# class TypeView(TemplateView):
#     template_name = 'types/type.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['type'] = TypeChoice.objects.all()
#         return context
#
#
# class TypesView(TemplateView):
#     template_name = 'types/type_view.html'
#
#     def get_context_data(self, **kwargs):
#         pk = kwargs.get('pk')
#         context = super().get_context_data(**kwargs)
#         context['type'] = get_object_or_404(TypeChoice, pk=pk)
#         return context
#
#
# class StatusUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         status = get_object_or_404(StatusChoice, pk=pk)
#         form = StatusForm(data={'status': status.statuses})
#         return render(request, 'statuses/status_update.html', context={'form': form, 'status': status})
#
#     def post(self, request, *args, **kwargs):
#         form = StatusForm(data=request.POST)
#         pk = kwargs.get('pk')
#         todo = get_object_or_404(StatusChoice, pk=pk)
#         if form.is_valid():
#             todo.statuses = form.cleaned_data['status']
#             todo.save()
#             return redirect('status_view', pk=todo.pk)
#         else:
#             return render(request, 'statuses/status_update.html', context={'form': form, 'status': todo.pk})
#
#
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
#             return redirect('type_view', pk=todo.pk)
#         else:
#             return render(request, 'types/type_update.html', context={'form': form, 'type': todo.pk})
#
#
# class StatusDeleteView(View):
#     def get(self, request, pk):
#         status = get_object_or_404(StatusChoice, pk=pk)
#         return render(request, 'statuses/status_delete.html', context={'status': status})
#
#     def post(self, request, pk):
#         status = get_object_or_404(StatusChoice, pk=pk)
#         status.delete()
#         return redirect('status')
#
# class StatusCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = StatusForm()
#         return render(request, 'statuses/status_create.html', context={'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = StatusForm(data=request.POST)
#         if form.is_valid():
#             status = StatusChoice.objects.create(
#                 statuses=form.cleaned_data['status']
#             )
#             return redirect('status_view', pk=status.pk)
#         else:
#             return render(request, 'statuses/status_create.html', context={'form': form})
#
#
# class TypeDeleteView(View):
#     def get(self, request, pk):
#         type = get_object_or_404(TypeChoice, pk=pk)
#         return render(request, 'types/type_delete.html', context={'type': type})
#
#     def post(self, request, pk):
#         type = get_object_or_404(TypeChoice, pk=pk)
#         type.delete()
#         return redirect('type')
#
#
# class TypeCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = TypeForm()
#         return render(request, 'types/type_create.html', context={'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = TypeForm(data=request.POST)
#         if form.is_valid():
#             type = TypeChoice.objects.create(
#                 types=form.cleaned_data['type']
#             )
#             return redirect('type_view', pk=type.pk)
#         else:
#             return render(request, 'types/type_create.html', context={'form': form})
#
# # Create your views here.
