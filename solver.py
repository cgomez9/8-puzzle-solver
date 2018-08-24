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
    def bfs(self, initial_state):
        start = time.time()
        max_level = 0
        frontier = SetQueue()
        initial_puzzle = Puzzle()
        initial_puzzle.fill_from_string(initial_state.split(','))
        frontier.put(initial_puzzle)
        explored = []
        forbidden = SetQueue()
        forbidden.put(initial_puzzle)
        while not frontier.empty():
            state = frontier.get()
            state.set_puzzle_id(len(explored))
            explored.append(state)
            if state.is_solved():
                solution = self.get_solution(state,explored,start,max_level)
                self.write_solution_to_file(solution)
                break
            moved_puzzles = self.create_list_of_moved_puzzles(
                state,
                forbidden
            )
            if moved_puzzles and moved_puzzles[0].get_level() > max_level:
                max_level = moved_puzzles[0].get_level()
            for puzzle in moved_puzzles:
                frontier.put(puzzle)
                forbidden.put(puzzle)

    def dfs(self, initial_state):
        start = time.time()
        max_level = 0
        frontier = SetStack()
        initial_puzzle = Puzzle()
        initial_puzzle.fill_from_string(initial_state.split(','))
        frontier.put(initial_puzzle)
        explored = []
        forbidden = SetQueue()
        forbidden.put(initial_puzzle)
        while not frontier.empty():
            state = frontier.get()
            state.set_puzzle_id(len(explored))
            explored.append(state)
            if state.is_solved():
                solution = self.get_solution(state,explored,start,max_level)
                self.write_solution_to_file(solution)
                break
            moved_puzzles = self.create_list_of_moved_puzzles(
                state,
                forbidden
            )
            if moved_puzzles and moved_puzzles[0].get_level() > max_level:
                max_level = moved_puzzles[0].get_level()
            for puzzle in reversed(moved_puzzles):
                frontier.put(puzzle)
                forbidden.put(puzzle)

    def ast(self,initial_state):
        start = time.time()
        max_level = 0
        frontier = []
        heapq.heapify(frontier)
        initial_puzzle = Puzzle()
        initial_puzzle.fill_from_string(initial_state.split(','))
        heapq.heappush(frontier,initial_puzzle)
        explored = []
        forbidden = SetQueue()
        while heapq.nlargest(1, frontier):
            state = heapq.heappop(frontier)
            state.set_puzzle_id(len(explored))
            explored.append(state)
            if state.is_solved():
                solution = self.get_solution(state,explored,start,max_level)
                self.write_solution_to_file(solution)
                break
            moved_puzzles = self.create_list_of_moved_puzzles(
                state,
                forbidden
            )
            if moved_puzzles and moved_puzzles[0].get_level() > max_level:
                max_level = moved_puzzles[0].get_level()
            for puzzle in moved_puzzles:
                heapq.heappush(frontier,puzzle)
                forbidden.put(puzzle)

    def create_list_of_moved_puzzles(self, original_puzzle, forbidden):
        moved_puzzles = []
        moves = original_puzzle.get_possible_movements_from_current_state()
        if moves[0] == 1:
            movedUpPuzzle = Puzzle()
            movedUpPuzzle.fill_from_puzzle(original_puzzle)
            movedUpPuzzle.moveBlankUp()
            if not self.puzzle_is_repeated(movedUpPuzzle, forbidden):
                movedUpPuzzle.set_parent(original_puzzle.get_puzzle_id())
                movedUpPuzzle.set_level(original_puzzle.get_level() + 1)
                movedUpPuzzle.set_movement('Up')
                moved_puzzles.append(movedUpPuzzle)
        if moves[1] == 1:
            moved_down_puzzle = Puzzle()
            moved_down_puzzle.fill_from_puzzle(original_puzzle)
            moved_down_puzzle.moveBlankDown()
            if not self.puzzle_is_repeated(moved_down_puzzle, forbidden):
                moved_down_puzzle.set_parent(original_puzzle.get_puzzle_id())
                moved_down_puzzle.set_level(original_puzzle.get_level() + 1)
                moved_down_puzzle.set_movement('Down')
                moved_puzzles.append(moved_down_puzzle)
        if moves[2] == 1:
            moved_left_puzzle = Puzzle()
            moved_left_puzzle.fill_from_puzzle(original_puzzle)
            moved_left_puzzle.moveBlankLeft()
            if not self.puzzle_is_repeated(moved_left_puzzle, forbidden):
                moved_left_puzzle.set_parent(original_puzzle.get_puzzle_id())
                moved_left_puzzle.set_level(original_puzzle.get_level() + 1)
                moved_left_puzzle.set_movement('Left')
                moved_puzzles.append(moved_left_puzzle)
        if moves[3] == 1:
            moved_right_puzzle = Puzzle()
            moved_right_puzzle.fill_from_puzzle(original_puzzle)
            moved_right_puzzle.moveBlankRight()
            if not self.puzzle_is_repeated(moved_right_puzzle, forbidden):
                moved_right_puzzle.set_parent(original_puzzle.get_puzzle_id())
                moved_right_puzzle.set_level(original_puzzle.get_level() + 1)
                moved_right_puzzle.set_movement('Right')
                moved_puzzles.append(moved_right_puzzle)
        return moved_puzzles

    @staticmethod
    def puzzle_is_repeated(puzzle, forbidden):
        return forbidden.hasElement(puzzle)

    @staticmethod
    def puzzleIsInFrontier(puzzle, frontier):
        return forbidden.hasElement(puzzle)

    def get_solution(self, state, explored, start, max_level):
        solution = Solution()
        solution.path_to_goal = self.find_path_for_solution(state,explored)
        solution.nodes_expanded = len(explored) - 1
        solution.search_depth = state.get_level()
        solution.max_search_depth = max_level
        mem_use = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        solution.max_ram_usage = mem_use / float(1024)
        solution.running_time = time.time()-start;
        return solution

    def write_solution_to_file(self, solution):
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
    def find_path_for_solution(state, explored):
        temp_solution_path = []
        temp_solution_path.append(state.get_movement())
        current_parent_id = state.get_parent()
        while current_parent_id > 0:
            parent_state = explored[current_parent_id]
            temp_solution_path.append(parent_state.get_movement())
            current_parent_id = parent_state.get_parent()
        real_solution_path = []
        for element in reversed(temp_solution_path):
            real_solution_path.append(element)
        return real_solution_path


method = sys.argv[1]
initial_state = sys.argv[2]

solver = Solver()
if method == 'bfs':
    solver.bfs(initial_state)
elif method == 'dfs':
    solver.dfs(initial_state)
elif method == 'ast':
    solver.ast(initial_state)
