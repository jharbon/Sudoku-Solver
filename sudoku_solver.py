# -*- coding: utf-8 -*-

import sys

import numpy as np

from timeit import default_timer

class SudokuSolver():
    
    def __init__(self):
        # Create attribute for storing grid information after user input
        self.grid = []
        
        # Solution for grid and time taken to solve can be stored in two attributes
        self.solved_grid = None
        self.solve_time = None
        
    # Create function which asks user to input puzzle and then appends the rows to self.grid    
    def ask_for_puzzle(self):
        print("Enter your puzzle one row at a time. For example, to enter the row [1, 3, 4, 5, 7, 8, 9, 1, 2] " +
              "type in 1 3 4 5 7 8 9 1 2 and then hit enter. Enter 0 for where there is no number in the puzzle. " +
              "Repeat this until you have entered all rows of your puzzle.")
        for i in range(9):
            row_input = input("Row: ")
            row_list = row_input.split()
            row_list = [int(i) for i in row_list]
            self.grid.append(row_list)

        # Check if user has inputted correct number of elements for columns
        # If not, reset self.grid and recursively call this method
        if np.array(self.grid).shape != (9, 9):
            print("You must input a puzzle with 9 rows and 9 columns!")
            self.grid = []
            self.ask_for_puzzle()
            return
        
        # Check that user has entered numbers in the valid range
        for x in range(9):
            for y in range(9):
                if self.grid[y][x] not in range(0, 10):
                    print("You must enter numbers in the range 0-9!")
                    self.grid = []
                    self.ask_for_puzzle()
                    return
        
        # Check that user has inputted the correct puzzle
        print("\nYou have inputted the following puzzle:\n")
        print(np.matrix(self.grid))
        print("\n Is this correct? Type y or n.")
        decision_input = input()
        while decision_input not in ["y", "n"]:
            print("You need to enter y or n.")
            decision_input = input()
        
        # If user has entered incorrect puzzle, reset self.grid and recursively call this method
        if decision_input == "y":
            return
        elif decision_input == "n":
            self.grid = []
            self.ask_for_puzzle()
            return
            
    
    # Create function which checks if it is possible to place a given number in a given grid position
    # x defines horizontal axis and hence column index
    # y defines vertical axis and hence row index    
    def check_possibility(self, x, y, num):
        # Check the box
        for i in range((x // 3) * 3, (x // 3) * 3 + 3):
            for j in range((y // 3) * 3, (y // 3) * 3 + 3):
                if self.grid[j][i] == num and (j, i) != (y, x):
                    return False
        
        # Check the row
        for i in range(9):
            if self.grid[y][i] == num and (y, i) != (y, x):
                return False
        
        # Check the column
        for i in range(9):
            if self.grid[i][x] == num and (i, x) != (y, x):
                return False
            
        return True 
    
    # Create function which implements the backtracking recursion algorithm
    def backtrack_alg(self, init_solve_grid = True):
        # First set solved_grid = grid and adjust solved_grid as we progress
        # Only make this change for the first call of this method
        if init_solve_grid:
            self.solved_grid = self.grid
        
        # Loop through every position in puzzle
        for x in range(9):
            for y in range(9):
                # When an empty position (0) is found, try different possible numbers
                # Try to recursively solve by calling backtrack_solve for a possible number
                # If puzzle cannot be solved after choosing that specific number, return False
                # Set value back to 0 (backtrack) and then try a different possible number
                if self.solved_grid[y][x] == 0:
                    for num in range(1, 10):
                        if self.check_possibility(x, y, num):
                            self.solved_grid[y][x] = num
                            if self.backtrack_alg(init_solve_grid = False):
                                return True
                            else:
                                self.solved_grid[y][x] = 0
                            
                    return False     
                
        return True        
        
    def solve(self):
        # Set timer to start measuring time taken to solve
        start = default_timer()
        
        self.backtrack_alg()
        
        # Check again if there are any empty spaces to check if the puzzle has been solved  
        # Exit program if there is no solution
        for x in range(9):
            for y in range(9):
                if self.solved_grid[y][x] == 0:
                    print("There is no solution for this puzzle!")
                    sys.exit()
                
        # If no empty positions can be found, then we have solved the puzzle
        stop = default_timer()
        self.solve_time = stop - start
        
        # Show the solution and time taken to solve
        print("\nSolution:\n")
        print(np.matrix(self.solved_grid))
        print("\nTime taken to solve: {:.2f} seconds".format(self.solve_time))
        return

if __name__ == "__main__":
    solver = SudokuSolver()
    solver.ask_for_puzzle()
    solver.solve()


         
            

