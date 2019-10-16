import numpy as np


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height))

    def fill_tile(self, width, height, value):
        if self.board[width, height] == 0:
            self.board[width, height] = value
            return True
        return False

    def change_tile(self, old_width, old_height, new_width, new_height, value):
        # Check that the player is trying to move his token, and that the tile being moved to is empty
        if self.board[old_width, old_height] != value or self.board[new_width, new_height] != 0:
            return False
        # Check that the player is moving to an adjacent tile
        if new_width > old_width + 1 or new_width < old_width - 1:
            return False
        if new_height > old_height + 1 or new_height < old_height - 1:
            return False
        # Move the token
        self.board[old_width, old_height] = 0
        self.board[new_width, new_height] = value
        return True

    def tile_is_empty(self, width, height):
        return self.board[width, height] == 0

    def tile_has_token(self, width, height, value):
        return self.board[width, height] == value

    def display(self):
        for i in range(11):
            print("----", end='')
        print("-----")
        for i, row in reversed(list(enumerate(self.board, start=1))):
            for cell in row:
                if cell == 0:
                    print("|   ", end='')
                elif cell == 1:
                    print("| x ", end='')
                elif cell == 2:
                    print("| o ", end='')
                else:
                    print("|", cell, end='')
            print("| ", i)
            for j in range(11):
                print("----", end='')
            print("-----")
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        for i in range(12):
            print(" ", letters[i], end=' ')
        print('\n')
