import numpy as np
from random import choice


class Player:

    count = 0

    def __init__(self, name, tokens, moves):
        Player.count += 1
        self.name = name
        self.tokens = tokens
        self.moves = moves
        self.id = Player.count

    def place_token(self, width, height, board):
        play = board.fill_tile(width, height, self.id)
        if play:
            self.tokens -= 1
            self.moves -= 1
        return play

    def move_token(self, old_width, old_height, new_width, new_height, board):
        play = board.change_tile(old_width, old_height, new_width, new_height)
        if play:
            self.moves -= 1
        return play


class ManualPlayer(Player):
    def __init__(self, name, tokens, moves):
        super().__init__(name, tokens, moves)

    def get_next_move(self):
        pass


class AIPlayer(Player):
    def __init__(self, tokens, moves):
        names = ("TARS", "Ava", "J.A.R.V.I.S", "Friday", "Christopher", "Ultron", "Samantha", "HAL 9000")
        super().__init__(choice(names), tokens, moves)

    def get_next_move(self):
        pass


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros(width, height)

    def fill_tile(self, width, height, value):
        if self.board[width, height] == 0:
            self.board[width, height] = value
            return True
        return False

    def change_tile(self, old_width, old_height, new_width, new_height, value):
        if self.board[old_width, old_height] != value and self.board[new_width, new_height] != 0:
            return False
        self.board[old_width, old_height] = 0
        self.board[new_width, new_height] = value

    def tile_is_empty(self, width, height):
        return self.board[width, height] == 0

    def tile_has_token(self, width, height, value):
        return self.board[width, height] == value


class Game:
    def __init__(self, width, height, player_1, player_2, tokens, moves):
        self.board = Board(width, height)
        self.player_1 = player_1
        self.player_1.tokens = tokens
        self.player_1.moves = moves
        self.player_2 = player_2
        self.player_2.tokens = tokens
        self.player_2.moves = moves
        self.current_player = self.player_1

    def get_next_player(self):
        if self.current_player == self.player_1:
            return self.player_2
        return self.player_1

    def find_cross(self, width, height, value):
        if self.board.board[width, height] != value:
            return False
        if self.board.board[width-1, height-1] != value:
            return False
        if self.board.board[width-1, height+1] != value:
            return False
        if self.board.board[width+1, height-1] != value:
            return False
        if self.board.board[width+1, height+1] != value:
            return False
        return True

    def find_strikethrough(self, width, height, value):
        if self.board.board[width-1, height] != value:
            return False
        if self.board.board[width+1, height] != value:
            return False
        return True

    def evaluate_winner(self):
        # Check if current player is in a winning state
        for row in range(1, self.board.width-2):
            for cell in range(1, self.board.height-2):
                if self.find_cross(row, cell, self.current_player.id):
                    if not self.find_strikethrough(row, cell, self.get_next_player().id):
                        return self.current_player.name

        # Check if next player is in a winning state
        for row in range(1, self.board.width-2):
            for cell in range(1, self.board.height-2):
                if self.find_cross(row, cell, self.get_next_player().id):
                    if not self.find_strikethrough(row, cell, self.current_player().id):
                        return self.get_next_player().name

        return False

    def play(self):
        pass
