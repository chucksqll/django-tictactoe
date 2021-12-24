import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .views import RoomView


class ServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'server_%s' % self.room_name

        if not self.room_name in RoomView.board:
            RoomView.board[self.room_name] = [
                ['','',''],
                ['','',''],
                ['','',''],
            ]
            RoomView.last_turn[self.room_name] = 'O'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
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

        if message =='reset':
            self.restart()           
        elif text == RoomView.last_turn[self.room_name]:
            print('wait, until your turn')
            text = 'O' if text == 'O' else 'X' 
        elif text != '':
            if text is None:
                text = ''
            self.fill_board(message, text)

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
                # message: game-square id that was clicked
                # text: the player that clicked that is croos or circle
                # game_result: 
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
            'game_result': game_result,
            'board': RoomView.board[self.room_name]
        }))


    def restart(self):
        RoomView.last_turn[self.room_name]='O'
        for i in range(3):
            for j in range(3):
                RoomView.board[self.room_name][i][j]=''


    def fill_board(self, message, text):
        RoomView.last_turn[self.room_name]=text
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
        if(RoomView.board[self.room_name][i][j]==''):
            RoomView.board[self.room_name][i][j]=text


    def check_if_over(self):
        for x in range(3):
            if (RoomView.board[self.room_name][0][x] == RoomView.board[self.room_name][1][x] and
                    RoomView.board[self.room_name][0][x] == RoomView.board[self.room_name][2][x] and
                    RoomView.board[self.room_name][0][x]!=''):
                return RoomView.board[self.room_name][0][x]

        for y in range(3):
            if (RoomView.board[self.room_name][y][0] == RoomView.board[self.room_name][y][1] and
                    RoomView.board[self.room_name][y][0] == RoomView.board[self.room_name][y][2] and
                    RoomView.board[self.room_name][y][0]!=''):
                return RoomView.board[self.room_name][y][0]

        if (RoomView.board[self.room_name][0][0] == RoomView.board[self.room_name][1][1] and
                RoomView.board[self.room_name][0][0] == RoomView.board[self.room_name][2][2] and
                RoomView.board[self.room_name][0][0]!=''):
            return RoomView.board[self.room_name][0][0]

        if (RoomView.board[self.room_name][2][0] == RoomView.board[self.room_name][1][1] and
                RoomView.board[self.room_name][2][0] == RoomView.board[self.room_name][0][2] and
                RoomView.board[self.room_name][2][0]!=''):
            return RoomView.board[self.room_name][2][0]
        for x in range(3):
            for y in range(3):
                if RoomView.board[self.room_name][y][x] =='':
                    return False
        return "Draw"