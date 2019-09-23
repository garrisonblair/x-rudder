from player import Player, ManualPlayer, AIPlayer
from board import Board


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
        if self.board.board[width, height+1] != value:
            return False
        if self.board.board[width, height-1] != value:
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
                    if not self.find_strikethrough(row, cell, self.current_player.id):
                        return self.get_next_player().name

        return False

    def play(self):
        # loop while moves remain
        while True:
            # display board
            self.board.display()
            # allow player one to play
            print("{}'s turn".format(self.current_player.name))
            print("Tokens Left: {}  Moves Left: {}\n".format(self.current_player.tokens, self.current_player.moves))
            while True:
                attempt = self.current_player.get_next_move()
                if attempt:
                    if attempt[0] == "1":
                        if self.current_player.place_token(attempt[1][1], attempt[1][0], self.board):
                            break
                        print("Move is invalid, try a different move\n")
                    elif attempt[0] == "2":
                        if self.current_player.move_token(attempt[1][1], attempt[1][0],
                                                          attempt[2][1], attempt[2][0], self.board):
                            break
                        print("Move is invalid, try a different move\n")
            print("{}'s turn has ended\n".format(self.current_player.name))
            # display board
            self.board.display()
            # check for winner
            winner = self.evaluate_winner()
            if winner:
                print("{} has won the game!\n".format(winner))
                return True
            # change current player
            self.current_player = self.get_next_player()
