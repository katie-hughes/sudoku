import numpy as np
from Interactive import Draw

class BoardOps:
	"""
	Functions that deal with the setup & organization of the sudoku board.
	The board is represented as an N x N numpy array.
	All updates to the board should be done through this class.
	"""
	def __init__(self, board, interactive=None):
		self.board = board
		self.size = len(board)
		self.sqt = int(np.sqrt(self.size))
		self.interactive = interactive
	def printnum(self,num):
		if num < 10:
			return str(num)
		else:
			return chr(ord('@')-9+num)
	def fill(self):
		print("Please enter in the known numbers by row, from left to right,"),
		print("separated by spaces (for an empty square, type 0)")
		while True:
			for x in range(self.size):
				while True:
					try:
						print(f"Row {x+1}", end=''),
						s = input(": ")
						numbers = list(map(int, s.split()))
						if len(numbers) != self.size:
							print(f"Input should contain {self.size} numbers.")
						else:
							numbers = np.array(numbers)
							max = numbers.max()
							min = numbers.min()
							if max>self.size or min<0:
								print(f"All numbers in the row must be between 1 and {self.size}! Try again.")
							else:
								self.board[x] = numbers
								break
					except ValueError:
						print("Unrecognized input. Try again!")
			self.printboard()
			print("^ ^ ^ Is this the correct board?")
			print("Press 1 to re-input your numbers,"),
			mistake = input("or any other key to continue: ")
			try:
				mistake = int(mistake)
				if mistake == 1:
					pass
			except ValueError:
				break
		return self.board
	def printboard(self):
		for x in range(self.size):
			if np.mod(x, self.sqt) == 0:
				print(" ", end = '')
				for z in range(self.size):
					print("_ ", end = '')
				print("\n", end = '')
			for y in range(self.size):
				num = self.board[x][y]
				if np.mod(y, self.sqt) == 0:
					print("|", end = '')
				else:
					print(" ", end = '')
				if num == 0:
					print(" ", end = '')
				else:
					print(self.printnum(num), end = '')
				if y == (self.size-1):
					print("|", end = '')
			if x == (self.size-1):
				print("\n", end = '')
				print(" ", end = '')
				for z in range(self.size):
					print("_ ", end = '')
			print(" ")
	def countarray(self, arr, num):
		return np.count_nonzero(np.array(arr) == num)
	def checkline(self, arr):
		for x in range(1, self.size+1):
			count = self.countarray(arr, x)
			if count > 1:
				return 0
		return 1
	def sanitycheck(self):
		if np.any(self.board > self.size):
			return 0
		for x in range(self.size):
			row = self.board[x]
			res = self.checkline(row)
			if res == 0:
				return 0
		transp = np.transpose(self.board)
		for y in range(self.size):
			col = transp[y]
			res = self.checkline(col)
			if res == 0:
				return 0
		for w in range(self.sqt):
			for x in range(self.sqt):
				box = np.zeros(self.size, dtype=int)
				count = 0;
				for y in range(self.sqt):
					for z in range(self.sqt):
						num = self.board[self.sqt*w+y][self.sqt*x+z]
						box[count] = num
						count += 1
				count = 0
				res = self.checkline(box)
				if res == 0:
					return 0
		return 1
	def selectrow(self, row, col):
		return self.board[row]
	def selectcol(self, row, col):
		transp = np.transpose(self.board)
		return transp[col]
	def selectbox(self, row, col):
		r = row //self.sqt
		c = col //self.sqt
		box = np.zeros(self.size, dtype=int)
		count = 0
		for x in range(self.sqt):
			for y in range(self.sqt):
				num = self.board[self.sqt*r+x][self.sqt*c+y]
				box[count] = num
				count += 1
		return box
	def update(self, board):
		self.board = board
	def checkdone(self):
		for r in range(self.size):
			for c in range(self.size):
				if self.board[r][c] == 0:
					return 0
		return 1
	def isdone(self):
		done = self.checkdone()
		sc = self.sanitycheck()
		if done and sc:
			print("\n\nSolved! Hooray!")
			self.printboard()
			exit()
	def place(self, row, col, val):
		self.board[row][col] = val
	def read(self, row, col):
		return self.board[row][col]
