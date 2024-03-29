# x-rudder
X-Rudder is a 2-player adversary game played with 30 square tokens (15/per color) on 12x10(12(width)x 10(height))board that is initially empty. The board is numbered 1 to 10 from bottom to top, and A to L from left to right.

Each player takes turn placing their tokens on the board or moving them (up, down, left, right, and  diagonal). As  soon  as  one  player is able to set an X with their 5 five tokens and avoided a strikethrough they become a winner only if they completed the X and the opponent did not strikethrough their X, that is, the opponent puts their two tokens on the left and right to the center of the central token of the X.

## Running the program
To run the program, simply run the main.py file.

## Playing with two manual players
In this case, both players are controlled by a human.

## Playing against an AI player
In this case, player two is controlled by the computer, and plays automatically.

### Setting Up
- Enter the name for Player 1 when prompted.
- You will be asked if you want to play Manual or Automatic Mode, press 1 to select Manual, 2 to select Automatic.
- Enter the name for Player 2.

### Gameplay
- You are asked whether you want to place a new token (1) or move an existing token (2).
- To place a new token, press 1.
  - Input the coordinates separated by a space: column letter [A-L] and row number [1-10].
- To move an existing token, press 2.
  - Input the coordinates of the token to move separated by a space: column letter [A-L] and row number [1-10].
  - Input the coordinates of where to place the token separated by a space: column letter [A-L] and row number [1-10].
- Players will alternate turns until a player wins or both players run out of moves
