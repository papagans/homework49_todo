from accounts.models import Token
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fields =['birth_date', 'avatar']


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.register(Token)
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
