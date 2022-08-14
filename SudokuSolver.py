import numpy as np
import argparse

from BoardOperations import BoardOps
from BoardPossibilities import Possibilities
from LogicMethods import Methods
from BruteForce import Brute
from Interactive import Draw

def main():
	print("\n\n\nWelcome to my sudoku solver!!! :)")
	parser = argparse.ArgumentParser(description='Solve a sudoku! :D')
	parser.add_argument('-n', '--nums', type=int, nargs='+', help='Numbers of the sudoku from top-left to bottom-right. Empty spaces should be denoted as 0. If not inputted, you will fill it out manually in a second!')
	parser.add_argument('-v', '--verbose', action='store_true', help='Print out additional information about the solving methods.')
	parser.add_argument('-s', '--size', type=int, help='Size of the sudoku (must be a square number)')
	parser.add_argument('-i', '--interactive', action='store_true', help='Show the board in an interactive pop out window')
	args = parser.parse_args()
	if args.nums is not None:
		nums = np.array(args.nums)
		l = len(nums)
		if (int(np.sqrt(l)))**2 != l:
			print(f"Size must be a square. You inputted {l} numbers.")
			exit()
		size = int(np.sqrt(l))
		if nums.max()>size or nums.min()<0:
			print(f"All numbers must be within range of 0 - {size}!")
			exit()
		board = nums.reshape(size, size)
		#if args.interactive:
		#	D = Draw(size)
		#	D.FillFromBoard(board)
	else:
		if args.size is not None:
			size = args.size
			if ((int(np.sqrt(size)))**2 != size) or size == 0:
				size = 0
		else:
			size = 0
		###creating the board
		if args.interactive:
			print("Interactive board")
			D = Draw(size)
			board = D.FillFromScratch()
		else:
			if size == 0:
				while True:
					try:
						s = input("Enter the size of the board: ")
						size = int(s)
						if (int(np.sqrt(size)))**2 != size:
							print("The size must be a square.")
						elif s == 0:
							print("Board must be larger than 0.")
						else:
							break
					except ValueError:
						print("Your input should be a single number.")
			board = np.zeros((size, size), dtype=int)
			BO = BoardOps(board)
			BO.fill()

	BO = BoardOps(board, interactive=args.interactive)
	print("This is the board you have inputted:")
	BO.printboard()

	print("Performing a preliminary check...")
	sc = BO.sanitycheck()
	if sc == 0:
		print("There is an error with the numbers you inputted.")
		exit()
	print("All good!")

	print("\n\nStarting out by analyzing the possibilities list.")
	M = Methods(board, BO, verbose=args.verbose, interactive=args.interactive)
	board = M.go()
	BO.update(board)
	if not BO.isdone():
		print("\n\nNext up: Brute Forcing this board!")
		BF = Brute(board, BO, verbose=args.verbose, interactive=args.interactive)
		board = BF.go()
		BO.update(board)
		BO.isdone()



if __name__ == "__main__":
	main()
