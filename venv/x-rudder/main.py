from game import *
from player import *


def main():
    print("#######################################")
    print("# W E L C O M E  T O  X - R U D D E R #")
    print("#######################################")
    p1_name = input("Enter name for player 1: ")
    player_1 = ManualPlayer(p1_name, 15, 30)

    while True:
        print("\nPlayer 2 selection")
        game_type = input("1. Manual\n2. Automatic\n")
        if game_type == "1":
            p2_name = input("Enter name for player 2: ")
            player_2 = ManualPlayer(p2_name, 15, 30)
            break
        elif game_type == "2":
            # player_2 = AIPlayer(15, 30)
            print("Coming Soon...")
            pass

    print("Starting Game...")

    game = Game(10, 12, player_1, player_2, 15, 30)
    game.play()


if __name__ == "__main__":
    main()
