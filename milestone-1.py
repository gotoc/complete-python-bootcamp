import string

def set_board():
    '''Set the starting conditions for a game.'''
    global b
    # b models the 3x3 game board [0][0] through [2][2]
    b = [[" "," "," "],[" "," "," "],[" "," "," "]]
    # return dictionary of variables for game beginning
    return {'player': ["X","O"], 'turn': 1, 'p_turn': 2}

def print_board():
    '''Print out the game board based on global list b.'''
    global b
    i = 1
    print "\n    A   B   C   \n  -------------"
    for r in b:
        row = string.join(r," | ")
        print i,"| " + row + " |\n  -------------"
        i += 1

def player_input(player,input_text):
    '''Take the row and column of a cell that a player wishes to claim'''
    global b
    # User input to designate the selected column of board
    while True:
        c = raw_input(input_text['col']).upper()
        if c == "A":
            col = 0
            break
        elif c == "B":
            col = 1
            break
        elif c == "C":
            col = 2
            break
    # User input to designate the selected row of board
    while True:
        try:
            row = int(raw_input(input_text['row'])) - 1
        except ValueError:
            print input_text['row_err']
            continue
        if row == 0 or row == 1 or row == 2:
            break
    # Only overwrite and return true if cell is "empty"
    if b[row][col] == " ":
        b[row][col] = player
        return True
    else:
        print input_text['taken']
        return False

def check_cond():
    '''Tally cell counts to determine if there is a winner.'''
    global b
    winner = 'none'
    row_count = [{"X":0,"O":0},{"X":0,"O":0},{"X":0,"O":0}]
    col_count = [{"X":0,"O":0},{"X":0,"O":0},{"X":0,"O":0}]
    diag_count = [{"X":0,"O":0},{"X":0,"O":0}]
    i = 0
    for row in b:
        # Check rows for win condition
        for v in row:
            if v != " ":
                row_count[i][v] += 1
                # Game won if there are 3 consecutive X or O
                if row_count[i][v] == 3:
                    winner = v
        i += 1
        # Check columns for win condition
        col = 0
        while col < 3:
            if row[col] != " ":
                col_count[col][row[col]] += 1
                # Game won if there are 3 consecutive X or O
                if col_count[col][row[col]] == 3:
                    winner = row[col]
            col += 1

    # Check for diagonal win condition
    # tuple (row,column,diagonal)
    r = [(0,0,0),(1,1,0),(2,2,0),(0,2,1),(1,1,1),(2,0,1)]
    for q in r:
        if b[q[0]][q[1]] != " ":
            diag_count[q[2]][b[q[0]][q[1]]] += 1
            if diag_count[q[2]][b[q[0]][q[1]]] == 3:
                winner = b[q[0]][q[1]]

    return winner

def replay(input_text):
    '''Asks the user if they would like to start a new game.'''
    return raw_input(input_text['replay']).lower().startswith("y")

def main():
    print "\nARE YOU READY TO TIC TAC TOE?!\n"
    # initiate the game
    p = set_board()
    print_board()
    # Start the game
    x = True
    while  x == True:
        # Determine active player by modulo associated with player list
        player = p['player'][(p['p_turn']%2)]
        # Text to pass to functions for user input
        input_text = {'col':"Please enter the column(A-C): ",
                      'row':"Please enter the row(1-3): ",
                      'row_err':"\nI must insist that you enter a number between 1-3!\n",
                      'replay':"\nDo you want to play again? (yes or no): ",
                      'taken':"\nThat square is already taken! Please try again.\n"}

        # Print out info bar
        print "\nTurn: %s | Player: %s" % (str(p['turn']), player)

        # Collect the player's chosen cell
        while True:
            if player_input(player,input_text) == True:
                print_board()
                break
        p['turn'] += 1
        p['p_turn'] += 1
        # Check to see if there is a winner
        winner = check_cond()
        if winner != 'none':
            print "Congratulations, %s - you're the winner!\n" % winner
            if replay(input_text) == True:
                p = set_board()
                print_board()
            else:
                x = False
        # End game if all cells are filled with no winner
        if p['turn'] > 9:
            print "Game was a tie.\n"
            if replay(input_text) == True:
                p = set_board()
                print_board()
            else:
                x = False
    else:
        print "Goodbye, and thanks for playing!"

main()
