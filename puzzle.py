import sys


class Puzzle:
    table = []
    PUZZLE_DIMENSION = 3
    SOLUTION_STATE = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    def __init__(self, initState):
        initStateIndex = 0
        for row in range(0, self.PUZZLE_DIMENSION):
            for column in range(0, self.PUZZLE_DIMENSION):
                self.table[row][column] = initState[initStateIndex]
                initStateIndex += 1

    def isSolved(self,currentState):
        self.table == self.SOLUTION_STATE

            
