import random

# Определение колоды карт
CARDS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_cards = []
        self.dealer_cards = []
        self.player_score = 0
        self.dealer_score = 0
        self.game_over = False
        self.player_moves = 0  # Счётчик ходов игрока

    def create_deck(self):
        """Создаёт стандартную колоду карт (52 карты)"""
        deck = []
        for card, value in CARDS.items():
            deck.extend([(card, value)] * 4)  # По 4 карты каждого типа (2-10, J, Q, K, A)
        random.shuffle(deck)
        return deck

    def deal_card(self):
        """Раздаёт карту из колоды"""
        card = self.deck.pop()  # Берёт карту с конца списка
        return card

    def start_game(self):
        """Запускает игру, раздаёт стартовые карты"""
        self.player_cards = [self.deal_card(), self.deal_card()]
        self.dealer_cards = [self.deal_card(), self.deal_card()]
        self.player_score = self.calculate_score(self.player_cards)
        self.dealer_score = self.calculate_score(self.dealer_cards)
        self.game_over = False
        self.player_moves = 0  # Сбрасываем счётчик ходов

        return self.get_game_state()

    def calculate_score(self, cards):
        """Вычисляет сумму очков, учитывая тузы"""
        score = sum(card[1] for card in cards)
        num_aces = sum(1 for card in cards if card[0] == 'A')

        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1

        return score

    def player_hit(self):
        """Игрок берет карту"""
        if self.game_over:
            return self.get_game_state()

        if self.player_moves >= 5:  # Ограничиваем количество ходов игрока
            self.game_over = True
            return self.get_game_state()

        card = self.deal_card()
        self.player_cards.append(card)
        self.player_score = self.calculate_score(self.player_cards)
        self.player_moves += 1  # Увеличиваем счётчик ходов

        # Если у игрока перебор, игра заканчивается
        if self.player_score > 21:
            self.game_over = True
            return self.get_game_state()

        return self.get_game_state()

    def dealer_play(self):
        """Дилер берет карты, пока не наберет 17 и больше"""
        while self.dealer_score < 17 and not self.game_over:
            card = self.deal_card()
            self.dealer_cards.append(card)
            self.dealer_score = self.calculate_score(self.dealer_cards)

        # Если дилер перебрал, игра заканчивается
        if self.dealer_score > 21:
            self.game_over = True

    def stand(self):
        """Игрок решает стоять"""
        if self.game_over:
            return self.get_game_state()

        self.dealer_play()  # Дилер начинает играть
        self.game_over = True
        return self.get_game_state()

    def get_game_state(self):
        """Возвращает текущий статус игры (карты и очки)"""
        result = self.check_winner() if self.game_over else None

        return {
            'player_cards': [card[0] for card in self.player_cards],
            'player_score': self.player_score,
            'dealer_cards': [card[0] for card in self.dealer_cards],
            'dealer_score': self.dealer_score,
            'result': result,
            'game_over': self.game_over
        }

    def check_winner(self):
        """Проверка на победителя"""
        if self.player_score > 21:
            return 'Перебор! Вы проиграли.'
        elif self.dealer_score > 21:
            return 'Дилер перебрал! Вы выиграли.'
        elif self.player_score > self.dealer_score:
            return 'Вы выиграли!'
        elif self.player_score < self.dealer_score:
            return 'Вы проиграли!'
        else:
            return 'Ничья!'
