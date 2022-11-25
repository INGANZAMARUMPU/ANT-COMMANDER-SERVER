import json
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

class ChatConsumer(WebsocketConsumer):
    offer = None
    candidate = []

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
        str_message = event["message"]
        message = json.loads(str_message)

        if(message["order"] == "set-offer"):
            self.offer = str_message
            self. candidates = []
        elif(message["order"] == "remote-candidate"):
            self.candidates.append(str_message)
        elif(message["order"] == "join-room"):
            self.send(text_data=offer)
            for candidate in self.candidates:
                self.send(text_data=candidate)
            return

        self.send(text_data=str_message)