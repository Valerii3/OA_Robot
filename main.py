import random
import os
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class CellType(Enum):
    EMPTY = "."
    ROBOT = "R"
    OBSTACLE = "O"


class Cell:
    def __init__(self, cell_type=CellType.EMPTY):
        self.type = cell_type

    def __str__(self):
        return self.type.value


class Map:
    def __init__(self, n, s):
        self.grid = [[Cell() for _ in range(n)] for _ in range(n)]
        self.robot_pos = None
        self.n = n
        self.s = s

    def place_robot(self):
        x, y = random.randint(0, len(self.grid)-1), random.randint(0, len(self.grid)-1)
        self.grid[x][y].type = CellType.ROBOT
        self.robot_pos = (x, y)

    def place_obstacle(self):
        placed = False
        while not placed:
            x = random.randint(0, len(self.grid) - 1)
            y = random.randint(0, len(self.grid) - 1)
            if self.grid[x][y].type == CellType.EMPTY:
                self.grid[x][y].type = CellType.OBSTACLE
                placed = True

    def display(self):
        # Convert the grid to a color matrix for visualization
        color_map = []
        for row in self.grid:
            color_row = []
            for cell in row:
                if cell.type == CellType.EMPTY:
                    color_row.append(mcolors.to_rgba('white'))
                elif cell.type == CellType.OBSTACLE:
                    color_row.append(mcolors.to_rgba('black'))
                elif cell.type == CellType.ROBOT:
                    color_row.append(mcolors.to_rgba('red'))
            color_map.append(color_row)

        # Use imshow to display the color matrix
        fig, ax = plt.subplots()
        ax.imshow(color_map, extent=[0, self.n * self.s, 0, self.n * self.s])

        # Drawing gridlines for cells
        ax.set_xticks([x * self.s for x in range(self.n + 1)])
        ax.set_yticks([y * self.s for y in range(self.n + 1)])
        ax.grid(which="both", ls="-", lw=2, color='black')

        # Adding the coordinate numbers
        ax.set_xticklabels([str(x * self.s) for x in range(self.n + 1)])
        ax.set_yticklabels([str(y * self.s) for y in range(self.n, -1, -1)])

        # Move x-axis labels to the top
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

        # Remove axis spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        save_plot()
        plt.show()

    def obstacle_coordinates(self):
        robot_row, robot_col = self.robot_pos
        coords = {}

        # For North direction (0 degrees)
        for i in range(robot_row, -1, -1):
            if self.grid[i][robot_col].type == CellType.OBSTACLE:
                coords[0] = ((robot_col + 0.5) * self.s, (i + 1) * self.s)
                break
            elif i == 0:
                coords[0] = ((robot_col + 0.5) * self.s, i * self.s)

        # For East direction (90 degrees)
        for j in range(robot_col, len(self.grid)):
            if self.grid[robot_row][j].type == CellType.OBSTACLE:
                coords[90] = (j * self.s, (robot_row + 0.5) * self.s)
                break
            elif j == len(self.grid) - 1:
                coords[90] = (self.s * (j + 1), (robot_row + 0.5) * self.s)

        # For South direction (180 degrees)
        for i in range(robot_row, len(self.grid)):
            if self.grid[i][robot_col].type == CellType.OBSTACLE:
                coords[180] = ((0.5 + robot_col) * self.s, i * self.s)
                break
            elif i == len(self.grid) - 1:
                coords[180] = ((0.5 + robot_col) * self.s, (i + 1) * self.s)

        # For West direction (270 degrees)
        for j in range(robot_col, -1, -1):
            if self.grid[robot_row][j].type == CellType.OBSTACLE:
                coords[270] = (self.s * (j + 1), self.s * (0.5 + robot_row) )
                break
            elif j == 0:
                coords[270] = (self.s * j, self.s * (0.5 + robot_row))

        return coords


def save_plot():
    if os.path.exists("/app"):
        output_path = "/app/output/map_visualization.png"
    else:
        output_path = "output/map_visualization.png"

    plt.savefig(output_path)


def get_user_input():
    n = int(input("Enter the size of the map (n x n): "))
    s = int(input("Enter the cell size of the map: "))
    return n, s


def main():
    n, s = get_user_input()
    game_map = Map(n, s)

    # Place robot and obstacles
    game_map.place_robot()
    num_obstacles = random.randint(1, n * n // 2)

    for _ in range(num_obstacles):
        game_map.place_obstacle()

    # Display the filled map
    game_map.display()
    coord = game_map.obstacle_coordinates()
    print(f"Obstacle coordinates: {coord}")


if __name__ == "__main__":
    main()
