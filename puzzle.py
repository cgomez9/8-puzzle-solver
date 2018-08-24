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
        self.manhattan_distance = 0
        self.creation_date = datetime.now()
        self.importance = 0

    def fill_from_string(self, init_state):
        init_state_index = 0
        new_column = []
        for row in range(0, self.MAX_DIMENSION):
            for column in range(0, self.MAX_DIMENSION):
                new_column.append(int(init_state[init_state_index]))
                if init_state[init_state_index] == '0':
                    self.blank_piece_position["row"] = row
                    self.blank_piece_position["column"] = column
                init_state_index += 1
            self.table.append(new_column)
            new_column = []
        self.calculate_table_signature()
        self.calculate_manhattan_distance()

    def fill_from_puzzle(self, puzzle):
        for row in puzzle.table:
            self.table.append(list(row))
        self.blank_piece_position = dict(puzzle.blank_piece_position)
        self.calculate_table_signature()
        self.calculate_manhattan_distance()

    def is_solved(self):
        return self.table == self.SOLUTION_STATE

    def get_possible_movements_from_current_state(self):
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

    def calculate_manhattan_distance(self):
        manhattan_distance = 0
        for index_row,row in enumerate(self.table):
            for index_column,element in enumerate(row):
                if element != 0:
                    row_distance = abs(index_row - self.SOLUTION_STATE_INDEX[element]["row"])
                    column_distance = abs(index_column - self.SOLUTION_STATE_INDEX[element]["column"])
                    manhattan_distance += row_distance + column_distance
        self.manhattan_distance = manhattan_distance


    def moveBlankUp(self):
        if self.blank_piece_position["row"] - 1 >= 0:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row - 1][blank_column]
            self.table[blank_row - 1][blank_column] = 0
            self.blank_piece_position["row"] -= 1
            self.calculate_table_signature()
            self.calculate_manhattan_distance()
            self.importance = 4

    def moveBlankDown(self):
        if self.blank_piece_position["row"] + 1 <= self.MAX_DIMENSION - 1:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row + 1][blank_column]
            self.table[blank_row + 1][blank_column] = 0
            self.blank_piece_position["row"] += 1
            self.calculate_table_signature()
            self.calculate_manhattan_distance()
            self.importance = 3

    def moveBlankLeft(self):
        if self.blank_piece_position["column"] - 1 >= 0:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row][blank_column - 1]
            self.table[blank_row][blank_column - 1] = 0
            self.blank_piece_position["column"] -= 1
            self.calculate_table_signature()
            self.calculate_manhattan_distance()
            self.importance = 2

    def moveBlankRight(self):
        if self.blank_piece_position["column"] + 1 <= self.MAX_DIMENSION - 1:
            blank_row = self.blank_piece_position["row"]
            blank_column = self.blank_piece_position["column"]
            self.table[blank_row][blank_column] = self.table[blank_row][blank_column + 1]
            self.table[blank_row][blank_column + 1] = 0
            self.blank_piece_position["column"] += 1
            self.calculate_table_signature()
            self.calculate_manhattan_distance()
            self.importance = 1

    def print_table(self):
        #print("\033[H\033[J")
        for row in self.table:
            print(row)
        print("")

    def set_puzzle_id(self, puzzle_id):
        self.puzzle_id = puzzle_id

    def get_puzzle_id(self):
        return self.puzzle_id

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_movement(self, movement):
        self.movement = movement

    def get_movement(self):
        return self.movement

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    def calculate_table_signature(self):
        self.table_signature = self.get_table_signature()

    def get_table_signature(self):
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
        self_heuristic = self.manhattan_distance + self.level
        other_heuristic = other.manhattan_distance + other.level
        if self_heuristic == other_heuristic:
            if self.importance == other.importance:
                return self.creation_date < other.creation_date
            else:
                return self.importance < other.importance
        else:
            return self_heuristic < other_heuristic
