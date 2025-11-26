"""
Game of Life
"""

import pathlib
import random
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Grid = List[List[int]]


class GameOfLife:
    """Defines the Game"""

    def __init__(self, size: Tuple[int, int], randomize: bool = True, max_generations: Optional[int] = None) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """Creates a grid"""

        grid = []
        for _ in range(self.rows):
            if randomize:
                grid.append([random.randint(0, 1) for _ in range(self.cols)])
            else:
                grid.append([0 for _ in range(self.cols)])
        return grid

    def get_neighbours(self, cell: Cell) -> List[int]:
        """Finds neighbours of a cell"""

        i, j = cell
        neighbours = []
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if (x, y) != (i, j) and 0 <= x < self.rows and 0 <= y < self.cols:
                    neighbours.append(self.curr_generation[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """Finds next generation of cells"""

        new_grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    if neighbours in [2, 3]:
                        new_grid[i][j] = 1
                else:
                    if neighbours == 3:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """Changes the previous generation to next"""

        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """Checks if max generations were exceeded"""

        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """Checks that the cells are actually changing"""

        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Load a grid from a text file and return a GameOfLife instance"""
        with open(filename, encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        grid = [[int(ch) for ch in line] for line in lines]

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        life = GameOfLife((rows, cols), randomize=False)
        life.curr_generation = grid
        life.prev_generation = life.create_grid()
        return life

    def save(self, filename: pathlib.Path) -> None:
        """Save current grid to a file"""
        with open(filename, "w", encoding="utf-8") as f:
            for row in self.curr_generation:
                f.write("".join(str(cell) for cell in row) + "\n")
