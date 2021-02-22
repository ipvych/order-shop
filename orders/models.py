from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from products.models import Product


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    address = models.CharField(_('order address'), max_length=128)
    amount = models.PositiveIntegerField(_('order amount'), validators=[MinValueValidator(1)])
    __original_amount = None

    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    ORDER_STATUS_CHOICES = (
        (CANCELED, _('Canceled')),
        (COMPLETED, _('Completed')),
        (PENDING, _('Pending')),
    )
    status = models.CharField(
        _('order status'),
        default='pending',
        choices=ORDER_STATUS_CHOICES,
        max_length=16,
    )

    created_at = models.DateTimeField(_('order date'), auto_now_add=True)
    completed_at = models.DateTimeField(_('completion date'), null=True, blank=True)
    canceled_at = models.DateTimeField(_('cancel date'), null=True, blank=True)


    class Meta:
        ordering = [
            'created_at', 'canceled_at', 'completed_at', 'address',
            'amount', 'status'
        ]
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.product.stock_amount -= self.amount
            self.product.save()
            return super().save(*args, **kwargs)

        if self.status == self.COMPLETED:
            self.completed_at = timezone.now()
        if self.status == self.CANCELED:
            self.canceled_at = timezone.now()
            self.product.stock_amount += self.amount
            self.product.save()

        if self.__original_amount != self.amount:
            if self.amount > self.__original_amount:
                self.product.stock_amount -= (self.amount - self.__original_amount)
            else:
                self.product.stock_amount += (self.__original_amount - self.amount)
            self.product.save()

        self.__original_amount = self.amount
        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_amount = self.amount

class LiveOrder(Order):
    class Meta:
        proxy = True
        verbose_name = _('live order')
        verbose_name_plural = _('live orders')
