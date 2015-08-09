from random import randint
from sys import exit

class Board(object):
	"""This class creates the board - its size and condition"""
	board = []
	def __init__(self, size):
		self.size = size
		while(self.size < 2):
			self.size = int(raw_input("Invalid board size! Enter again : "))
		
	def create_board(self):
		for x in range(self.size):
			self.board.append(["O"] * self.size)
			
	def print_board(self):
		print "\n"
		for row in self.board:
			print " ".join(row)
		print "\n"
			
class Ship(object):
	"""This class creates the ship"""
	ship_row = 0
	ship_col = 0
	def __init__(self, board, size, id):
		self.board = board
		self.size = size
		self.id = id
		self.ship_row = randint(0, len(self.board) - 1)
		self.ship_col = randint(0, len(self.board[0]) - 1)

	def set_ship_pos(self):
		return { "ship_id" : self.id,
				 "ship_row" : self.ship_row,
				 "ship_col" : self.ship_col }

class Player(object):
	"""This class creates the player """
	def __init__(self, id):
		self.id = id
		self.name = raw_input("Enter name : ")
		
	def guess_pos(self):
		row = int(raw_input("Guess Row:"))
		col = int(raw_input("Guess Col:"))
		return row, col
		
	def __repr__(self):
		return "%s" % (self.name)
		
class Game(object):
	"""This class sets the game play"""
	turn = 1 # default turn
	scenario = { "win" : "Congratulations %s! You sunk my battleship!",
				"invalid" : "Oops, that's not even in the ocean.",
				"repeat" : "You guessed that one already.",
				"miss" : "You missed the ship.",
				"destroy" : "Ship %d destroyed!",
				"lose" : "Game over..."
				} 
	
	def __init__(self, turn):
		self.turn = turn
	
	def update_turn(self):
		if self.turn == 0: # no more turn left
			print "Sorry, you are out of turn!"
			return False
		else:
			print "You have %d more turn" % int(self.turn)
			self.turn -= 1
			return True
			
	def outcome(self, action):
		self.action = action
		return self.scenario[self.action]
		
def main():
	print "\nWelcome to the Battleship Game!"
	print "-" * 40
	option = raw_input("\nStart new game (Y/N)?")
	if option != 'Y':
		print "See you again..."
		raw_input("")
		exit(0)
	else:
		# Setting up board parameters
		board_size = int(raw_input("Enter your board size : "))
		board = Board(board_size)
		board.create_board()
		
		# Setting up ships parameters
		shiplist = []
		ship_num = int(raw_input("Enter how many enemy ships should exist : "))
		while ship_num > board_size / 2: 
			ship_num = int(raw_input("Too many ships in the board. Enter new value : "))
		for i in range(ship_num):
			ship = Ship(board.board, 1, i+1)
			shiplist.append(ship.set_ship_pos())
		print "Ships loc: ", shiplist
		
		# Setting up turn count parameters
		turn_value = int(raw_input("Enter how many turn to try : "))

		# Setting up players parameters
		playerlist = []
		player_num = int(raw_input("Enter how many player : "))
		for i in range(player_num):
			player = Player(i+1)
			playerlist.append(player)
		print "Players : ", playerlist

		game = Game(turn_value)
		while game.update_turn():
			for player in playerlist:
				print "Hi %s, it's your turn!" % (player.name)
				board.print_board()
				guess_row, guess_col = player.guess_pos()
				guess_turn = False
				
				for each_ship in shiplist: # checking each ship's location
					if guess_row == each_ship["ship_row"] and guess_col == each_ship["ship_col"]:
						print game.outcome("destroy") % (each_ship["ship_id"])
						shiplist.remove(each_ship)
						guess_turn = True
				if len(shiplist) == 0: # no more ship left
					print game.outcome("win") % player.name
					raw_input("")
					exit(0)
				else:
					if (guess_row < 0 or guess_row > (int(board_size) - 1)) or \
						(guess_col < 0 or guess_col > (int(board_size) - 1)):
						print game.outcome("invalid")
					elif(board.board[guess_row][guess_col] == "X"):
						print game.outcome("repeat")
					elif not guess_turn:
						print game.outcome("miss")
						board.board[guess_row][guess_col] = "X"
					else:
						board.board[guess_row][guess_col] = "-"
		else:
			print game.outcome("lose")
			raw_input("")

main()