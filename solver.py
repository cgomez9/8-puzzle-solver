import sys
import copy
import time
import resource
from setqueue import SetQueue
from setstack import SetStack
from puzzle import Puzzle
from solution import Solution

class Solver:
    def bfs(self, initialState):
        start = time.time()
        frontier = SetQueue()
        forbidden = []
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.put(initialPuzzle)
        forbidden.append(initialPuzzle.table)
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
                solution = Solution()
                solution.path_to_goal = real_solution_path
                solution.nodes_expanded = len(explored) - 1
                solution.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024)
                solution.running_time = time.time()-start;
                self.writeSolutionToFile(solution)
                break
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                forbidden
            )
            for puzzle in movedPuzzles:
                frontier.put(puzzle)
                forbidden.append(puzzle.table)

    def dfs(self, initialState):
        start = time.time()
        frontier = SetStack()
        forbidden = []
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.put(initialPuzzle)
        forbidden.append(initialPuzzle.table)
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
                solution = Solution()
                solution.path_to_goal = real_solution_path
                solution.nodes_expanded = len(explored)-1
                solution.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / float(1024)
                solution.running_time = time.time()-start;
                self.writeSolutionToFile(solution)
                break
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                forbidden
            )
            for puzzle in reversed(movedPuzzles):
                frontier.put(puzzle)
                forbidden.append(puzzle.table)


    def a_star(self,initialState):
        pass

    def createListOfMovedPuzzles(self, originalPuzzle, forbidden):
        movedPuzzles = []
        moves = originalPuzzle.getPossibleMovementsFromCurrentState()
        if moves[0] == 1:
            movedUpPuzzle = copy.deepcopy(originalPuzzle)
            movedUpPuzzle.moveBlankUp()
            if not self.puzzleIsRepeated(movedUpPuzzle, forbidden):
                movedUpPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedUpPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedUpPuzzle.setMovement('Up')
                movedPuzzles.append(movedUpPuzzle)
        if moves[1] == 1:
            movedDownPuzzle = copy.deepcopy(originalPuzzle)
            movedDownPuzzle.moveBlankDown()
            if not self.puzzleIsRepeated(movedDownPuzzle, forbidden):
                movedDownPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedDownPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedDownPuzzle.setMovement('Down')
                movedPuzzles.append(movedDownPuzzle)
        if moves[2] == 1:
            movedLeftPuzzle = copy.deepcopy(originalPuzzle)
            movedLeftPuzzle.moveBlankLeft()
            if not self.puzzleIsRepeated(movedLeftPuzzle, forbidden):
                movedLeftPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedLeftPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedLeftPuzzle.setMovement('Left')
                movedPuzzles.append(movedLeftPuzzle)
        if moves[3] == 1:
            movedRightPuzzle = copy.deepcopy(originalPuzzle)
            movedRightPuzzle.moveBlankRight()
            if not self.puzzleIsRepeated(movedRightPuzzle, forbidden):
                movedRightPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedRightPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedRightPuzzle.setMovement('Right')
                movedPuzzles.append(movedRightPuzzle)

        return movedPuzzles

    @staticmethod
    def puzzleIsRepeated(puzzle, forbidden):
        return puzzle.table in forbidden

    def writeSolutionToFile(self, solution):
        file = open("output.txt","w")
        file.write("path_to_goal: {}\n".format(solution.path_to_goal))
        file.write("cost_of_path: {}\n".format(len(solution.path_to_goal)))
        file.write("nodes_expanded: {}\n".format(solution.nodes_expanded))
        file.write("max_search_depth\n")
        file.write("running_time: {}\n".format(solution.running_time))
        file.write("max_ram_usage: {}\n".format(solution.max_ram_usage))
        file.close()


method = sys.argv[1]
initialState = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solver.bfs(initialState)
elif method == 'dfs':
    solver.dfs(initialState)
