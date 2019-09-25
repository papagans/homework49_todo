from webapp.models import Todo
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render, get_object_or_404, redirect


class IndexRedirectView(RedirectView):
   pattern_name = 'todo_index'


# def todo_index(request, *args, **kwargs):
#     todos = Todo.objects.all()
#     return render(request, 'index.html', context={
#         'todos': todos,
#     })


class MyTemplateView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = Todo.objects.all()
        return context

# class ArticleView(TemplateView):
#     template_name = 'view.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['article'] = get_object_or_404(, pk=kwargs['article_pk'])
#
#         return context
# Create your views here.
