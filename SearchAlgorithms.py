import queue
import sys

class SearchAlgorithms:
    def bfs(initialState, goalState):
        frontier = queue.Queue()
        frontier.put(initialState)
        explored = []
        while !frontier.empty():
            state = frontier.get()
            explored.append(state)
            if state === goalState:
                return state

    def dfs(initialState, goalTest):
        pass
    def ucs(initialState, goalTest):
        pass
