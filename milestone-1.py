import string

b = [["*","*","*"],["*","*","*"],["*","*","*"]]

# Print out the game board based on global list b
def print_board():
    global b
    i = 1
    print "\n    A   B   C   \n  -------------"
    for r in b:
        row = string.join(r," | ")
        print i,"| " + row + " |\n  -------------"
        i += 1

# Take the row and column of a cell that a player wishes claim
def player_input(player):
    global b
    # User input to designate the selected column of board
    while True:
        c = raw_input("Please enter the column(A-C): ")
        if c.upper() == "A":
            col = 0
            break
        elif c.upper() == "B":
            col = 1
            break
        elif c.upper() == "C":
            col = 2
            break
        else:
            print "\nPlease enter A, B, or C!\n"
    # User input to designate the selected row of board
    while True:
        while True:
            try:
                row = int(raw_input("Please enter the row(1-3): ")) - 1
                break
            except ValueError:
                print "\nI must insist that you enter a number between 1-3!\n"
        if row == 0 or row == 1 or row == 2:
            break
        else:
            print "\nI must insist that you enter a number between 1-3!\n"
    # Only overwrite and return true if cell is "empty"
    if b[row][col] == "*":
        b[row][col] = player
        return True
    else:
        return False

# Tally cell counts to determine if there is a winner
def check_cond():
    global b
    winner = 'V'
    row_count = [{"X":0,"O":0},{"X":0,"O":0},{"X":0,"O":0}]
    col_count = [{"X":0,"O":0},{"X":0,"O":0},{"X":0,"O":0}]
    diag_count = [{"X":0,"O":0},{"X":0,"O":0}]
    i = 0
    for row in b:
        # Check rows for win condition
        for v in row:
            if v != "*":
                row_count[i][v] += 1
                if row_count[i][v] == 3:
                    winner = v
        i += 1
        # Check columns for win condition
        col = 0
        while col < 3:
            if row[col] != "*":
                col_count[col][row[col]] += 1
                if col_count[col][row[col]] == 3:
                    winner = row[col]
            col += 1
    # Check for diagonal win condition
    if b[0][0] != "*":
        diag_count[0][b[0][0]] += 1
        if diag_count[0][b[0][0]] == 3:
            winner = b[0][0]
    if b[0][2] != "*":
        diag_count[1][b[0][2]] += 1
        if diag_count[1][b[0][2]] == 3:
            winner = b[0][2]
    if b[1][1] != "*":
        diag_count[0][b[1][1]] += 1
        diag_count[1][b[1][1]] += 1
        if diag_count[0][b[1][1]] == 3 or diag_count[1][b[1][1]] == 3:
            winner = b[1][1]
    if b[2][0] != "*":
        diag_count[1][b[2][0]] += 1
        if diag_count[1][b[2][0]] == 3:
            winner = b[2][0]
    if b[2][2] != "*":
        diag_count[0][b[2][2]] += 1
        if diag_count[0][b[2][2]] == 3:
            winner = b[2][2]
    return winner

def main():
    turn = 1
    p_turn = 2
    player = ["X","O"]

    print "\nARE YOU READY TO TIC TAC TOOOOEEEEEE!!!!!!!!\n"
    print ".###..###..###...###...#....###...###..###..###."
    print "..#....#...#......#...#.#...#......#...#.#..##.."
    print "..#...###..###....#..##.##..###....#...###..###."
    print_board()

    while True:
        print "\nTurn: %s | Player: %s" % (str(turn), player[(p_turn%2)])
        while True:
            if player_input(player[(p_turn%2)]) == True:
                print_board()
                break
            else:
                print "\nThat square is already taken! Please try again.\n"
        winner = check_cond()
        if winner != 'V':
            print "Congratulations, %s - you're the winner!" % winner
            break
        turn += 1
        if turn > 9:
            print "Game was a tie. Thanks for playing!"
            break
        p_turn += 1

main()
