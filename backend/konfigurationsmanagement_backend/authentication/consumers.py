import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_id = 'user_%s' % self.user_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.user_group_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.user_group_id,
            {
                'type': message,
                'message': message
            }
        )

    def new_changes(self, event):
        message = event['content']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'new_changes',
            'message': message
        }))
