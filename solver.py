import sys
import copy
import time
from setqueue import SetQueue
from puzzle import Puzzle
from stack import Stack

class Solver:
    def bfs(self, initialState):
        frontier = SetQueue()
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        initialPuzzle.setPuzzleId(1)
        frontier.put(initialPuzzle)
        explored = []
        while not frontier.empty():
            state = frontier.get()
            state.printTable()
            explored.append(state.table)
            if state.isSolved():
                return state
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                explored
            )
            for puzzle in movedPuzzles:
                puzzle.setPuzzleId(len(explored) + 1)
                frontier.put(puzzle)
            time.sleep(20)


    def dfs(self, initialState):
        frontier = Stack()
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.push(initialPuzzle)
        explored = []
        while not frontier.isEmpty():
            state = frontier.pop()
            state.printTable()
            explored.append(state.table)
            if state.isSolved():
                return state
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                state.getPossibleMovementsFromCurrentState(),
                explored
            )
            for puzzle in movedPuzzles:
                frontier.push(puzzle)

    def ucs(self,initialState):
        pass

    def createListOfMovedPuzzles(self, originalPuzzle, explored):
        movedPuzzles = []
        moves = originalPuzzle.getPossibleMovementsFromCurrentState()
        print(moves)
        if moves[0] == 1:
            movedUpPuzzle = copy.deepcopy(originalPuzzle)
            movedUpPuzzle.moveBlankUp()
            if self.puzzleIsNotRepeated(movedUpPuzzle, explored):
                movedUpPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedPuzzles.append(movedUpPuzzle)
        if moves[1] == 1:
            movedDownPuzzle = copy.deepcopy(originalPuzzle)
            movedDownPuzzle.moveBlankDown()
            if self.puzzleIsNotRepeated(movedDownPuzzle, explored):
                movedDownPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedPuzzles.append(movedDownPuzzle)
        if moves[2] == 1:
            movedLeftPuzzle = copy.deepcopy(originalPuzzle)
            movedLeftPuzzle.moveBlankLeft()
            if self.puzzleIsNotRepeated(movedLeftPuzzle, explored):
                movedLeftPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedPuzzles.append(movedLeftPuzzle)
        if moves[3] == 1:
            movedRightPuzzle = copy.deepcopy(originalPuzzle)
            movedRightPuzzle.moveBlankRight()
            if self.puzzleIsNotRepeated(movedRightPuzzle, explored):
                movedRightPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedPuzzles.append(movedRightPuzzle)

        return movedPuzzles

    @staticmethod
    def puzzleIsNotRepeated(puzzle, explored):
        return puzzle.table not in explored



method = sys.argv[1]
initialState = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solution = solver.bfs(initialState)
    print("")
    print("Padre: {}".format(solution.getParent()))
    print("ID: {}".format(solution.getPuzzleId()))
elif method == 'dfs':
    solution = solver.dfs(initialState)
