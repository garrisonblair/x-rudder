from game import *
from player import *
from random import randint


def main():
    print("#######################################")
    print("# W E L C O M E  T O  X - R U D D E R #")
    print("#######################################")

    while True:
        print("\nHow many are playing?")
        game_type = input("1. One Player\n2. Two Player\n")
        if game_type == "2":
            p1_name = input("Enter name for player 1: ")
            player_1 = ManualPlayer(p1_name, 15, 30)
            p2_name = input("Enter name for player 2: ")
            player_2 = ManualPlayer(p2_name, 15, 30)
            break
        elif game_type == "1":
            while True:
                print("Who will play first?")
                first = input("1. Human\n2. Computer\n")
                if first == "1":
                    print("You will play first")
                    p1_name = input("Enter name for player 1: ")
                    player_1 = ManualPlayer(p1_name, 15, 30)
                    player_2 = AIPlayer(15, 30)
                    break
                elif first == "2":
                    print("Computer will play first")
                    player_1 = AIPlayer(15, 30)
                    p2_name = input("Enter name for player 2: ")
                    player_2 = ManualPlayer(p2_name, 15, 30)
                    break
            break

    print("Starting Game...")

    game = Game(10, 12, player_1, player_2, 15, 30)
    Player.set_state(width=10, height=12, p1_tokens=15, p1_moves=30, p2_tokens=15, p2_moves=30, turn=1)
    game.play()


if __name__ == "__main__":
    main()
