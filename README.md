# 🧩 Maze Generation in Python

This python script generates mazes using recursive backtracing, solves them with one of a couple methods and then outputs a nice lil' GIF or in the terminal.

<img src="out.gif"/>

## Usage
### GIF with solution (same as preview above)
```python
from mazes import Maze

m = Maze(200 + 1, 200 + 1, save_gif=True)
m.shortest_path(method="dijkstra")
```
*Told you it was bad.*

### Output to terminal
```python
from mazes import Maze

m = Maze(200 + 1, 200 + 1)
m.print()
```

## Opportunities for Improvement
- Multithreading (GIF generation is super slow)
- Add generation algorithms other than backtracing
  - [Randomized Prim's](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm)
  - [Randomized Kruskal's](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Kruskal's_algorithm)
  - [Something Cellular Automata](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Cellular_automaton_algorithms) would be super cool
- GIF generation refactoring (relevant code is concise but not nicely OOP'ed)
- Better comments (as always)

## References
https://scipython.com/blog/making-a-maze/

https://levelup.gitconnected.com/solve-a-maze-with-python-e9f0580979a1

https://www.geeksforgeeks.org/stack-in-python/

https://algorithms.tutorialhorizon.com/depth-first-search-dfs-in-2d-matrix-2d-array-iterative-solution/

https://medium.com/swlh/solving-mazes-with-depth-first-search-e315771317ae

https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/

https://en.wikipedia.org/wiki/ANSI_escape_code

https://en.wikipedia.org/wiki/Maze_solving_algorithm#Random_mouse_algorithm

https://stackoverflow.com/questions/60532245/implementing-a-recursive-backtracker-to-generate-a-maze

https://courses.cs.washington.edu/courses/cse326/07su/prj2/kruskal.html