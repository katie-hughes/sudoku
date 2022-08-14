import numpy as np

from Interactive import Draw

class Possibilities:
	"""
	Operations for creating and updating the possible numbers associated with the board.
	poss[x][y] is a list of possible numbers that could fit in board[x][y] .
	Any updates to the possibilities list should be done through this class.
	"""
	def __init__(self,board,ops,verbose=False,interactive=False):
		self.board = board
		self.size = len(board)
		self.sqt = int(np.sqrt(self.size))
		self.poss = []
		self.changes = 0
		self.verbose = verbose
		self.interactive = interactive
		self.ops = ops
		for x in range(self.size):
			self.poss.append([])
			for y in range(self.size):
				self.poss[x].append([])
		for x in range(self.size):
			for y in range(self.size):
				num = self.ops.read(x,y)
				# If the current square is empty:
				if num == 0:
					row = self.ops.selectrow(x, y)
					col = self.ops.selectcol(x, y)
					box = self.ops.selectbox(x, y)
					options = list(range(1, self.size+1))
					for z in range(1, self.size+1):
						# count occurences of each number in row/col/box
						cr = self.ops.countarray(row, z)
						cc = self.ops.countarray(col, z)
						cb = self.ops.countarray(box, z)
						if ((cr == 1) or (cc == 1) or (cb == 1)):
							options.remove(z)
							self.changes += 1
					self.poss[x][y] = options
		if self.verbose:
			print(self.changes, 'numbers eliminated from the possibilities list.')

	# Return a list of lists representing the possibilities for the row/col/box
	def poss_row(self, index):
		return self.poss[index]
	def poss_col(self, index):
		col_poss = []
		for x in range(self.size):
			col_poss.append(self.poss[x][index])
		return col_poss
	def poss_box(self, index):
		r = index // self.sqt
		c = index % self.sqt
		box_poss = []
		for x in range(self.sqt):
			for y in range(self.sqt):
				p = self.poss[self.sqt*r+x][self.sqt*c+y]
				box_poss.append(p)
		return box_poss

	# Remove num from the possibilities of a row/col/box
	def remove_poss_row(self, index, num):
		for x in range(self.size):
			p = self.poss[index][x]
			if num in p:
				p.remove(num)
				self.poss[index][x] = p
	def remove_poss_col(self, index, num):
		for x in range(self.size):
			p = self.poss[x][index]
			if num in p:
				p.remove(num)
				self.poss[x][index] = p
	def remove_poss_box(self, index, num):
		r = index // self.sqt
		c = index % self.sqt
		for x in range(self.sqt):
			for y in range(self.sqt):
				p = self.poss[self.sqt*r+x][self.sqt*c+y]
				if num in p:
					p.remove(num)
					self.poss[self.sqt*r+x][self.sqt*c+y] = p

	# Count the number of occurances of a number in a possibilities row/col/box
	def occurences(self, lst, number):
		count = 0
		for x in range(self.size):
			for n in lst[x]:
				if n == number:
					count += 1
		return count
	# Convert row/col to a box number (1-Size)
	def box_index(self, row, col):
		r = row // self.sqt
		c = col // self.sqt
		return self.sqt*r+c
	# Place number and update possibilities list accordingly
	def place(self, num, row, col, color=None):
		if self.verbose:
			print("Placing ", num, " on row ", row, ", col ", col, sep='')
		if self.ops.read(row, col) != 0:
			print("\nThis board has no possible solution. Goodbye :( ")
			exit()
		else:
			self.ops.place(row, col, num, color=color)
			self.poss[row][col] = []
			self.remove_poss_row(row, num)
			self.remove_poss_col(col, num)
			self.remove_poss_box(self.box_index(row, col), num)
