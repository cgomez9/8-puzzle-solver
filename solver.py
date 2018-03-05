import sys
import copy
import time
import resource
import heapq
from setqueue import SetQueue
from setstack import SetStack
from puzzle import Puzzle
from solution import Solution

class Solver:
    def bfs(self, initialState):
        start = time.time()
        max_level = 0
        frontier = SetQueue()
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.put(initialPuzzle)
        explored = []
        forbidden = SetQueue()
        forbidden.put(initialPuzzle)
        while not frontier.empty():
            state = frontier.get()
            state.setPuzzleId(len(explored))
            explored.append(state)
            if state.isSolved():
                solution = self.getSolution(state,explored,start,max_level)
                self.writeSolutionToFile(solution)
                break
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                forbidden
            )
            if movedPuzzles and movedPuzzles[0].getLevel() > max_level:
                max_level = movedPuzzles[0].getLevel()
            for puzzle in movedPuzzles:
                frontier.put(puzzle)
                forbidden.put(puzzle)

    def dfs(self, initialState):
        start = time.time()
        max_level = 0
        frontier = SetStack()
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        frontier.put(initialPuzzle)
        explored = []
        forbidden = SetQueue()
        forbidden.put(initialPuzzle)
        while not frontier.empty():
            state = frontier.get()
            state.setPuzzleId(len(explored))
            explored.append(state)
            if state.isSolved():
                solution = self.getSolution(state,explored,start,max_level)
                self.writeSolutionToFile(solution)
                break
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                forbidden
            )
            if movedPuzzles and movedPuzzles[0].getLevel() > max_level:
                max_level = movedPuzzles[0].getLevel()
            for puzzle in reversed(movedPuzzles):
                frontier.put(puzzle)
                forbidden.put(puzzle)

    def ast(self,initialState):
        start = time.time()
        max_level = 0
        frontier = []
        heapq.heapify(frontier)
        initialPuzzle = Puzzle()
        initialPuzzle.fillFromString(initialState.split(','))
        heapq.heappush(frontier,initialPuzzle)
        explored = []
        forbidden = SetQueue()
        forbidden.put(initialPuzzle)
        while heapq.nlargest(1, frontier):
            state = heapq.heappop(frontier)
            state.setPuzzleId(len(explored))
            explored.append(state)
            if state.isSolved():
                solution = self.getSolution(state,explored,start,max_level)
                self.writeSolutionToFile(solution)
                break
            movedPuzzles = self.createListOfMovedPuzzles(
                state,
                forbidden
            )
            if movedPuzzles and movedPuzzles[0].getLevel() > max_level:
                max_level = movedPuzzles[0].getLevel()
            for puzzle in movedPuzzles:
                heapq.heappush(frontier,puzzle)
                forbidden.put(puzzle)

    def createListOfMovedPuzzles(self, originalPuzzle, forbidden):
        movedPuzzles = []
        moves = originalPuzzle.getPossibleMovementsFromCurrentState()
        if moves[0] == 1:
            movedUpPuzzle = Puzzle()
            movedUpPuzzle.fillFromPuzzle(originalPuzzle)
            movedUpPuzzle.moveBlankUp()
            if not self.puzzleIsRepeated(movedUpPuzzle, forbidden):
                movedUpPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedUpPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedUpPuzzle.setMovement('Up')
                movedPuzzles.append(movedUpPuzzle)
        if moves[1] == 1:
            movedDownPuzzle = Puzzle()
            movedDownPuzzle.fillFromPuzzle(originalPuzzle)
            movedDownPuzzle.moveBlankDown()
            if not self.puzzleIsRepeated(movedDownPuzzle, forbidden):
                movedDownPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedDownPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedDownPuzzle.setMovement('Down')
                movedPuzzles.append(movedDownPuzzle)
        if moves[2] == 1:
            movedLeftPuzzle = Puzzle()
            movedLeftPuzzle.fillFromPuzzle(originalPuzzle)
            movedLeftPuzzle.moveBlankLeft()
            if not self.puzzleIsRepeated(movedLeftPuzzle, forbidden):
                movedLeftPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedLeftPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedLeftPuzzle.setMovement('Left')
                movedPuzzles.append(movedLeftPuzzle)
        if moves[3] == 1:
            movedRightPuzzle = Puzzle()
            movedRightPuzzle.fillFromPuzzle(originalPuzzle)
            movedRightPuzzle.moveBlankRight()
            if not self.puzzleIsRepeated(movedRightPuzzle, forbidden):
                movedRightPuzzle.setParent(originalPuzzle.getPuzzleId())
                movedRightPuzzle.setLevel(originalPuzzle.getLevel() + 1)
                movedRightPuzzle.setMovement('Right')
                movedPuzzles.append(movedRightPuzzle)
        return movedPuzzles

    @staticmethod
    def puzzleIsRepeated(puzzle, forbidden):
        return forbidden.hasElement(puzzle)

    def getSolution(self, state, explored, start, max_level):
        solution = Solution()
        solution.path_to_goal = self.findPathForSolution(state,explored)
        solution.nodes_expanded = len(explored) - 1
        solution.search_depth = state.getLevel()
        solution.max_search_depth = max_level
        mem_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        solution.max_ram_usage = mem_use / float(1024)
        solution.running_time = time.time()-start;
        return solution

    def writeSolutionToFile(self, solution):
        file = open("output.txt","w")
        file.write("path_to_goal: {}\n".format(solution.path_to_goal))
        file.write("cost_of_path: {}\n".format(len(solution.path_to_goal)))
        file.write("nodes_expanded: {}\n".format(solution.nodes_expanded))
        file.write("search_depth: {}\n".format(solution.search_depth))
        file.write("max_search_depth: {}\n".format(solution.max_search_depth))
        file.write("running_time: {}\n".format(solution.running_time))
        file.write("max_ram_usage: {}\n".format(solution.max_ram_usage))
        file.close()

    @staticmethod
    def findPathForSolution(state, explored):
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


method = sys.argv[1]
initialState = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solver.bfs(initialState)
elif method == 'dfs':
    solver.dfs(initialState)
elif method == 'ast':
    solver.ast(initialState)
