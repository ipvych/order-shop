from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from products.models import Product
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'address', 'amount', 'created_at']

        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def validate(self, data):
        if data['product'].stock_amount < data['amount']:
            raise serializers.ValidationError({'amount':_('There is not enough items in stock')})
        return data
