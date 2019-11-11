from player import Player, ManualPlayer
from ai_player import AIPlayer
from board import Board
from state import State
import pdb


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
        # display board
        self.board.display()

        # loop while moves remain
        while True:
            # allow player one to play
            print("{}'s turn".format(self.current_player.name))
            print("Tokens Left: {}  Moves Left: {}\n".format(self.current_player.tokens, self.current_player.moves))
            while True:
                if self.current_player.moves == 0:
                    print("You are out of moves")
                    break

                # Poll the player for their next move
                attempt = self.current_player.get_next_move()
                print("B: {}".format(attempt[1]))
                if attempt:
                    # Player decides to place a new token
                    if attempt[0] == "1":
                        if self.current_player.place_token(attempt[1][1], attempt[1][0], self.board):
                            # Update Game State
                            if self.current_player.id == 1:
                                Player.p1_add_coordinate(attempt[1][1], attempt[1][0])
                                Player.set_state(p1_tokens=self.current_player.tokens,
                                                 p1_moves=self.current_player.moves)
                            elif self.current_player.id == 2:
                                Player.p2_add_coordinate(attempt[1][1], attempt[1][0])
                                Player.set_state(p2_tokens=self.current_player.tokens,
                                                 p2_moves=self.current_player.moves)
                            break
                        print("Move is invalid, try a different move\n")
                        pdb.set_trace()

                    # PLayer decides to move an existing token
                    elif attempt[0] == "2":
                        if self.current_player.move_token(attempt[1][1], attempt[1][0],
                                                          attempt[2][1], attempt[2][0], self.board):
                            # Update Game State
                            if self.current_player.id == 1:
                                Player.p1_remove_coordinate(attempt[1][1], attempt[1][0])
                                Player.p1_add_coordinate(attempt[2][1], attempt[2][0])
                                Player.set_state(p1_moves=self.current_player.moves)
                            elif self.current_player.id == 2:
                                Player.p2_remove_coordinate(attempt[1][1], attempt[1][0])
                                Player.p2_add_coordinate(attempt[2][1], attempt[2][0])
                                Player.set_state(p2_moves=self.current_player.moves)
                            break
                        print("Move is invalid, try a different move\n")
                        pdb.set_trace()

            print("{}'s turn has ended\n".format(self.current_player.name))

            # display board
            self.board.display()
            # pdb.set_trace()

            # check for winner
            winner = self.evaluate_winner()
            if winner:
                print("{} has won the game!\n".format(winner))
                return True

            # change current player and update game state
            self.current_player = self.get_next_player()
            Player.set_state(turn=self.current_player.id)

            # check for game over
            if self.current_player.moves == 0 and self.get_next_player().moves == 0:
                print("NO MORE MOVES, GAME OVER\n")
                return False
