from django.contrib import admin
from django.utils.translation import gettext as _
from users.models import User

from .models import LiveOrder, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'address', 'amount', 'created_at', 'status')
    fieldsets = (
        (_('order info'), {
        'fields': (
            'user', 'product', 'address', 'amount',
            'status', 'created_at', 'completed_at', 'canceled_at')
        }),)

    list_filter = ('status',)
    readonly_fields = ['created_at', 'completed_at', 'canceled_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LiveOrder)
class LiveOrderAdmin(admin.ModelAdmin):
    change_list_template = 'admin/live_orders.djhtml'
    list_display = ('user', 'product', 'address', 'amount', 'created_at')
    def changelist_view(self, request, extra_context=None):
        all_fields = Order._meta.fields
        fields = [x.verbose_name for x in all_fields if x.name in self.list_display]

        return super().changelist_view(request, extra_context={'fields': fields})

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
