class State:
    def __init__(self, width, height, p1_tokens, p1_moves, p2_tokens, p2_moves):
        self.width = width
        self.height = height
        self.p1_tokens = p1_tokens
        self.p1_moves = p1_moves
        self.p1_coordinates = []
        self.p2_tokens = p2_tokens
        self.p2_moves = p2_moves
        self.p2_coordinates = []
        self.turn = 1

    def is_terminal(self):
        if self.p2_moves == 0:
            return True
        else:
            return False
