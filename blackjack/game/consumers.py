import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_logic import BlackjackGame

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """При подключении WebSocket-клиента"""
        self.game = BlackjackGame()
        self.game.start_game()

        # Принимаем соединение и отправляем начальное состояние игры
        await self.accept()
        await self.send(text_data=json.dumps(self.game.get_game_state()))

    async def disconnect(self, close_code):
        """Отключение WebSocket-клиента"""
        pass

    async def receive(self, text_data):
        """Обрабатываем сообщения от клиента"""
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'hit':
            game_state = self.game.player_hit()
        elif action == 'stand':
            game_state = self.game.stand()
        else:
            game_state = self.game.get_game_state()

        # Отправляем обновлённое состояние игры клиенту
        await self.send(text_data=json.dumps(game_state))
