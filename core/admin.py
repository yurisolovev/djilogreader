from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Note, Log


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class NoteInline(admin.TabularInline):
    model = Note
    can_delete = True


class LogInline(admin.TabularInline):
    model = Log
    can_delete = True
    exclude = ['data']


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, NoteInline, LogInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Note)
admin.site.register(Log)
