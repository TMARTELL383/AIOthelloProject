-----OTHELLO A.I.-----

-----By: Tyler Martell-----

-----README.txt-----

-----What I have done so far-----

I have completed n-depth minimax where the depth is specified by the user (depth 2 is done with this). I have implemented the heuristic, but have not implemented a seen-list
or alpha-beta pruning.


-----Introduction-----

This Othello program has two computer players play the board game, Othello, against each other (X and O). There are various methods and strategies each A.I. can be programmed to perform such as
playing greedy (making the move that grants the most number of flips - this will not always be the best move), using a heuristic that values edges and corners more than other moves in 
the middle of the board, and depth searches of 1 or more.


-----How it Works-----

game() is the main function where the game starts. The user will be asked which optimizations they want for each A.I. player (heuristic, 0-depth, 1-depth, 2-depth, n-depth, or none). After
they choose, the game will begin, printing the current board to the console. X will go first and will call the respective function depending on the optimization chosen. O will go next, and,
just like X, it will call the appropriate function for its optimization. The two players will battle back and forth until the board is filled or there are no more turns left to be made by
either player. A score will be reported to the console with the winner announced.



-----Details of each function-----

__init__(self):

	Constructor of the Board class that initializes the board we use.

evaluate(self):

	Evaluates the board to determine the overall score of the game between the two players.

copy(self):

	Makes a copy of an existing board and returns it.

index(self, x, y):

	Returns the board state position given an x and y coordinate.

canplace(self, x, y, id):

	Given an x, y, and id (which determines which computer player is going), this function looks to see if this move can be done or not. It looks at the surrounding pieces (in all eight
	directions) to see if there are any pieces of the opposite player (O looks for X, and X looks for O). In a particular direction, if there is a single piece or multiple pieces of the
	opposite player's, followed by the current player's own piece, the current player can place their piece at that location, returning true. Otherwise, it will return false.

place(self, x, y, id):

	Places a piece at the given x,y coordinate, modifying the state of the board object of our game.

validmoves(self, id):

	Returns a list of valid moves based on the state of the board.

allmoves(self, id):

	Returns a list of boards after a paricular move has been made.

printboard(self):

	Prints out the board.

end(self):

	Determines if the game is over or not. This function looks at the state of the board to see if there is a 0 (empty space). If that isn't the case, it will also look to see if any
	of the players can make validmoves. If both cannot, the game is over and this function will return a true. If none of these conditions are met, the game is still going on, so a
	false will be returned.

heuristic(self, id):

	This is one of the A.I. optimizations. It compiles a list of allmoves for a particular player, goes through each potential move, and determines which move is best depending on a
	heuristic. The heuristic is giving more "points" (i.e. a better score) to moves that capture an edge on the board (1 point) or a corner (10 points). Since corners cannot be
	captured from any direction, they are worth more points than edges. The list of moves is made into a tuple with a score as the first component and is sorted from best to worst 
	score. The move with the best score is returned and that move is used by the player.

score(self, id):

	Determines the score of a particular player and returns the value.

greedy_player(self, id):

	This is one of the A.I. optimizations. It gathers a list of allmoves for a particlar player, goes through each move, and determines a score. The move with the biggest score is
	returned and used by the player.

ndepth_minimax(self, id, n, recursive_call=False):

	This is one of the A.I. optimizations. It compiles a list of allmoves for the current player. For each of those moves, it then gathers a list of the opponents moves. The scores 
	for each opponent move are found. If n does not equal 0, the function is recursively called with n being 1 less. This will continue to occur until n = 0. The opponent's worst
	score is considered because that means it is would be the best move for the current player. These opponent scores are placed into the current player's movelist. The list is sorted
	by score and the move with the best score for the current player is returned.

onedepth_minimax(self, id):

	This is one of the A.I. optimizations. It functions exactly the same as ndepth_minimax(), but with this method, the depth is only 1, so the opponent's moves for each of the current
	player's moves are looked at. The function does not go any deeper. The move with the best score for current player (i.e. the worst score for the opponent player) is returned.

game():

	Runs the game until there is a winner or there are no valid moves left to be made by either player.














