# welcome to my sudoku solver!!!

My script `SudokuSolver.py` is an object-oriented approach to solving sudoku puzzles. It includes methods of working through the sudoku logically as well as a brute force approach. 

Main command:
`python3 SudokuSolver.py` <br />
There are some optional arguments you can include:
* `-n` or `--nums`: follow this by a list of numbers separated by spaces corresponding to the rows of the sudoku. For example, to enter the board:<br />
  
         _ _ _ _ 
        |   |3 4| 
        |3 4|1 2| 
         _ _ _ _ 
        |  1|4  | 
        |  3|   |
         _ _ _ _ 
        

  run: `SudokuSolver.py -n 0 0 3 4 3 4 1 2 0 1 4 0 0 3 0 0 ` . 
  
  If you do not include this argument, there will be prompts to fill out the board later. 
  
  *`-v`: will print out more information about the steps taken while solving the sudoku. 
  
  *`-i`: Will show the board and solving visually in an pop out window using pygame. Numbers can be entered interactively while using this mode if you choose not to run with the `-n` command. 



## classes used

**BoardOperations**: General board operations. Anything that deals with adding, removing, or reading numbers from the board should be performed through this class. The board is represented as an NxN numpy array. Empty squares are represented as 0s. 

**BoardPossibilities**: given a board, creates a list of possibilities of numbers that are allowed in each square. This possibilities list is constructed such that `possibilities[row][col]` returns a list of numbers that can fit in `board[row][col]`. Any operation to add, remove, or read a number from the possibilities list should be done through this class. 
 
 **LogicMethods**: Uses the possibilities list to systematically fill in the board. The logic methods currently implemented are taken from this source: http://geometer.org/mathcircles/sudoku.pdf. In the future, I want to implement more methods described in the paper such as x-wing and swordfish. The sudoku can sometimes be solved only by using these methods, depending on the difficulty. 
  * naked_single: looks at the possibilities for each square. If there is only one possibilty, fill it in
  * hidden_single: looks at the list of possibilities for each row, column, and box, and check if a number only appears once. If so, fill it in 
  * poss_manip: looks at the possibilities for each row. col, and box. If there is a combination of two possibilities for squares in which the same two numbers are the only options, they are eliminated as possibilities from the other empty squares in the row/col box. The goal is to generalize this function to deal with 3 numbers over 3 different squares, 4 numbers over 4 different squares, etc. 
  * go: try all of the above methods until they no longer can make any changes to the board. Might not necessarily solve the sudoku, depending on the difficulty.

**BruteForce**: Systematically try filling in numbers until the solution is found. Starting from the top left of the board, it attempts to place numbers starting from 1 until one is found that meets sudoku rules. It will continue placing numbers until reaching a square in which no numbers fit. If this is the case, go back to the last square updated, increment it by 1, and try again. This is guaranteed to find a solution as long as the input is a valid sudoku. 

**Draw**: Interactive board implementation using pygame. All updates to the interactive board need to be done using this class. This class includes a unique way of inputting a board by entering the numbers interactively, as well as a way to specify the size of the board if that is not inputted. 


## some fun puzzles to try: 

"Hardest Sudoku": https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html. None of the logic-based methods are able to place any numbers, but it can be brute-forced:
`-n 8 0 0 0 0 0 0 0 0 0 0 3 6 0 0 0 0 0 0 7 0 0 9 0 2 0 0 0 5 0 0 0 7 0 0 0 0 0 0 0 4 5 7 0 0 0 0 0 1 0 0 0 3 0 0 0 1 0 0 0 0 6 8 0 0 8 5 0 0 0 1 0 0 9 0 0 0 0 4 0 0  `


Standard 9x9 sudoku that can be brute-forced very quickly:
`-n 0 1 0 0 0 9 7 0 3 0 8 0 0 6 0 0 0 0 6 0 0 0 0 0 0 0 9 0 0 9 0 7 0 0 3 0 0 6 0 0 9 0 2 0 0 3 0 1 0 0 5 0 7 0 0 0 8 0 0 3 0 0 7 0 0 0 0 0 0 3 0 0 0 3 0 0 5 0 4 0 8`

Standard 9x9 sudoku that can be solved with only the logic methods: 
`-n 5 3 0 0 7 0 0 0 0 6 0 0 1 9 5 0 0 0 0 9 8 0 0 0 0 6 0 8 0 0 0 6 0 0 0 3 4 0 0 8 0 3 0 0 1 7 0 0 0 2 0 0 0 6 0 6 0 0 0 0 2 8 0 0 0 0 4 1 9 0 0 5 0 0 0 0 8 0 0 7 9 `

Test puzzle that I used a lot: 
`-n 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 8 5 0 0 1 0 2 0 0 0 0 0 0 0 5 0 7 0 0 0 0 0 4 0 0 0 1 0 0 0 9 0 0 0 0 0 0 0 5 0 0 0 0 0 0 7 3 0 0 2 0 1 0 0 0 0 0 0 0 0 4 0 0 0 9`
