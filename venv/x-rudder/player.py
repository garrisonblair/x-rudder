from state import State


class Player:
    count = 0
    game_state = State(0, 0, 0, 0, 0, 0)

    def __init__(self, name, tokens, moves):
        Player.count += 1
        self.name = name
        self.tokens = tokens
        self.moves = moves
        self.id = Player.count

    def move_token(self, old_width, old_height, new_width, new_height, board):
        play = board.change_tile(old_width, old_height, new_width, new_height, self.id)
        if play:
            self.moves -= 1
        return play

    @staticmethod
    def set_state(width=None, height=None, p1_tokens=None, p1_moves=None, p2_tokens=None, p2_moves=None, turn=None):
        if width:
            Player.game_state.width = width
        if height:
            Player.game_state.height = height
        if p1_tokens:
            Player.game_state.p1_tokens = p1_tokens
        if p1_moves:
            Player.game_state.p1_moves = p1_moves
        if p2_tokens:
            Player.game_state.p2_tokens = p2_tokens
        if p2_moves:
            Player.game_state.p2_moves = p2_moves
        if turn:
            Player.game_state.turn = turn

    @staticmethod
    def p1_add_coordinate(x, y):
        Player.game_state.p1_coordinates.append((x, y))

    @staticmethod
    def p1_remove_coordinate(x, y):
        Player.game_state.p1_coordinates.remove((x, y))

    @staticmethod
    def p2_add_coordinate(y, x):
        Player.game_state.p2_coordinates.append((x, y))

    @staticmethod
    def p2_remove_coordinate(y, x):
        Player.game_state.p2_coordinates.remove((x, y))

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

    def place_token(self, width, height, board):
        print("C: {}, {}".format(width, height))
        play = board.fill_tile(width, height, self.id)
        if play:
            self.tokens -= 1
            self.moves -= 1
        return play

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
