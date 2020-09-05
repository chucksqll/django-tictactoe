import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import RoomListView
class ServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'server_%s' % self.room_name

        # Join room group
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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        text = text_data_json['text']

        index = message.split('-')

        messageToIndex = {
            'top': 0,
            'left' : 0,
            'mid': 1,
            'bot': 2,
            'right' : 2
        }

        x = messageToIndex[index[0]]
        y = messageToIndex[index[1]]

        RoomListView.board[x][y]=text

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'server_message',
                'message': message,
                'text' : text
            }
        )

    # Receive message from room group
    async def server_message(self, event):
        message = event['message']
        text = event['text']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'text' : text
        }))