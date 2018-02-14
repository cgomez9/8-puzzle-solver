import sys


class Puzzle:
    table = []
    blank_piece_position = {"row":0, "column":0}
    MAX_DIMENSION = 3
    SOLUTION_STATE = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    def fillFromString(self, initState):
        initStateIndex = 0
        new_column = []
        for row in range(0, self.MAX_DIMENSION):
            for column in range(0, self.MAX_DIMENSION):
                new_column.append(initState[initStateIndex])
                print(initState[initStateIndex])
                if initState[initStateIndex] == '0':
                    self.blank_piece_position["row"] = row
                    self.blank_piece_position["column"] = column
                initStateIndex += 1
            self.table.append(new_column)
            new_column = []

    def isSolved(self):
        self.table == self.SOLUTION_STATE

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
