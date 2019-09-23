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
        play = board.change_tile(old_width, old_height, new_width, new_height, self.id)
        if play:
            self.moves -= 1
        return play

    @staticmethod
    def get_coordinates(text_input):
        w_values = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11}
        h_values = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "10": 9}

        visual_coordinates = text_input.upper().split(" ")

        if len(visual_coordinates) != 2:
            return False
        if visual_coordinates[0] in w_values.keys() and visual_coordinates[1] in h_values.keys():
            width = w_values.get(visual_coordinates[0])
            height = h_values.get(visual_coordinates[1])
            return width, height
        elif visual_coordinates[0] in h_values.keys() and visual_coordinates[1] in w_values.keys():
            width = w_values.get(visual_coordinates[1])
            height = h_values.get(visual_coordinates[0])
            return width, height
        else:
            return False


class ManualPlayer(Player):
    def __init__(self, name, tokens, moves):
        super().__init__(name, tokens, moves)

    def get_next_move(self):
        while True:
            move_type = input("Play your next turn:\n1. Place New Token\n2. Move Token\nChoose 1 or 2: ")
            # place new token
            # Validation on whether a token can be placed is not performed here
            # it is done in the place_tile function of the Board class
            if move_type == "1":
                if self.tokens == 0:
                    print("You no longer have tokens to place, you can try moving a token\n")
                    continue
                while True:
                    move_input = input("Where would you like to place your token?\n"
                                       "Input coordinates separated by a space: ")
                    # convert visual coordinates to board coordinate values
                    coordinates = Player.get_coordinates(move_input)
                    if not coordinates:
                        print("Invalid Coordinates, try again\n")
                        continue
                    return move_type, coordinates
            # Move existing token
            elif move_type == "2":
                if self.moves == 0:
                    print("You have no moves left\n")
                    return False
                # Loop for choosing which token to move
                # Validation on whether a token can be moved is not performed here
                # it is done in the change_tile function of the Board class
                while True:
                    token_input = input("Which token would you like to move?\n"
                                        "Input coordinates separated by a space: ")
                    # convert visual coordinates to board coordinate values
                    token_coordinates = Player.get_coordinates(token_input)
                    if not token_coordinates:
                        print("Invalid Coordinates, try again\n")
                        continue
                    break
                # Loop for choosing where to move token
                # Validation on whether a token can be placed is not performed here
                # it is done in the change_tile function of the Board class
                while True:
                    move_input = input("Where would you like to move the token to?\n"
                                       "Input coordinates separated by a space: ")
                    move_coordinates = Player.get_coordinates(move_input)
                    if not move_coordinates:
                        print("Invalid Coordinates, try again\n")
                        continue
                    break
                return move_type, token_coordinates, move_coordinates
            print(move_type, " is not a valid input, try again\n")


class AIPlayer(Player):
    def __init__(self, tokens, moves):
        names = ("TARS", "Ava", "J.A.R.V.I.S", "Friday", "Christopher", "Ultron", "Samantha", "HAL 9000")
        super().__init__(choice(names), tokens, moves)

    def get_next_move(self):
        pass
