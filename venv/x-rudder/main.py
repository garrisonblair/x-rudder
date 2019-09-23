from game import *
from player import *


def main():
    player_1 = ManualPlayer("Garrison", 15, 30)
    player_2 = ManualPlayer("Samy", 15, 30)

    print(player_1.id, " ", player_1.name)
    print(player_2.id, " ", player_2.name)

    game = Game(10, 12, player_1, player_2, 15, 30)
    game.play()


if __name__ == "__main__":
    main()
