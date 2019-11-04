from accounts.models import Token
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Profile, Command

class ProfileInline(admin.StackedInline):
    model = Profile
    fields =['avatar', 'github', 'about_me']


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


class CommandProfileAdmin(admin.ModelAdmin):
    model = Command
    fields = ['user', 'project', 'created_at', 'end_at']

admin.site.register(Command)
admin.site.register(Token)
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
