import queue
import sys
import copy
import time
from puzzle import Puzzle

class Solver:
    def bfs(self, initialState):
        frontier = queue.Queue()
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.put(initialPuzzle)
        explored = []
        while not frontier.empty():
            state = frontier.get()
            state.printTable()
            explored.append(state)
            if state.isSolved():
                return state
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                state.getPossibleMovementsFromCurrentState()
            )
            for puzzle in movedPuzzles:
                if puzzle not in explored:
                    frontier.put(puzzle)

            time.sleep(2)


    @staticmethod
    def dfs(self,initialState):
        pass

    @staticmethod
    def ucs(self,initialState):
        pass

    @staticmethod
    def createListOfMovedPuzzles(originalPuzzle, moves):
        movedPuzzles = []
        if moves[0] == 1:
            movedUpPuzzle = copy.deepcopy(originalPuzzle)
            movedUpPuzzle.moveBlankUp()
            movedPuzzles.append(movedUpPuzzle)
        if moves[1] == 1:
            movedDownPuzzle = copy.deepcopy(originalPuzzle)
            movedDownPuzzle.moveBlankDown()
            movedPuzzles.append(movedDownPuzzle)
        if moves[2] == 1:
            movedLeftPuzzle = copy.deepcopy(originalPuzzle)
            movedLeftPuzzle.moveBlankLeft()
            movedPuzzles.append(movedLeftPuzzle)
        if moves[3] == 1:
            movedRightPuzzle = copy.deepcopy(originalPuzzle)
            movedRightPuzzle.moveBlankRight()
            movedPuzzles.append(movedRightPuzzle)

        return movedPuzzles



method = sys.argv[1]
initialState = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solution = solver.bfs(initialState)
    print(solution.table)
