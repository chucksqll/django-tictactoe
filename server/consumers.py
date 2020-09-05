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
        i = messageToIndex[index[0]]
        j = messageToIndex[index[1]]
        RoomListView.board[i][j]=text

        #check if someone wins and who
        game_result = self.check_if_over()


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'server_message',
                'message': message,
                'text' : text,
                'game_result': game_result
            }
        )

    # Receive message from room group
    async def server_message(self, event):
        message = event['message']
        text = event['text']
        game_result = event['game_result']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'text' : text,
            'game_result': game_result
        }))


    def check_if_over(self):
        for x in range(3):
            if (RoomListView.board[0][x] == RoomListView.board[1][x] and
                    RoomListView.board[0][x] == RoomListView.board[2][x] and
                    RoomListView.board[0][x]!=''):
                return RoomListView.board[0][x]

        for y in range(3):
            if (RoomListView.board[y][0] == RoomListView.board[y][1] and
                    RoomListView.board[y][0] == RoomListView.board[y][2] and
                    RoomListView.board[y][0]!=''):
                return RoomListView.board[y][0]

        if (RoomListView.board[0][0] == RoomListView.board[1][1] and
                RoomListView.board[0][0] == RoomListView.board[2][2] and
                RoomListView.board[0][0]!=''):
            return RoomListView.board[0][0]

        if (RoomListView.board[2][0] == RoomListView.board[1][1] and
                RoomListView.board[2][0] == RoomListView.board[0][2] and
                RoomListView.board[2][0]!=''):
            return RoomListView.board[2][0]

        return False