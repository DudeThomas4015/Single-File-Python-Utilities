import random

def print_board(board):
    for row in board:
        print(" ".join(row))

def random_row(board):
    return random.randint(0, len(board) - 1)

def random_col(board):
    return random.randint(0, len(board[0]) - 1)

def place_ship(board):
    orientation = random.choice(["horizontal", "vertical"])
    if orientation == "horizontal":
        row = random_row(board)
        col = random.randint(0, len(board[0]) - 3)
        ship_positions = [(row, col + i) for i in range(3)]
    else:
        row = random.randint(0, len(board) - 3)
        col = random_col(board)
        ship_positions = [(row + i, col) for i in range(3)]
    return ship_positions

def battleship_game():
    board = [["O"] * 5 for _ in range(5)]
    guesses = 6

    print("Let's play Battleship!")
    print_board(board)

    ship_positions = place_ship(board)

    while guesses > 0:
        print(f"Remaining guesses: {guesses}")

        while True:
            try:
                guess_col = int(input("Guess Col (1-5): ")) - 1
                guess_row = int(input("Guess Row (1-5): ")) - 1
                if 0 <= guess_row <= 4 and 0 <= guess_col <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        guess = (guess_row, guess_col)
        if guess in ship_positions:
            print("Hit!")
            board[guess_row][guess_col] = "H"
            ship_positions.remove(guess)
            if not ship_positions:
                print("Congratulations! You sank my battleship!")
                print_board(board)
                break
        else:
            if board[guess_row][guess_col] in ["X", "H"]:
                print("You guessed that one already.")
            else:
                print("You missed my battleship!")
                board[guess_row][guess_col] = "X"
                guesses -= 1
        
        print_board(board)

        if guesses == 0:
            print("Game Over")
            for position in ship_positions:
                board[position[0]][position[1]] = "S"
            print("The ship was at:", ship_positions)
            print_board(board)

if __name__ == "__main__":
    battleship_game()

    # Wait for user input to exit
    input("Press Enter to exit...")
