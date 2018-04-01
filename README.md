# 8-puzzle-solver

8-puzzle game solver made for the Artificial Intelligence Micromaster of Columbia. [More info](http://mypuzzle.org/sliding) about the game.

# Implementation

The puzzle can be solved using three methods: Breadth first search, Depth first search and A* with the manhattan distance heuristic.

# Usage

In order to see the algorithm in action, execute the following command on a terminal

```
python solver.py method initialPuzzleState
```
Where method can take the values: bfs, dfs and ast.

And initialPuzzleState is a secuence of comma separated numbers representing the initial positions of the pieces of the puzzle. The empty space is represented by a 0.

Example: 0,8,7,6,5,4,3,2,1

# Academic Honesty

If you are taking the Micromaster at Columbia, feel free to help you out with the code, but the idea is that you have to make the implementation by yourself.
Feel free to pull request improvements, because is not the optimal solution by far.
