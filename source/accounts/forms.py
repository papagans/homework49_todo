from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import Profile
import re


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username', required=True)
    password = forms.CharField(max_length=100, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, label='Password Confirm', required=True,
                                       widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('User with this email already exists',
                                  code='user_email_exists')
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('User with this username already exists',
                                  code='user_username_exists')
        except User.DoesNotExist:
            return username

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('Passwords do not match',
                                  code='passwords_do_not_match')
        return self.cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserChForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'about_me', 'github')

    def clean_github(self):
        github = self.cleaned_data['github']
        if github:
            git = re.match("https://github.com/", github)
            if git:
                print(github, 'it works!!!')
            else:
                raise forms.ValidationError('Введенна ссылка не является ссылкой на Github')
        # return github
        else:
            raise forms.ValidationError('Вы ввели пустую ссылку')
        return github


class UserChangeForm(forms.ModelForm):

    avatar = forms.ImageField(label='Аватар', required=False)
    about_me = forms.CharField(label='О себе', required=False, widget=forms.Textarea(), max_length=200)
    github = forms.URLField(label='Github', required=False)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)

        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit=commit)
        self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        profile.avatar = self.cleaned_data.get('avatar', None)
        profile.about_me = self.cleaned_data.get('about_me', None)
        profile.github = self.cleaned_data.get('github', None)

        # self.instance.profile = profile
        if commit:
            profile.save()


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'about_me', 'github']
        profile_fields = ['avatar', 'about_me', 'github']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}




class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']

