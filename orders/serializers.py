from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'address', 'amount', 'created_at']

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            }
