#!/usr/bin/env python

from random import randint
from sys import exit
import os

class Board(object):
	"""This class creates the board - its size and condition"""
	board = []
	# Initialize the board size and ensure it's valid
	def __init__(self, size):
		self.size = size
		while(self.size < 2):
			self.size = int(raw_input("Invalid board size! Enter again : "))

	# Build the board based on size given
	def create_board(self):
		for x in range(self.size):
			# Set 'O' as the base value 
			self.board.append(["O"] * self.size)
			
	# Display the board and its current values
	def print_board(self):
		print "\n"
		for row in self.board:
			print "   ", " ".join(row)
		print "\n"
			
class Ship(object):
	"""This class creates the ship size and its random position"""
	ship_pos = []
	# Initialize the board and set its max size
	def __init__(self, board, size, id):
		self.board = board
		self.size = size
		if self.size > 2:
			print "No bigger size. Set to 2 max"
			self.size = 2
		self.id = id

	# Set the random position of the ship
	def set_ship_pos(self):
		row = randint(0, len(self.board) - self.size)
		col = randint(0, len(self.board[0]) - self.size)
		pos = '%d:%d' % (row, col)
		self.ship_pos = [pos]
		if self.size == 2: # special mapping for big size ship
			pos = '%d:%d' % (row+1, col)
			self.ship_pos.append(pos)
			pos = '%d:%d' % (row, col+1)
			self.ship_pos.append(pos)
			pos = '%d:%d' % (row+1, col+1)
			self.ship_pos.append(pos)
		return { "ship_id" : self.id,
				 "ship_pos" : self.ship_pos
				}

class Player(object):
	"""This class creates the player """
	# Initialize the player characters
	def __init__(self, id):
		self.id = id
		self.name = raw_input("Enter name : ")
		print "Hi %s! Welcome to the game\n" % (self.name)

	# Inquire and keep the position given by player
	def guess_pos(self):
		row = val_input("Guess Row:")
		col = val_input("Guess Col:")
		return row, col

	# Display representation of player
	def __repr__(self):
		return "%s" % (self.name)
		
class Game(object):
	"""This class sets the game play"""
	turn = 1 # default turn
	# collection of appropriate messages to print based on scenario met
	scenario = { "win" : "Congratulations %s! You sunk my battleship!",
				"invalid" : "Oops, that's not even in the ocean.",
				"repeat" : "You guessed that one already.",
				"miss" : "You missed the ship.",
				"minor" : "You got part of the ship. Guess again.",
				"destroy" : "Ship %d destroyed!",
				"lose" : "Game over..."
				} 

	# initialize the current turn
	def __init__(self, turn):
		self.turn = turn

	# keep track of current turn
	def update_turn(self):
		if self.turn == 0: # no more turn left
			print "Sorry, you are out of turn!"
			return False
		else:
			print "You have %d more turn" % int(self.turn)
			self.turn -= 1
			return True

	# display appropriate message based on scenario met
	def outcome(self, action):
		self.action = action
		return self.scenario[self.action]

def display_header():
	"""This function serves to clear screen and display header for the game"""
	os.system('cls')
	print "-" * 35
	print "\n the Battleship Game!".upper()
	print "-" * 35
	return True

def val_input(prompt):
	"""This function validates the input user entered and return value in integer"""
	# convert user input string into equivalent integer value
	user_input = 0
	while True:
		try:
			user_input = int(raw_input(prompt))       
		except ValueError:
			print("Invalid integer value!")
			continue
		else:
			return user_input
	
def main():
	"""Main function to play the game"""
	display_header()
	option = raw_input("\nStart new game (Y/N)?")
	if option != 'Y':
		print "See you again..."
		raw_input("")
		exit(0)
	else:
		# Setting up board parameters
		board_size = val_input("\nEnter your board size : ")
		board = Board(board_size)
		board.create_board()
		
		# Setting up ships parameters
		shiplist = []
		ship_num = val_input("Enter how many enemy ships to battle : ")
		while ship_num > board_size / 2: 
			ship_num = val_input("Too many ships in the board. Enter new value : ")
		ship_size = val_input("Choose small(1) or big(2) ship : ")
		for i in range(ship_num):
			ship = Ship(board.board, ship_size, i+1)
			shiplist.append(ship.set_ship_pos())
		
		# Setting up turn count parameters
		turn_value = val_input("Enter how many turn to try : ")

		# Setting up players parameters
		playerlist = []
		player_num = val_input("Enter how many player : ")
		for i in range(player_num):
			player = Player(i+1)
			playerlist.append(player)

		# Mark the start of the game
		raw_input('\nAll settings done. Press enter to continue...\n')
		display_header()
		
		# Setting up the game based on current turn and players
		game = Game(turn_value)
		while game.update_turn():
			for player in playerlist:
				board.print_board()
				print "Go %s, put your guess!\n" % (player.name)
				guess_row, guess_col = player.guess_pos()
				guess_pos = '%d:%d' % (guess_row, guess_col)
				guess_turn = False # set to False since no ship has been destroyed yet
				
				### debugging only: print "Ships loc: ", shiplist
				for each_ship in shiplist: # checking each ship's location
					# compare position guessed by player with one or more ships location
					# if matched, the ship will be destroyed ie. removed from the battleship
					if guess_pos in each_ship["ship_pos"]:
						each_ship["ship_pos"].remove(guess_pos)
						guess_turn = True # set to True due to successful guess
						# check if the ship is completely destroyed
						# else, display message to remind player to keep guessing
						if len(each_ship["ship_pos"]) == 0:
							print game.outcome("destroy") % (each_ship["ship_id"])
							shiplist.remove(each_ship)
						else:
							print game.outcome("minor")
				# check if entire battleship has been destroyed ie. full game completion
				if len(shiplist) == 0: 
					print game.outcome("win") % player.name
					raw_input("")
					exit(0)
				else:
					# display invalid message for position guessing which outside board coordinates
					if (guess_row < 0 or guess_row > (int(board_size) - 1)) or \
						(guess_col < 0 or guess_col > (int(board_size) - 1)):
						print game.outcome("invalid")
					# display message for guess of position which has already guessed before
					elif(board.board[guess_row][guess_col] == "X" or \
						board.board[guess_row][guess_col] == "-") :
						print game.outcome("repeat")
					# mark the board to 'X' for any unsuccessful guess
					elif not guess_turn:
						print game.outcome("miss")
						board.board[guess_row][guess_col] = "X"
					# mark the board to '-' for any correct guess ie. ship is hit not yet destroyed
					else:
						board.board[guess_row][guess_col] = "-"
						
					raw_input("Press enter to continue...\n")
			display_header()
		# display lose message if turn has expired
		else:
			print game.outcome("lose")
			raw_input("")

# Standard call to the main() function to begin the program.
if __name__ == '__main__':
	main()