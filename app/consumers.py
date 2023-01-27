import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await channel_layer.group_add("global", self.channel_name)
        await self.accept()
        channel = self.channel_name
        room = self.scope['url_route']["kwargs"]["room_name"]
        print(f"[NEW_CONNECTION] {channel=}")
        print(f"[NEW_CONNECTION] {room=}")

    async def disconnect(self, close_code):
        channel = self.channel_name
        room = self.scope['url_route']["kwargs"]["room_name"]
        print(f"[DISCONNECTING] {channel=}")
        print(f"[DISCONNECTING] {room=}")
        pass

    async def receive(self, text_data):
        channel = self.channel_name
        room = self.scope['url_route']["kwargs"]["room_name"]
        print(f"[NEW_MESSAGE] {channel=}")
        print(f"[NEW_MESSAGE] {room=}")
        print(f"[NEW_MESSAGE] {text_data=}")
        await channel_layer.group_send('global', {
        	"type": "global.event",
            # "room_id": channel,
            'message': text_data
        })

    async def global_event(self, event):
        await self.send(text_data=event["message"])
        print(f"[FORWADED] {text_data=}")