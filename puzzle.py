import sys
import re
from datetime import datetime


class Puzzle:
    def __init__(self):
        self.parent = -1
        self.puzzle_id = -1
        self.table_signature = ()
        self.level = 0
        self.movement = ''
        self.table = []
        self.blank_piece_position = {"row":0, "column":0}
        self.MAX_DIMENSION = 3
        self.SOLUTION_STATE = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]
        self.SOLUTION_STATE_INDEX = [
            {"row":0, "column":0},
            {"row":0, "column":1},
            {"row":0, "column":2},
            {"row":1, "column":0},
            {"row":1, "column":1},
            {"row":1, "column":2},
            {"row":2, "column":0},
            {"row":2, "column":1},
            {"row":2, "column":2}
        ]
        self.manhattanDistance = 0
        self.creation_date = datetime.now()

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
        self.calculateTableSignature()
        self.importance = 1

    def fillFromPuzzle(self, puzzle):
        for row in puzzle.table:
            self.table.append(list(row))
        self.blank_piece_position = dict(puzzle.blank_piece_position)
        self.calculateTableSignature()

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

    def calculateManhattanDistance(self):
        manhattanDistance = 0
        for indexRow,row in enumerate(self.table):
            for indexColumn,element in enumerate(row):
                if element != 0:
                    rowDistance = abs(indexRow - self.SOLUTION_STATE_INDEX[element]["row"])
                    columnDistance = abs(indexColumn - self.SOLUTION_STATE_INDEX[element]["column"])
                    manhattanDistance += rowDistance + columnDistance
        return manhattanDistance


    def moveBlankUp(self):
        if self.blank_piece_position["row"] - 1 >= 0:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row - 1][blank_column]
            self.table[blank_row - 1][blank_column] = 0
            self.blank_piece_position["row"] -= 1
            self.calculateTableSignature()

    def moveBlankDown(self):
        if self.blank_piece_position["row"] + 1 <= self.MAX_DIMENSION - 1:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row + 1][blank_column]
            self.table[blank_row + 1][blank_column] = 0
            self.blank_piece_position["row"] += 1
            self.calculateTableSignature()

    def moveBlankLeft(self):
        if self.blank_piece_position["column"] - 1 >= 0:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row][blank_column - 1]
            self.table[blank_row][blank_column - 1] = 0
            self.blank_piece_position["column"] -= 1
            self.calculateTableSignature()

    def moveBlankRight(self):
        if self.blank_piece_position["column"] + 1 <= self.MAX_DIMENSION - 1:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row][blank_column + 1]
            self.table[blank_row][blank_column + 1] = 0
            self.blank_piece_position["column"] += 1
            self.calculateTableSignature()

    def printTable(self):
        #print("\033[H\033[J")
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

    def setMovement(self, movement):
        self.movement = movement

    def getMovement(self):
        return self.movement

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def calculateTableSignature(self):
        self.table_signature = self.getTableSignature()

    def getTableSignature(self):
        return (
            self.table[0][0],
            self.table[0][1],
            self.table[0][2],
            self.table[1][0],
            self.table[1][1],
            self.table[1][2],
            self.table[2][0],
            self.table[2][1],
            self.table[2][2]
        )

    def __hash__(self):
        return hash(self.table_signature)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.table_signature == other.table_signature
        )

    def __lt__(self, other):
        selfHeuristic = self.calculateManhattanDistance() + self.level
        otherHeuristic = other.calculateManhattanDistance() + other.level
        if selfHeuristic == otherHeuristic:
            return self.creation_date < other.creation_date
        else: 
            return selfHeuristic < otherHeuristic
