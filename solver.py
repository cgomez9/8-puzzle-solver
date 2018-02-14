import queue
import sys
from puzzle import Puzzle

class Solver:
    def bfs(initialState, goalState):
        frontier = queue.Queue()
        frontier.put(initialState)
        explored = []
        while not frontier.empty():
            state = frontier.get()
            explored.append(state)
            if state == goalState:
                return state

    def dfs(initialState, goalTest):
        pass

    def ucs(initialState, goalTest):
        pass

method = sys.argv[1]
initialState = sys.argv[2]

print(method)
print(initialState)

puzzle = Puzzle()
puzzle.fillFromString(initialState.split(','))
print(puzzle.table)
print(puzzle.blank_piece_position)
print(puzzle.getPossibleMovementsFromCurrentState())
