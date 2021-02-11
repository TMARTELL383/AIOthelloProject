import random


# this class stores an othello board state
# the state is handled as a 1d list that stores a 10x10 board.  1 and -1 are the two colors, 0 are empty squares
class Board:
    # make a starting board.  There are four pieces in the center
    # constructor that initializes the board to have 4 pieces (2b, 2w) start in the middle of the board
    def __init__(self):
        self.state = [0] * 100
        self.state[44] = 1  # 1 will be white
        self.state[45] = -1  # -1 will be black
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
            return self.state[
                x + y * 10]  # Empty spaces are represented with a 0, so we're checking this particular position to see if one is there
        else:
            # out of bounds, return -2 for error
            return -2  # a -2 return ensures that we will have self.index(x,y) != 0, so we return false

    # given an x,y coordinate, and an id of 1 or -1, returns true if this is a valid move
    # Basically an allmoves function
    def canplace(self, x, y, id):
        # square is not empty? return false
        if self.index(x, y) != 0:  # If the tile is NOT an empty space (0), then return false
            return False
        # dirs stores a list of tuples that each compute the 8 different directions from a tile x,y
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        for xop, yop in dirs:  # for each x,y in each lambda function in dirs...
            # move one space.  is the piece the opponent's color?
            i, j = xop(x), yop(y)  # I still don't know what this line means
            if self.index(i, j) != -id:  # we want opponent's color, not our own because we want to flip their pieces
                # no, then we'll move on to the next direction
                continue
            # keep going until we hit our own piece
            i, j = xop(i), yop(j)
            while self.index(i, j) == -id:  # if we do encounter an enemy's piece...
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                return True
        # if I can't capture in any direction, I can't place here
        return False

    # given an x,y coordinate, and an id of 1 or -1, place a tile (if valid) at x,y, and modify the state accordingly
    def place(self, x, y, id):
        # don't bother if it isn't a valid move
        if not self.canplace(x, y, id):
            return
        # place your piece at x,y
        self.state[x + y * 10] = id
        dirs = [(lambda x: x, lambda y: y - 1), (lambda x: x, lambda y: y + 1), (lambda x: x - 1, lambda y: y - 1),
                (lambda x: x - 1, lambda y: y), (lambda x: x - 1, lambda y: y + 1), (lambda x: x + 1, lambda y: y - 1),
                (lambda x: x + 1, lambda y: y), (lambda x: x + 1, lambda y: y + 1)]
        # go through each direction
        for xop, yop in dirs:
            i, j = xop(x), yop(y)
            # move one space.  is the piece the opponent's color?
            if self.index(i, j) != -id:
                # no, then we can't capture in this direction.  we'll move on to the next one
                continue
            # keep going until we hit our own piece
            while self.index(i, j) == -id:
                i, j = xop(i), yop(j)
            # if we found a piece of our own color, then this is a valid move
            if self.index(i, j) == id:
                k, l = xop(x), yop(y)
                # go back and flip all the pieces to my color
                while k != i or l != j:
                    self.state[k + l * 10] = id
                    k, l = xop(k), yop(l)

    # returns a list of all valid x,y moves for a given id
    def validmoves(self, id):
        moves = []
        for x in range(10):
            for y in range(10):
                if self.canplace(x, y, id):  # Within the board, we need to check if it is a place we can actually place
                    moves = moves + [(x, y)]  # if we can place it there, we'll add it to the list we're going to return
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
        # No more empty spaces left on the board
        if not 0 in self.state:
            return True
        # No one can make a valid move, game is over
        elif len(self.validmoves(1)) == 0 and len(self.validmoves(-1)) == 0:
            return True
        else:
            return False


    # have the board and player as a parameter
    # check to see if the player has any pieces in the corners of the board (can have simple if statements for each)
    # check number of spaces available
    # check num of moves that force an opponent to lose a turn
    # can do this by calling canplace for player then for opponent and seeing if the num of moves == 0

    # Does the move create a heuristic, loop through moves in game or wherever, then call heuristic, then make a move depending on the highest value
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
            # check number of edges taken by the player
            # in our for loops, we need to exclude corner points
            for x in range(1, 9):  # loop from 1 to 8

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


    # I need to "make the move", then see the valid moves that my opponent has

    # Might need to make a method where I pass in a board, x, y, and id and return that board after the move is made.

    # Greedy player - look at all the moves, then return the move that grants the player the largest number of pieces
    # Perform the greedy action inside of greedy_player, so you can easily turn it off inside of game()

    def score(self, id):
        value = 0
        for i in range(100):
            if self.state == id:
                value = value + 1
        return value

    # 3 3 3, it's just going to find where the top numbers stop and then pick one, let me just pick the first one.
    def greedy_player(self, id):
        moves = self.allmoves(id)

        # Give all the moves an attaching score, so make a tuple
        for i in range(len(moves)):
            moves[i] = (
            moves[i].score(id), moves[i])  # Making moves a list of tuples with a score and board (with the move)
        moves.sort(reverse=True, key=lambda x: x[
            0])  # Sorting the moves in reverse, so biggest comes first, but i'm sorting it via the scores only x[0]
        # we need to pick the best move
        bestmove = moves[0][
            1]  # moves[0][1] look to the zeroth tuple in my list, then pick the 2nd thing inside the tuple
        return bestmove  # returning the tuple of (x,y)

    def ndepth_minimax(self, id, n, recursive_call=False):
        # Get all possible moves for the player
        movelist = self.allmoves(id)

        for i in range(len(movelist)):
            # for each board here, call the allmoves function for the opponent to look at the retaliation of that particular move
            opponentmoves = movelist[i].allmoves(-id)
            # if this move ends the game, this is the best move, so put it in your movelist with the score
            if movelist[i].end():
                # make your move into a tuple that stores the score and the move (board) itself
                movelist[i] = (movelist[i].score(id), movelist[i])

            # if the opponent has no counter moves, then this is the next best move besides end game, make that move!
            elif len(opponentmoves) == 0:
                movelist[i] = (movelist[i].score(id), movelist[i])

            # else, we need to gather all the opponent's opposing moves and check which one is the worst.
            else:
                # get ALL the opponent moves for the specific move i did, not all in general
                for j in range(len(opponentmoves)):
                    # Need to check OUR counter moves to these moves, check same conditions as above, then recursion.
                    if opponentmoves[j].end():
                        opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                    # check if any possible moves for opposite player based on this j board atm
                    elif len(opponentmoves[j].allmoves(id)) == 0:
                        opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                    else:
                        # check depth first, if no depth, then just exit out, no recursion needed
                        if n == 0:
                            opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                        else:
                            # Make separate variable for opponent score
                            # If n != 0, we need to call function again to gather the next move, and the next one and so on until we reach the depth we want
                            opponent_score = opponentmoves[j].ndepth_minimax(id, n=n-1, recursive_call=True)
                            opponentmoves[j] = (opponent_score, opponentmoves[j])

                # we want opponent's worst score based on THE OTHER PLAYER, so we'll want to worst one (reverse=false)
                # picking the worst one means we'll get the best one for the opposite player
                opponentmoves.sort(reverse=False, key=lambda x: x[0])
                movelist[i] = (opponentmoves[0][0], movelist[i])


        # We now have all our moves, so we need to sort them based on score and return the best move
        movelist.sort(reverse=True, key=lambda x: x[0])
        bestmove = movelist[0][1]
        if recursive_call == True:
            return movelist[0][0]
        else:
            return bestmove


    def onedepth_minimax(self, id):
        # Get all possible moves for the player
        movelist = self.allmoves(id)

        for i in range(len(movelist)):
            # for each board here, call the allmoves function for the opponent to look at the retaliation of that particular move
            opponentmoves = movelist[i].allmoves(-id)
            # if this move ends the game, this is the best move, so put it in your movelist with the score
            if movelist[i].end():
                # make your move into a tuple that stores the score and the move (board) itself
                movelist[i] = (movelist[i].score(id), movelist[i])

            # if the opponent has no counter moves, then this is the next best move besides end game, make that move!
            elif len(opponentmoves) == 0:
                movelist[i] = (movelist[i].score(id), movelist[i])

            # else, we need to gather all the opponent's opposing moves and check which one is the worst.
            else:
                # get ALL the opponent moves for the specific move i did, not all in general
                for j in range(len(opponentmoves)):
                    # Get the scores of all the opponent's moves, then get the worst ones.
                    # if -id's worst moves are our best moves, then based on the opponent's moves, we want to get our best score
                    opponentmoves[j] = (opponentmoves[j].score(id), opponentmoves[j])
                opponentmoves.sort(reverse=False, key=lambda x: x[0])
                # we want to see what the score will be if the opponent makes a move (so we must pass in our id)
                # we look at the first score of opponentmoves (which is the smallest but it's the smallest score that WE WILL GET)
                # take the first move because that is what gives us our smallest and weakest move of ours

                movelist[i] = (opponentmoves[0][0], movelist[i])
        # We now have all our moves, so we need to sort them based on score and return the best move
        movelist.sort(reverse=True, key=lambda x: x[0])
        bestmove = movelist[0][1]
        return bestmove


# this plays a game between two players that will play completely randomly
def game():
    # make the starting board
    board = Board()
    # start with player 1
    turn = 1
    print("Which optimization would you like for X?")
    answer1 = input("Heuristic, 0-depth, 1-depth, 2-depth, n-depth, None (greedy only): ")
    if answer1 == "n-depth":
        n1 = int(input("Specify depth "))
    print("Which optimization would you like for O?")
    answer2 = input("Heuristic, 0-depth, 1-depth, 2-depth, n-depth, None (greedy only): ")
    if answer2 == "n-depth":
        n2 = int(input("Specify depth "))
    while True:

        # get the moves
        movelist = board.validmoves(turn)
        # no moves, skip the turn
        if len(movelist) == 0:
            turn = -turn
            continue


        # pick a move totally at random
        i = random.randint(0, len(movelist) - 1)
        # make a new board
        board = board.copy()

#        board = board.greedy_player(turn)
#        board = board.heuristic(turn)

        # X uses one-depth

        if turn == 1:
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

        # O uses greedy
        elif turn == -1:
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



        # swap players
        turn = -turn
        # print
        board.printboard()
        # wait for user to press a key
        input()
        # game over? stop.
        if board.end():
            break

    gamescore = board.evaluate()
    if gamescore > 0:
        print("Score is", gamescore, ". X won!")
    elif gamescore < 0:
        print("Score is", gamescore, ". O won!")
    else:
        print("Score is 0. Tied game!")

game()
