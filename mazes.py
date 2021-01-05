# https://scipython.com/blog/making-a-maze/
# https://levelup.gitconnected.com/solve-a-maze-with-python-e9f0580979a1
# https://www.geeksforgeeks.org/stack-in-python/
# https://algorithms.tutorialhorizon.com/depth-first-search-dfs-in-2d-matrix-2d-array-iterative-solution/
# https://medium.com/swlh/solving-mazes-with-depth-first-search-e315771317ae
# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://en.wikipedia.org/wiki/Maze_solving_algorithm#Random_mouse_algorithm
# https://stackoverflow.com/questions/60532245/implementing-a-recursive-backtracker-to-generate-a-maze
# https://courses.cs.washington.edu/courses/cse326/07su/prj2/kruskal.html

import random
from queue import PriorityQueue

from PIL import Image


class Maze:
    def __init__(self, width, height, start=None, end=None, save_gif=False):
        self.width = width
        self.height = height
        self.save_gif = save_gif

        self.arr = [[1 for _ in range(self.width)] for _ in range(self.height)]
        if not start:
            self.start = (1, 1)
        if not end:
            self.end = (self.width - 2, self.height - 2)

        self.images = []
        if save_gif:
            self.images = [self.to_image()]

        self.recursive_backtrace()

    def recursive_backtrace(self):
        stack = [self.start]

        while stack:
            x, y = stack.pop()

            directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            valid = [
                [dx, dy]
                for dx, dy in directions
                if self.is_wall(x + (dx * 2), y + (dy * 2))
            ]

            if valid:
                stack.append((x, y))

                dx, dy = random.choice(valid)

                x1, y1 = (x + dx, y + dy)
                self.arr[y1][x1] = 0

                if self.save_gif:
                    self.images.append(self.to_image())

                x2, y2 = (x + (dx * 2), y + (dy * 2))
                self.arr[y2][x2] = 0

                if self.save_gif:
                    self.images.append(self.to_image())

                stack.append((x2, y2))

    def is_wall(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.arr[y][x] == 1
        return False

    def is_path(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.arr[y][x] == 0
        return False

    def neighbors(self, x, y, radius=1, type="path"):
        def desired_type(x, y):
            if type == "path":
                return self.is_path(x, y)
            elif type == "wall":
                return self.is_wall(x, y)
            else:
                raise Exception("Unknown neighbor type: " + type)

        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        out = []

        for direction in directions:
            n = (x + (direction[0] * radius), y + (direction[1] * radius))
            if desired_type(*n):
                out += [n]

        return out

    def random_mouse(self):
        path = [self.start]
        while path[-1] != self.end:
            x, y = path[-1]
            path += [random.choice(self.neighbors(x, y))]
        return path

    def dfs(self):
        stack = []
        visited = []

        stack.insert(0, self.start)

        while stack:
            # grab the next pos off the stack
            x, y = stack[0]

            # mark pos as visited
            visited += [(x, y)]

            # if we're at the end cell, we're done
            if (x, y) == self.end:
                break

            # filter for only neighboring pos that are not visited
            neighbors = [n for n in self.neighbors(x, y) if n not in visited]

            if neighbors:
                # let's go to the first neighbor
                stack.insert(0, neighbors[0])
            else:
                # there's nowhere else to go! backtrace to most recent successful cell.
                stack.pop(0)

        return stack

    def dijkstra(self):
        # mapping position -> length of shortest route there
        # defaults to infinity so our less than updating works
        dist = {
            (x, y): float("inf") for x in range(self.width) for y in range(self.height)
        }

        # mapping position -> previous pos in shortest route
        prev = {(x, y): None for x in range(self.width) for y in range(self.height)}

        dist[self.start] = 0

        # used to pick the shortest route neighbor, optimizing time
        pq = PriorityQueue()
        pq.put((0, self.start))

        while not pq.empty():
            current_distance, current = pq.get()
            x, y = current

            # if the current way we got here isn't better than the best we've done before, skip it
            # we need this because our implementation of PriorityQueue doesn't allow updating, so we have duplicates pushed in
            if current_distance > dist[current]:
                continue

            for neighbor in self.neighbors(x, y):
                distance = current_distance + 1
                # if we've found a better route, remember it as the best
                if distance < dist[neighbor]:
                    dist[neighbor] = distance
                    prev[neighbor] = current
                    pq.put((distance, neighbor))

        # trace from the end back to the begining using the prev dict
        out = [self.end]
        while out[-1] != self.start:
            out += [prev[out[-1]]]
        return out

    def shortest_path(self, method="dijkstra"):
        if method in ["random_mouse", "dfs", "dijkstra"]:
            path = getattr(self, method)()
        else:
            raise Exception("Unexpected shortest path method:" + method)

        new_arr = [row[:] for row in self.arr]

        for x, y in reversed(path):
            if self.end != (x, y) and self.start != (x, y):
                new_arr[y][x] = "P"
                if self.save_gif:
                    m = Maze(len(new_arr), len(new_arr[0]))
                    m.arr = new_arr
                    self.images.append(m.to_image())

        if self.save_gif:
            self.images[0].save(
                "out.gif",
                save_all=True,
                append_images=self.images[1:],
                optimize=True,
                duration=40,
                loop=0,
            )

        m = Maze(len(new_arr), len(new_arr[0]))
        m.arr = new_arr
        return m

    def print(self):
        block = "\033[48;5;{0}m  \033[0m"
        colors = {
            0: "  ",
            1: block.format(8),
            "P": block.format(6),
            "S": block.format(10),
            "E": block.format(9),
        }

        out = ""

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.start:
                    out += colors["S"]
                elif (x, y) == self.end:
                    out += colors["E"]
                else:
                    out += colors[self.arr[y][x]]
            out += "\n"

        print("\n" + out)

    def to_image(self):
        colors = {
            1: (76, 86, 106, 255),
            0: (46, 52, 64, 255),
            "P": (136, 192, 208, 255),
            "S": (163, 190, 140, 255),
            "E": (191, 97, 106, 255),
        }

        data = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.start:
                    data += [colors["S"]]
                elif (x, y) == self.end:
                    data += [colors["E"]]
                else:
                    data += [colors[self.arr[y][x]]]

        im = Image.new("RGBA", (self.width, self.height), "white")
        im.putdata(data)

        return im


if __name__ in "__main__":
    m = Maze(200 + 1, 200 + 1, save_gif=True)
    m.shortest_path(method="dijkstra")
