import json
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(channel_layer.group_add)("global", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        async_to_sync(channel_layer.group_send)('global', {
        	"type": "global.event",
            'message': text_data
        })

    def global_event(self, event):
        self.send(text_data=event["message"])