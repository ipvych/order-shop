import json

import channels.layers
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from rest_framework import generics, status
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

class MakeOrder(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
