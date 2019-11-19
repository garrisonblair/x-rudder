from player import Player, ManualPlayer
from ai_player import AIPlayer
from board import Board
from state import State
import pdb


class Game:
    def __init__(self, player_1, player_2,
                 width=None, height=None, tokens=None, moves=None, board=None, current_player=None):
        if board is None:
            self.board = Board(width, height)
        else:
            self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        if tokens is not None:
            self.player_1.tokens = tokens
            self.player_2.tokens = tokens
        if moves is not None:
            self.player_1.moves = moves
            self.player_2.moves = moves
        if current_player is None:
            self.current_player = self.player_1
        else:
            self.current_player = current_player
        self.moves = moves

    @classmethod
    def from_seed(cls, hex_seed):
        seed = bytes.fromhex(hex_seed).decode()
        values = seed.split('.')
        board = Board(int(values[0]), int(values[1]))
        if values[2] == 'm':
            player_1 = ManualPlayer(values[3], int(values[4]), int(values[5]))
        else:
            player_1 = AIPlayer(values[3], int(values[4]), int(values[5]))
        end = 7 + int(values[6])
        for i in range(7, end):
            coordinates = values[i].split('-')
            x, y = int(coordinates[0]), int(coordinates[1])
            board.fill_tile(x, y, player_1.id)
            Player.p1_add_coordinate(x, y)
        i = end
        if values[i] == 'm':
            player_2 = ManualPlayer(values[i+1], int(values[i+2]), int(values[i+3]))
        else:
            player_2 = AIPlayer(name=values[i+1], tokens=int(values[i+2]), moves=int(values[i+3]))
            Player.set_state(p2_tokens=int(values[i+2]), p2_moves=int(values[i+3]))
        end = i + 5 + int(values[i+4])
        for j in range(i + 5, end):
            coordinates = values[j].split('-')
            x, y = int(coordinates[0]), int(coordinates[1])
            board.fill_tile(x, y, player_2.id)
            Player.p2_add_coordinate(x, y)
        j = end
        if values[j] == "1":
            current_player = player_1
            Player.set_state(width=int(values[0]),
                             height=int(values[1]),
                             turn=1,
                             p1_tokens=int(values[4]),
                             p1_moves=int(values[5]))
        else:
            current_player = player_2
            Player.set_state(width=int(values[0]),
                             height=int(values[1]),
                             turn=2)
        return cls(player_1=player_1, player_2=player_2, board=board, current_player=current_player)

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

    def get_seed(self):
        plain_seed = ''
        state = Player.game_state
        plain_seed += "{}.{}.".format(state.width, state.height)
        if isinstance(self.player_1, ManualPlayer):
            plain_seed += 'm.'
        else:
            plain_seed += 'a.'
        plain_seed += "{}.{}.{}.".format(self.player_1.name, state.p1_tokens, state.p1_moves)
        plain_seed += "{}.".format(len(state.p1_coordinates))
        for (x, y) in state.p1_coordinates:
            plain_seed += "{}-{}.".format(x, y)

        if isinstance(self.player_2, ManualPlayer):
            plain_seed += 'm.'
        else:
            plain_seed += 'a.'
        plain_seed += "{}.{}.{}.".format(self.player_2.name, state.p2_tokens, state.p2_moves)
        plain_seed += "{}.".format(len(state.p2_coordinates))
        for (x, y) in state.p2_coordinates:
            plain_seed += "{}-{}.".format(x, y)
        plain_seed += "{}".format(self.current_player.id)

        seed = plain_seed.encode().hex()

        return seed

    def evaluate_winner(self):
        # Check if current player is in a winning state
        for row in range(1, self.board.width-2):
            for cell in range(1, self.board.height-2):
                if self.find_cross(row, cell, self.current_player.id):
                    if not self.find_strikethrough(row, cell, self.get_next_player().id):
                        return self.current_player

        # Check if next player is in a winning state
        for row in range(1, self.board.width-2):
            for cell in range(1, self.board.height-2):
                if self.find_cross(row, cell, self.get_next_player().id):
                    if not self.find_strikethrough(row, cell, self.current_player.id):
                        return self.get_next_player()

        return False

    def play(self):
        # display board
        self.board.display()

        # loop while moves remain
        while True:
            # Display state seed
            print("The seed for game at this point is {}".format(self.get_seed()))
            # allow player one to play
            print("{}'s turn".format(self.current_player.name))
            print("Tokens Left: {}  Moves Left: {}\n".format(self.current_player.tokens, self.current_player.moves))
            while True:
                if self.current_player.moves == 0:
                    print("You are out of moves")
                    break

                # Poll the player for their next move
                attempt = self.current_player.get_next_move()
                # print("B: {}".format(attempt[1]))
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
                            display_move = Player.display_coordinates(attempt[1][1], attempt[1][0])
                            print("{} has placed a token at {}".format(self.current_player.name, display_move))
                            break
                        print("Move is invalid, try a different move\n")
                        if isinstance(self.current_player, AIPlayer):
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
                            display_move_from = Player.display_coordinates(attempt[1][1], attempt[1][0])
                            display_move_to = Player.display_coordinates(attempt[2][1], attempt[2][0])
                            print("{} has moved token from {} to {}".format(self.current_player.name,
                                                                            display_move_from,
                                                                            display_move_to))
                            break
                        print("Move is invalid, try a different move\n")
                        if isinstance(self.current_player, AIPlayer):
                            pdb.set_trace()

            print("{}'s turn has ended\n".format(self.current_player.name))

            # display board
            self.board.display()

            # check for winner
            winner = self.evaluate_winner()
            if winner:
                moves = self.moves - winner.moves
                print("{} has won the game in {} moves!\n".format(winner.name, moves))
                return True

            # change current player and update game state
            self.current_player = self.get_next_player()
            Player.set_state(turn=self.current_player.id)

            # check for game over
            if self.current_player.moves == 0 and self.get_next_player().moves == 0:
                print("NO MORE MOVES, GAME OVER\n")
                return False
