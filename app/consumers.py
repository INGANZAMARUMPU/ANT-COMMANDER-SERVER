import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        channel = self.channel_name.split("!")[1]
        room = self.scope['url_route']["kwargs"]["room_name"]
        
        await channel_layer.group_add(room, self.channel_name)
        await channel_layer.group_add(channel, self.channel_name)
        await self.accept()
        
        await channel_layer.group_send(channel, {
            "type": "global.event",
            'message': json.dumps({
                "order": "your_id",
                "message": channel
            })
        })

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        room = self.scope['url_route']["kwargs"]["room_name"]
        data = json.loads(text_data)
        order = data["order"]
        print(f"[NEW MESSAGE] {data}")
        if(order == "new_robot"):
            return channel_layer.group_send('commander', {
                "type": "global.event",
                'message': text_data
            })
        elif(order == "new_commander"):
            return channel_layer.group_send('robot', {
                "type": "global.event",
                'message': text_data
            })

        destination = data.get("dest")
        if(destination):
            return channel_layer.group_send(destination, {
                "type": "global.event",
                'message': text_data
            })

    async def global_event(self, event):
        print(f"[SENDING] {event['message']}")
        await self.send(text_data=event['message'])