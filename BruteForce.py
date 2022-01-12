import numpy as np
import time
import CurrentPlace

from BoardOperations import BoardOps
from Interactive import Draw

class Brute:
	"""
	Systematically try filling in numbers until a valid sudoku is produced.
	Guaranteed to find a solution! (If there is one)
	"""
	def __init__(self, b, verbose=False, interactive=False):
		self.board = b
		self.size = len(b)
		self.ops = BoardOps(self.board)
		self.history = []
		self.n = 0
		self.verbose = verbose
		self.interactive = interactive
		if self.interactive:
			self.D = Draw(self.size)
			self.D.FillFromBoard(self.board, update=False)

	def try_val(self, row, col, val):
		# Attempt to place val at row, col; and check if it is valid.
		open = self.ops.read(row, col)
		if open == 0:
			board_init = np.array(self.board)
			if self.verbose:
				print(f"Trying {val} at row {row}, col {col}")
			self.ops.place(row, col, val)
			if self.interactive:
				self.D.enterNumber(val, row, col, color=self.D.pink)
			self.n += 1
			check_row = self.ops.checkline(self.ops.selectrow(row, col))
			check_col = self.ops.checkline(self.ops.selectcol(row, col))
			check_box = self.ops.checkline(self.ops.selectbox(row, col))
			##if any of these is 0, then sudoku rules are violated.
			if check_row and check_col and check_box:
				return 1
			else:
				# Replace row, col with 0 again as val did not fit.
				self.ops.place(row, col, 0)
				return 0
		else:
			return -1
	def pop(self):
		# remove and return the most recent addition to the history
		fst = self.history[0]
		self.history = self.history[1:]
		return fst
	def push(self, lst):
		# add a placement to the history
		self.history = [lst]+self.history
	def go(self):
		self.ops.printboard()
		if self.verbose:
			input("\nReady? Set? Press anything to go!\n")
		ti = time.perf_counter()
		original = self.board
		# Begin from the upper-left side of the board
		r = 0
		c = 0
		v = 1
		while r<self.size:
			c = 0
			while c<self.size:
				v = 1
				while v<(self.size+1):
					res = self.try_val(r, c, v)
					if res == 1:
						# Valid placement
						if self.verbose:
							print("This placement was good :)")
						self.push([r, c, v])
					elif res == 0:
						# Invalid placement
						if self.verbose:
							print("This placement was bad :(")
						while v == self.size:
							# If we've reached the maximum number, then nothing fit in this square
							if self.verbose:
								print("Nothing fit here :|")
							if self.interactive:
								#cover with white
								self.D.enterNumber(0, r, c, color=self.D.white)
							## Have to go back using history
							if self.history == []:
								print('Unsolvable ;(')
								exit()
							else:
								# Recover the last row, col, and val we placed a number at
								[lr, lc, lv] = self.pop()
								if self.verbose:
									print(f"Backtracking to row {lr}, col {lc}, value {lv}")
								r = lr
								c = lc
								v = lv
								self.ops.place(r, c, 0)
					v += 1
				c += 1
			r += 1
		tf = time.perf_counter()
		dt = tf - ti
		print(f"\n\nTime to brute force: {round(dt,5)} s.")
		print(f"There were {self.n} attempted placements!")
		return self.board
