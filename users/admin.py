from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email',]
    fieldsets = (
        (_('User info'), {
            'fields': ('phone', 'email', 'first_name', 'last_name')
            }),)

    readonly_fields = fieldsets[0][1]['fields']
    ordering = ['first_name', 'last_name', 'phone', 'email']

admin.site.unregister(Group)
