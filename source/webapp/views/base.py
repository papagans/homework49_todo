from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect


class DetailView(TemplateView):
    context_key = 'objects'
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        context[self.context_key] = get_object_or_404(self.model, pk=pk)
        return context


#
# class TypeUpdateView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         type_pk = kwargs.get('pk')
#         type = get_object_or_404(Type, pk=type_pk)
#         form = TypeForm(data={
#             'type': type.type,
#         })
#         return render(request, 'type_update.html', context={
#             'form': form,
#             'type': type
#
#         })
#
#     def post(self, request, *args, **kwargs):
#         form = TypeForm(data=request.POST)
#         type_pk = kwargs.get('pk')
#         type = get_object_or_404(Type, pk=type_pk)
#         if form.is_valid():
#             type.type = form.cleaned_data['type']
#             type.save()
#
#             return redirect('type_index')
#         else:
#             return render(request, 'type_update.html', context={
#                 'form': form,
#                 'type': type,
#             })


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