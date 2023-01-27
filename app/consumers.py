import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await channel_layer.group_add("global", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        channel = self.channel_name
        room = self.scope['url_route']["kwargs"]["room_name"]
        print(f"[DISCONNECTING] {channel=}")
        print(f"[DISCONNECTING] {room=}")
        pass

    async def receive(self, text_data):
        room = self.scope['url_route']["kwargs"]["room_name"]
        data = json.loads(text_data)
        order = data["order"]

        if(order == "new_robot"):
            await channel_layer.group_add(
                data["message"]["id"],
                self.channel_name
            )
            return channel_layer.group_send('global', {
                "type": "global.event",
                'message': text_data
            })
        elif(order == "new_robot"):
            return channel_layer.group_send('global', {
                "type": "global.event",
                'message': text_data
            })
        destination = data.get("dest")
        if(destination):
            return channel_layer.group_send('global', {
                "type": "global.event",
                "room_id": destination,
                'message': text_data
            })
        return channel_layer.group_send('global', {
            "type": "global.event",
            'message': text_data
        })

    async def global_event(self, event):
        await self.send(text_data=event["message"])