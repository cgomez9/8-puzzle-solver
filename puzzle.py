import sys


class Puzzle:
    def __init__(self):
        self.parent = 0
        self.puzzle_id = 0
        self.table = []
        self.blank_piece_position = {"row":0, "column":0}
        self.MAX_DIMENSION = 3
        self.SOLUTION_STATE = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

    def fillFromString(self, initState):
        initStateIndex = 0
        new_column = []
        for row in range(0, self.MAX_DIMENSION):
            for column in range(0, self.MAX_DIMENSION):
                new_column.append(int(initState[initStateIndex]))
                if initState[initStateIndex] == '0':
                    self.blank_piece_position["row"] = row
                    self.blank_piece_position["column"] = column
                initStateIndex += 1
            self.table.append(new_column)
            new_column = []

    def fillFromPuzzle(self, puzzle):
        self.table = puzzle.table
        self.blank_piece_position = puzzle.blank_piece_position

    def isSolved(self):
        return self.table == self.SOLUTION_STATE

    def getPossibleMovementsFromCurrentState(self):
        possible_movements = []
        # Blank space can move up
        up = 1 if self.blank_piece_position["row"] - 1 >= 0 else 0
        possible_movements.append(up)
        # Blank space can move down
        down = 1 if self.blank_piece_position["row"] + 1 <= self.MAX_DIMENSION - 1 else 0
        possible_movements.append(down)
        # Blank space can move left
        left = 1 if self.blank_piece_position["column"] - 1 >= 0 else 0
        possible_movements.append(left)
        # Blank space can move right
        right = 1 if self.blank_piece_position["column"] + 1 <= self.MAX_DIMENSION - 1 else 0
        possible_movements.append(right)
        return possible_movements

    def moveBlankUp(self):
        if self.blank_piece_position["row"] - 1 >= 0:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row - 1][blank_column]
            self.table[blank_row - 1][blank_column] = 0
            self.blank_piece_position["row"] -= 1

    def moveBlankDown(self):
        if self.blank_piece_position["row"] + 1 <= self.MAX_DIMENSION - 1:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row + 1][blank_column]
            self.table[blank_row + 1][blank_column] = 0
            self.blank_piece_position["row"] += 1

    def moveBlankLeft(self):
        if self.blank_piece_position["column"] - 1 >= 0:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row][blank_column - 1]
            self.table[blank_row][blank_column - 1] = 0
            self.blank_piece_position["column"] -= 1

    def moveBlankRight(self):
        if self.blank_piece_position["column"] + 1 <= self.MAX_DIMENSION - 1:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row][blank_column + 1]
            self.table[blank_row][blank_column + 1] = 0
            self.blank_piece_position["column"] += 1

    def printTable(self):
        print("\033[H\033[J")
        for row in self.table:
            print(row)
        print("")

    def setPuzzleId(self, puzzle_id):
        self.puzzle_id = puzzle_id

    def getPuzzleId(self):
        return self.puzzle_id

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
