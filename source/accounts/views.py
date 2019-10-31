from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from main.settings import HOST_NAME
from accounts.forms import UserCreationForm, UserForm, PasswordChangeForm, UserGitHubForm
from accounts.models import Token, UserGitHub
from django.views.generic import DetailView, UpdateView, TemplateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def login_view(request):
    context = {}
    next = request.GET.get('next')
    redirect_page = request.session.setdefault('redirect_page', next)
    print(redirect_page)
    if redirect_page == None:
        redirect_page = '/'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_page)
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('webapp:todo_index')


def register_view(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                is_active=False  # user не активный до подтверждения email
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            # токен для активации, его сложнее угадать, чем pk user-а.
            token = Token.objects.create(user=user)
            activation_url = HOST_NAME + reverse('accounts:user_activate') + \
                             '?token={}'.format(token)

            # отправка письма на email пользователя
            user.email_user('Регистрация на сайте localhost',
                            'Для активации перейдите по ссылке: {}'.format(activation_url))

            return redirect("webapp:todo_index")
        else:
            return render(request, 'register.html', {'form': form})


def user_activate(request):
    token_value = request.GET.get('token')
    try:
        # найти токен
        token = Token.objects.get(token=token_value)

        # активировать пользователя
        user = token.user
        user.is_active = True
        user.save()

        # удалить токен, он больше не нужен
        token.delete()

        # войти
        login(request, user)

        # редирект на главную
        return redirect('webapp:todo_index')
    except Token.DoesNotExist:
        # если токена нет - сразу редирект
        return redirect('webapp:todo_index')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


# class UserEditView(UserPassesTestMixin, UpdateView):
#     model = User
#     template_name = 'user_update.html'
#     form_class = UserChangeForm
#     context_object_name = 'user_obj'
#
#     def test_func(self):
#         return self.get_object() == self.request.user
#
#     def get_success_url(self):
#         return reverse('accounts:detail', kwargs={'pk': self.object.pk})



class UserPasswordChangeView(UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def get_success_url(self):
        return reverse('accounts:login')


class UsersView(TemplateView):
    template_name = 'users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserGitHubForm(request.POST, instance=request.user.usergithub)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # messages.success(request, _('Your profile was successfully updated!'))
            return redirect('accounts:user_list')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserGitHubForm(instance=request.user.usergithub)
        print(user_form)
        print(profile_form)
    return render(request, 'user_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })