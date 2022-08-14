import numpy as np
from itertools import combinations
import time

from BoardPossibilities import Possibilities

class Methods:
	"""
	Uses the possibilities for each square to determine number placement.
	Is not guaranteed to completely solve the sudoku.
	"""
	def __init__(self, board, ops, verbose=False, interactive=False):
		self.board = board
		self.size = len(board)
		self.sqt = int(np.sqrt(self.size))
		self.ops = ops
		self.P = Possibilities(board, ops, verbose=verbose, interactive=interactive)
		self.n = 0
		self.verbose = verbose
		self.interactive = interactive
		self.lightgreen = (153,255,170)
	def naked_single(self):
		# Check if there is only one option in the possibilities list
		ret = 0
		for x in range(self.size):
			for y in range(self.size):
				if len(self.P.poss[x][y]) == 1:
					num = self.P.poss[x][y][0]
					if self.verbose:
						print("Naked Single: ", end="")
					self.P.place(num, x, y, color=self.lightgreen)
					self.n += 1
					ret += 1
		return ret
	def hidden_single(self):
		# Check if a number can only go in one spot in a row/col/box
		ret = 0
		# Check rows
		for x in range(self.size):
			row_poss = self.P.poss_row(x)
			# Count the occurences of each number in possibilities list.
			for n in range(1, self.size+1):
				count = self.P.occurences(row_poss, n)
				if count == 1:
					# Find the corresponding square.
					for z in range(self.size):
						if n in row_poss[z]:
							if self.verbose:
								print("Hidden Single (row): ", end="")
							self.P.place(n, x, z, color=self.lightgreen)
							self.n += 1
							ret += 1
							break
		# Check cols
		for x in range(self.size):
			col_poss = self.P.poss_col(x)
			for n in range(1, self.size+1):
				count = self.P.occurences(col_poss, n)
				if count == 1:
					for z in range(self.size):
						if n in col_poss[z]:
							if self.verbose:
								print("Hidden Single (col): ", end="")
							self.P.place(n, z, x, color=self.lightgreen)
							self.n += 1
							ret += 1
							break
		# Check boxes
		for w in range(self.sqt):
			for x in range(self.sqt):
				box_poss = self.P.poss_box(self.sqt*w+x)
				for n in range(1, self.size+1):
					count = self.P.occurences(box_poss, n)
					if count == 1:
						index = 0
						for a in range(self.size):
							if n in box_poss[a]:
								index = a
						itr = 0
						for b in range(self.sqt):
							for c in range(self.sqt):
								if itr == index:
									if self.verbose:
										print("Hidden Single (box): ", end="")
									self.P.place(n, self.sqt*w+b, self.sqt*x+c, color=self.lightgreen)
									self.n += 1
									ret += 1
								itr += 1

		return ret
	def poss_manip(self):
		count = 0
		# Check rows
		for x in range(self.size):
			row_poss = self.P.poss_row(x)
			indices = []
			poss2 = []
			for p in range(self.size):
				if len(row_poss[p]) == 2:
					indices.append(p)
					poss2.append(row_poss[p])
			###indices contains a list of the indices in row with 2 elements
			###poss2 contains a list of the possibilities in row with 2 elements.
			comb_indices = list(combinations(indices, 2))
			comb_poss2 = list(combinations(poss2, 2))
			##these are lists of tuples of all the combinations between 2 element pieces
			for c in range(len(comb_indices)):
				first = comb_poss2[c][0]
				second = comb_poss2[c][1]
				##print("comb is", first, second)
				if first == second:
					n0 = first[0]
					n1 = first[1]
					if self.verbose:
						print(f"Removing {n0} and {n1} from row {x}.")
					i0 = comb_indices[c][0]
					i1 = comb_indices[c][1]
					##these are the indices I want to step over.
					for s in range(self.size):
						if s!=i0 and s!=i1:
							if n0 in self.P.poss[x][s]:
								self.P.poss[x][s].remove(n0)
								count += 1
							if n1 in self.P.poss[x][s]:
								self.P.poss[x][s].remove(n1)
								count += 1
					self.naked_single()
					break
		# Check cols
		for x in range(self.size):
			col_poss = self.P.poss_col(x)
			indices = []
			poss2 = []
			for p in range(self.size):
				if len(col_poss[p]) == 2:
					indices.append(p)
					poss2.append(col_poss[p])
			comb_indices = list(combinations(indices, 2))
			comb_poss2 = list(combinations(poss2, 2))
			for c in range(len(comb_indices)):
				first = comb_poss2[c][0]
				second = comb_poss2[c][1]
				if first == second:
					n0 = first[0]
					n1 = first[1]
					if self.verbose:
						print(f"Removing {n0} and {n1} from col {x}.")
					i0 = comb_indices[c][0]
					i1 = comb_indices[c][1]
					for s in range(self.size):
						if s != i0 and s!=i1:
							if n0 in self.P.poss[s][x]:
								self.P.poss[s][x].remove(n0)
								count += 1
							if n1 in self.P.poss[s][x]:
								self.P.poss[s][x].remove(n1)
								count += 1
					self.naked_single()
					break
		# Check box
		for x in range(self.size):
			box_poss = self.P.poss_box(x)
			indices = []
			poss2 = []
			for p in range(self.size):
				if len(box_poss[p]) == 2:
					indices.append(p)
					poss2.append(box_poss[p])
			comb_indices = list(combinations(indices, 2))
			comb_poss2 = list(combinations(poss2, 2))
			for c in range(len(comb_indices)):
				first = comb_poss2[c][0]
				second = comb_poss2[c][1]
				if first == second:
					n0 = first[0]
					n1 = first[1]
					if self.verbose:
						print(f"Removing {n0} and {n1} from box {x}.")
					i0 = comb_indices[c][0]
					i1 = comb_indices[c][1]
					r = x // self.sqt
					c = x % self.sqt
					itr = 0
					for s in range(self.sqt):
						for t in range(self.sqt):
							if (itr != i0) and (itr != i1):
								poss = self.P.poss[self.sqt*r+s][self.sqt*c+t]
								if n0 in poss:
									self.P.poss[self.sqt*r+s][self.sqt*c+t].remove(n0)
									count += 1
								if n1 in poss:
									self.P.poss[self.sqt*r+s][self.sqt*c+t].remove(n1)
									count += 1
							itr += 1
					self.naked_single()
					break
		return count
	def go(self):
		if self.verbose:
			input("\nReady? Set? Press anything to go!\n")
		ret = 1
		ti = time.perf_counter()
		# Continue running methods until no more updates are made to the board / poss list
		while ret != 0:
			ret = self.naked_single()
			ret += self.hidden_single()
			ret += self.poss_manip()
		tf = time.perf_counter()
		dt = tf - ti
		print(f"\nCompleted in {round(dt,5)} sec.")
		print(f"\n{self.n} number(s) have been filled in to the board.")
		print("After these methods, the board is:")
		self.ops.printboard()
		return self.board
