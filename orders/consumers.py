import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from users.models import User
from products.models import Product

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_staff:
            await self.close()

        # Join room group
        self.room_group_name = 'live_orders'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def get_user_phone(self, user_pk):
        return User.objects.get(pk=user_pk).phone

    def get_product_name(self, product_pk):
        return Product.objects.get(pk=product_pk).name

    async def new_order(self, event):
        data = event['content']
        data['user_phone'] = await database_sync_to_async(
            self.get_user_phone)(data['user'])
        data['product_name'] = await database_sync_to_async(
            self.get_product_name)(data['product'])
        await self.send(text_data=json.dumps(data))
