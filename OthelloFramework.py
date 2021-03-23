import random


# this class stores an othello board state
# the state is handled as a 1d list that stores a 10x10 board.  1 and -1 are white and black, respectively, 0 are empty squares
class Board:
    # make a starting board with four pieces (two of each color) in the center
    def __init__(self):
        self.state = [0] * 100
        self.state[44] = 1  # white
        self.state[45] = -1  # black
        self.state[54] = -1
        self.state[55] = 1

    # returns the score as the difference between the number of 1s and the number of -1s
    def evaluate(self):
        value = 0
        for i in range(100):
            if self.state[i] == 1:
                value = value + 1
            elif self.state[i] == -1:
                value = value - 1
        return value

    # returns a new board that is a copy of the current board
    def copy(self):
        board = Board()
        for i in range(100):
            board.state[i] = self.state[i]
        return board

    # given a x,y position, returns the tile within the 1d list
    def index(self, x, y):
        if x >= 0 and x < 10 and y >= 0 and y < 10:
            return self.state[x + y * 10]  # Empty spaces are represented with a 0, so we're checking this particular position to see if one is there
        else:
            return -2  # out of bounds, return -2 for error since 0 is used for "empty" space and -1 represents black

    # given an x,y coordinate, and an id of 1 or -1, returns true if this is a valid move
    def canplace(self, x, y, id):
        if self.index(x, y) != 0:  # Tile is taken already, return false
            return False
        # dirs stores a list of tuples that each compute the 8 different directions from the tile (x,y)
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        for xop, yop in dirs:
            i, j = xop(x), yop(y)  # obtain x and y values of lambda functions
            if self.index(i, j) != -id:  # if our own chip, continue
                continue
            # keep going until we hit our own piece
# i, j = xop(i), yop(j)
            while self.index(i, j) == -id:  # if we do encounter an enemy's piece, check the next pieces until we don't see the enemy's chips anymore
                i, j = xop(i), yop(j)
            if self.index(i, j) == id: # if we found a piece of our own color, then this is a valid move
                return True
        # if I can't capture in any direction, I can't place here
        return False

    # given an x,y coordinate, and an id of 1 or -1, place a tile (if valid) at x,y, and modify the state accordingly
    def place(self, x, y, id):
        if not self.canplace(x, y, id):
            return

        self.state[x + y * 10] = id
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]

        for xop, yop in dirs:
            i, j = xop(x), yop(y)
            if self.index(i, j) != -id:
                continue
            while self.index(i, j) == -id: # Keep going while it's still an opponent piece
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id: # once we've found our own piece, we're going to place our piece down at (x,y) and flip all enemy pieces
                k, l = xop(x), yop(y)
                while k != i or l != j:  # go back and flip all the pieces to my color
                    self.state[k + l * 10] = id
                    k, l = xop(k), yop(l)

    # returns a list of all valid x,y moves for a given id
    def validmoves(self, id):
        moves = []
        for x in range(10):
            for y in range(10):
                if self.canplace(x, y, id):  # Within the board, we need to check if it is a place we can actually place
                    moves = moves + [(x, y)]  # if we can place it there, we'll add it to the list of moves we're going to return
        return moves

    # Gives the potential boards after a particular move
    def allmoves(self, id):
        boards = []
        for move in self.validmoves(id):
            newboard = self.copy()
            newboard.place(move[0], move[1], id)  # move[0] is the x portion of my tuple, move[1] is the y portion
            boards.append(newboard)
        return boards

    # moves.sort(reverse=True,key=lambda x:x[0])

    # print out the board.  1 is X, -1 is O
    def printboard(self):
        for y in range(10):
            line = ""
            for x in range(10):
                if self.index(x, y) == 1:
                    line = line + "X"
                elif self.index(x, y) == -1:
                    line = line + "O"
                else:
                    line = line + "."
            print(line)
        print()

    # state is an end game if there are no empty places
    def end(self):
        if not 0 in self.state: # No more empty spaces left on the board
            return True
        elif len(self.validmoves(1)) == 0 and len(self.validmoves(-1)) == 0: # No one can make a valid move, game is over
            return True
        else:
            return False



    # Returns the best possible move based on a heuristic value. Grabbing edges and corners give better scores for the heuristic
    def heuristic(self, id):
        heu_scores = []
        movelist = self.allmoves(id)  # returns a list of boards

        # we need to "make the move" first, then look at all these conditions
        for i in range(len(movelist)):
            points = 0
            # check corners of board - 4 if statements with specific coordinates, add to count
            if movelist[i].index(0, 0) == id:
                points = points + 10
            if movelist[i].index(0, 9) == id:
                points = points + 10
            if movelist[i].index(9, 0) == id:
                points = points + 10
            if movelist[i].index(9, 9) == id:
                points = points + 10

            # check number of edges taken by the player - excluding corners
            for x in range(1, 9):
                if movelist[i].index(x, 0) == id:
                    points = points + 2
                if movelist[i].index(x, 9) == id:
                    points = points + 2
            for y in range(1, 9):
                if movelist[i].index(0, y) == id:
                    points = points + 2
                if movelist[i].index(9, y) == id:
                    points = points + 2
            movelist[i] = (points, movelist[i])
        heu_scores.sort(reverse=True, key=lambda x: x[0])


        bestmove = movelist[0][1]
        return bestmove

    # Returns the score of the game at the moment
    def score(self, id):
        value = 0
        for i in range(100):
            if self.state == id:
                value = value + 1
        return value

    # Method to find move that grants the largest amount of flips / points
    def greedy_player(self, id):
        moves = self.allmoves(id)
        # Give all the moves an attaching score - make a tuple of score and move
        for i in range(len(moves)):
            moves[i] = (moves[i].score(id), moves[i])
        moves.sort(reverse=True, key=lambda x: x[0])  # Sorting the moves in reverse, so biggest comes first
        # we need to pick the best move
        bestmove = moves[0][1]  # moves[0][1] look to the zeroth index tuple (the first tuple) in my list, then pick the move inside the tuple (the second thing in THAT tuple)
        return bestmove

    # Performs an ndepth_minimax A.I. optimization technique
    # The opponent's moves will be looked at then the player's moves for EACH of those moves will be looked at all the way to n-depth
    # Anything greater than n=2 is unrealistic because of the ridiculous exponential growth
    def ndepth_minimax(self, id, n, recursive_call=False):
        movelist = self.allmoves(id)
        for i in range(len(movelist)):
            # for each board here, call the allmoves function for the opponent to look at the retaliation of that particular move
            opponentmoves = movelist[i].allmoves(-id)
            if movelist[i].end(): # if this move ends the game, this is the best move, so put it in your movelist with the score
                movelist[i] = (movelist[i].score(id), movelist[i])
            elif len(opponentmoves) == 0: # if the opponent has no counter moves, then this is the next best move besides end game, make that move!
                movelist[i] = (movelist[i].score(id), movelist[i])

            else: # We need to gather all the opponent's opposing moves and check which one is the worst.
                for j in range(len(opponentmoves)):
                    # Check worst outcome for us (best outcome in opponent's case)
                    if opponentmoves[j].end():
                        opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                    elif len(opponentmoves[j].allmoves(id)) == 0:
                        opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                    else:
                        # check depth first, if no depth, then just exit out, no recursion needed
                        if n == 0:
                            opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                        else:
                            # If n != 0, we need to call function again to gather the next move subset of moves
                            # recursive_call will remain true for as long as we haven't reached n=0
                            opponent_score = opponentmoves[j].ndepth_minimax(id, n=n-1, recursive_call=True)
                            opponentmoves[j] = (opponent_score, opponentmoves[j])

                # The other player wants the opponent's WORST score (meaning it's the best for him/her) - reverse=False
                opponentmoves.sort(reverse=False, key=lambda x: x[0])
                movelist[i] = (opponentmoves[0][0], movelist[i])
        # We now have all our moves, so we need to sort them based on score and return the best move
        movelist.sort(reverse=True, key=lambda x: x[0])
        bestmove = movelist[0][1]
        if recursive_call == True:
            return movelist[0][0]
        else:
            return bestmove

    # Same idea as ndepth_minimax, but no recursion is required. This could have been baked inside of ndepth, but I made this first, so I decided to just keep it
    def onedepth_minimax(self, id):
        movelist = self.allmoves(id) # Get all possible moves for the player

        for i in range(len(movelist)):
            opponentmoves = movelist[i].allmoves(-id) # list of opponent moves for EACH move for the player
            # if this move ends the game or causes the opponent to have no countermoves, this is the best move
            if movelist[i].end():
                movelist[i] = (movelist[i].score(id), movelist[i])
            elif len(opponentmoves) == 0:
                movelist[i] = (movelist[i].score(id), movelist[i])
            else:
                for j in range(len(opponentmoves)):
                    # Get the scores of all the opponent's moves, then get the worst ones.
                    opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                opponentmoves.sort(reverse=False, key=lambda x: x[0]) # Want to sort based on worst move (because it's best move for us)
                movelist[i] = (opponentmoves[0][0], movelist[i])
        # Now with OUR movelist, we want to sort it based on the best score and return the move
        movelist.sort(reverse=True, key=lambda x: x[0])
        bestmove = movelist[0][1]
        return bestmove


# initializes the game and lets the user choose A.I. optimizations (if any) for each computer player
def game():
    board = Board()
    turn = 1 # start game with X going first
    print("Which optimization would you like for X?")
    answer1 = input("Heuristic, 0-depth, 1-depth, 2-depth, n-depth, None (greedy only): ")
    if answer1 == "n-depth":
        n1 = int(input("Specify depth "))
    print("Which optimization would you like for O?")
    answer2 = input("Heuristic, 0-depth, 1-depth, 2-depth, n-depth, None (greedy only): ")
    if answer2 == "n-depth":
        n2 = int(input("Specify depth "))
    while True:

        movelist = board.validmoves(turn)
        if len(movelist) == 0: # no moves - skip the turn
            turn = -turn
            continue

        board = board.copy()

        # Depending on optimization, the appropriate function is called
        if turn == 1: # X turn
            print("X's turn")
            if answer1 == "Heuristic":
                board = board.heuristic(turn)
            elif answer1 == "0-depth":
                board = board.ndepth_minimax(turn, 0, False)
            elif answer1 == "1-depth":
                board = board.onedepth_minimax(turn)
            elif answer1 == "2-depth":
                board = board.ndepth_minimax(turn, 2, False)
            elif answer1 == "n-depth":
                board = board.ndepth_minimax(turn, n1, False)
            elif answer1 == "None":
                board = board.greedy_player(turn)

        elif turn == -1: # O turn
            print("O's turn")
            if answer2 == "Heuristic":
                board = board.heuristic(turn)
            elif answer2 == "0-depth":
                board = board.ndepth_minimax(turn, 0, False)
            elif answer2 == "1-depth":
                board = board.onedepth_minimax(turn)
            elif answer2 == "2-depth":
                board = board.ndepth_minimax(turn, 2, False)
            elif answer2 == "n-depth":
                board = board.ndepth_minimax(turn, n2, False)
            elif answer2 == "None":
                board = board.greedy_player(turn)

        turn = -turn # swap players
        board.printboard() # print the board after the current player makes the move
        input() # wait for user to press a key to continue the game
        if board.end(): # if game is over, break and end the program
            break

    # Get the score of the game to see who won and print out the winner
    gamescore = board.evaluate()
    if gamescore > 0:
        print("Score is", gamescore, ". X won!")
    elif gamescore < 0:
        print("Score is", gamescore, ". O won!")
    else:
        print("Score is 0. Tied game!")

game()
