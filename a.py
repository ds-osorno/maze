import sys
from node import Node

from stackfrontier import StackFrontier
from queuefrontier import QueueFrontier
from listFrontier import ListFrontier


class Maze:
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        self.explored = set()

    def neighbours(self, state):
        row, col = state
        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]
        actions = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    actions.append((action, (r, c)))
            except:
                continue
        return actions

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print('S', end="")
                elif (i, j) == self.goal:
                    print("E", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(' ', end="")
            print("")
        print()

    def solve(self):
        def h(state):
            x, y = self.goal
            a, b = state
            d = abs(x-a)+abs(y-b)
            return d

        def get_nearest_node():
            nodes = self.frontier.all()
            distances = {node: h(node.state)+node.distance for node in nodes}
            best_node = min(distances, key=lambda x: distances.get(x))
            self.frontier.remove(best_node)
            return best_node

        self.frontier = ListFrontier()

        node = Node(state=self.start, parent=None, action=None)
        self.num_explored = 0
        self.set_explored = set()
        self.frontier.add(node)

        while True:

            node = get_nearest_node()
            self.num_explored += 1
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.set_explored.add(node.state)
            for action, state in self.neighbours(node.state):
                if state not in self.set_explored and not self.frontier.contains_state(state):
                    child = Node(state, node, action)
                    self.frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


def main():

    m3 = Maze("long.txt")
    print("Maze A Start:")
    m3.print()
    print("Solving A Start...")
    m3.solve()
    print("States Explored:", m3.num_explored)
    print("Solution A Start:")
    m3.print()
    m3.output_image("maze_AStart.png", show_explored=True)


if __name__ == '__main__':
    main()
