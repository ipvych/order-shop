from django.contrib import admin
from django.utils.translation import gettext as _
from users.models import User

from .models import LiveOrder, Order

# Register your models here.


@admin.register(LiveOrder)
class LiveOrderAdmin(admin.ModelAdmin):
    change_list_template = 'admin/live_orders.djhtml'
    list_display = ('user', 'product', 'address', 'amount', 'created_at')

    def has_add_permission(self, request):
        return False



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'address', 'amount', 'created_at', 'status')
    fieldsets = (
        (_('order info'), {
        'fields': ('user', 'product', 'address',
                   'amount', 'status', 'created_at', 'completed_at', 'canceled_at')
        }),)

    list_filter = ('status',)
    readonly_fields = ['created_at', 'completed_at', 'canceled_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False
