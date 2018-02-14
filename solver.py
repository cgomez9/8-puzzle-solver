import queue
import sys
from puzzle import Puzzle

class Solver:
    @staticmethod
    def bfs(initialState):
        frontier = queue.Queue()
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.put(initialPuzzle)
        explored = []
        while not frontier.empty():
            state = frontier.get()
            print(state.isSolved())
            explored.append(state)
            if state.isSolved():
                return state

    @staticmethod
    def dfs(self,initialState):
        pass

    @staticmethod
    def ucs(self,initialState):
        pass

method = sys.argv[1]
initialState = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solver.bfs(initialState)
