from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(_('category name'), max_length=64, unique=True)


    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('product name'), max_length=64)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name=_('category'))
    description = models.CharField(_('product description'), max_length=4096)
    price = models.PositiveIntegerField(_('product price'))
    stock_amount = models.PositiveIntegerField(_('amount in stock'))


    class Meta:
        ordering = ['name', 'price', 'stock_amount']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(_('photo'), blank=True)


    class Meta:
        verbose_name = _('product picture')
        verbose_name_plural = _('product pictures')

    def __str__(self):
        return self.picture.name
