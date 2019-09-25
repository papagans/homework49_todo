from django.contrib import admin

from webapp.models import Todo, TypeChoice, StatusChoice


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'date', 'statuses', 'types']
    list_filter = ['summary']
    search_fields = ['summary', 'description']
    fields = ['id', 'summary', 'description', 'date']
    readonly_fields = ['date']


class TypesAdmin(admin.ModelAdmin):
    list_display = ['types']
    # list_filter = ['summary']
    search_fields = ['types']
    fields = ['types']
    readonly_fields = ['']


class StatusesAdmin(admin.ModelAdmin):
    list_display = ['statuses']
    # list_filter = ['summary']
    search_fields = ['statuses']
    fields = ['statuses']
    readonly_fields = ['']


admin.site.register(Todo)
admin.site.register(StatusChoice)
admin.site.register(TypeChoice)
# admin.site.register(Status)
# Register your models here.
