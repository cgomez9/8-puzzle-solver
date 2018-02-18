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
        frontier.put(initialPuzzle)
        explored = []
        while not frontier.empty():
            state = frontier.get()
            state.printTable()
            state.setPuzzleId(len(explored))
            explored.append(state)
            if state.isSolved():
                temp_solution_path = []
                temp_solution_path.append(state.getMovement())
                current_parent_id = state.getParent()
                while current_parent_id > 0:
                    parent_state = explored[current_parent_id]
                    temp_solution_path.append(parent_state.getMovement())
                    current_parent_id = parent_state.getParent()
                real_solution_path = []
                for element in reversed(temp_solution_path):
                    real_solution_path.append(element)
                return real_solution_path
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                explored
            )
            for puzzle in movedPuzzles:
                frontier.put(puzzle)
            time.sleep(0.1)


    def dfs(self, initialState):
        frontier = Stack()
        frontier.push(initialPuzzle)
        while not frontier.isEmpty():
            state = frontier.pop()
            frontier.push(puzzle)

    def a_star(self,initialState):
        pass

    def createListOfMovedPuzzles(self, originalPuzzle, explored):
        movedPuzzles = []
        moves = originalPuzzle.getPossibleMovementsFromCurrentState()
        if moves[0] == 1:
            movedUpPuzzle = copy.deepcopy(originalPuzzle)
            movedUpPuzzle.moveBlankUp()
            if self.puzzleIsNotRepeated(movedUpPuzzle, explored):
                movedUpPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedUpPuzzle.setMovement('Up')
                movedPuzzles.append(movedUpPuzzle)
        if moves[1] == 1:
            movedDownPuzzle = copy.deepcopy(originalPuzzle)
            movedDownPuzzle.moveBlankDown()
            if self.puzzleIsNotRepeated(movedDownPuzzle, explored):
                movedDownPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedDownPuzzle.setMovement('Down')
                movedPuzzles.append(movedDownPuzzle)
        if moves[2] == 1:
            movedLeftPuzzle = copy.deepcopy(originalPuzzle)
            movedLeftPuzzle.moveBlankLeft()
            if self.puzzleIsNotRepeated(movedLeftPuzzle, explored):
                movedLeftPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedLeftPuzzle.setMovement('Left')
                movedPuzzles.append(movedLeftPuzzle)
        if moves[3] == 1:
            movedRightPuzzle = copy.deepcopy(originalPuzzle)
            movedRightPuzzle.moveBlankRight()
            if self.puzzleIsNotRepeated(movedRightPuzzle, explored):
                movedRightPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedRightPuzzle.setMovement('Right')
                movedPuzzles.append(movedRightPuzzle)

        return movedPuzzles

    @staticmethod
    def puzzleIsNotRepeated(puzzle, explored):
        for state in explored:
            if puzzle.table == state.table:
                return False
        return True


method = sys.argv[1]
initialState = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solution = solver.bfs(initialState)
    print("")
    print(solution)
elif method == 'dfs':
    solution = solver.dfs(initialState)
