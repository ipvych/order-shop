import json

import channels.layers
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import OrderSerializer

# Create your views here.

def broadcast_order(order):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'live_orders', {
            "type": 'new_order',
            "content": order,
        })

class MakeOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.pk
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, pk=request.data['product'])
        if product.stock_amount >= int(request.data['amount']):
            product.stock_amount -= int(request.data['amount'])
            product.save()
            serializer.save()
            broadcast_order(serializer.data)
            return Response()
        else:
            return Response({'amount': [_('There is not enough items in stock')]},
                            status=status.HTTP_400_BAD_REQUEST)
