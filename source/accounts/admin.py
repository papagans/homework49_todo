from accounts.models import Token
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import UserGitHub


# class UserInline(admin.StackedInline):
#     model = UserGitHub
#
#
# class UserAdmin(UserAdmin):
#     inlines = [UserInline]
#
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


admin.site.register(Token)
admin.site.register(UserGitHub)
