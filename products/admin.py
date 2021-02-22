from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from .models import ProductCategory, Product, ProductPicture
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductPictureInline(admin.TabularInline):
    model = ProductPicture
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.picture:
            print(obj.picture.url)
            return mark_safe('<a href="{0}"><img src="{0}" width="150" height="150" style="object-fit:contain" /></a>'.format(obj.picture.url))
        else:
            return ''


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPictureInline,]
    list_display = ('name', 'category', 'price', 'stock_amount')
    search_fields = ('name', 'category', 'price', 'stock_amount')
    list_filter = ('category__name',)



admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
