"""
Game of Life: console edition
"""

import curses
import random
import time
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Grid = List[List[int]]


class GameOfLife:
    """Defines the Game"""

    def __init__(self, size: Tuple[int, int], randomize: bool = False, max_generations: Optional[int] = None):
        self.height, self.width = size
        self.cell_size = 1
        self.speed = 10
        self.randomize = randomize
        self.max_generations = max_generations
        self.generations = 0
        self.grid: Grid = self.create_grid(randomize=randomize)
        self.prev_generation = self.create_grid(randomize=False)
        self.curr_generation = self.create_grid(randomize=randomize)

    def create_grid(self, randomize: bool = False) -> Grid:
        """Creates a grid"""

        if randomize:
            return [[random.randint(0, 1) for _ in range(self.width)] for _ in range(self.height)]
        else:
            return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_neighbours(self, cell: Cell) -> List[int]:
        """Finds neighbours of a cell"""

        i, j = cell
        neighbours = []
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if (x, y) != (i, j) and 0 <= x < self.height and 0 <= y < self.width:
                    neighbours.append(self.grid[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """Finds next generation of cells"""

        new_grid = self.create_grid(randomize=False)
        for i in range(self.height):
            for j in range(self.width):
                alive_neighbours = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 1:
                    new_grid[i][j] = 1 if alive_neighbours in (2, 3) else 0
                else:
                    new_grid[i][j] = 1 if alive_neighbours == 3 else 0
        return new_grid

    @property
    def grid(self):
        return self.curr_generation

    @grid.setter
    def grid(self, value):
        self.curr_generation = value

    @property
    def is_changing(self) -> bool:
        """Check if the grid has changed from the previous generation."""
        return hasattr(self, "prev_generation") and self.curr_generation != self.prev_generation

    @property
    def is_max_generations_exceeded(self) -> bool:
        """Check if max generations limit was reached."""
        return self.max_generations is not None and self.generations >= self.max_generations

    def step(self) -> None:
        """Changes the previous generation to next"""

        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1


class ConsoleUI:
    """Console version of Game of Life"""

    def __init__(self, life: GameOfLife, speed: float = 0.1):
        self.life = life
        self.speed = speed

    def draw(self, screen):
        screen.clear()
        height, width = screen.getmaxyx()

        for i, row in enumerate(self.life.curr_generation):
            if i >= height - 1:
                break
            for j, cell in enumerate(row):
                if j >= width - 1:
                    break
                screen.addch(i, j, "1" if cell else " ")

        screen.refresh()

    def run(self, screen):
        curses.curs_set(0)
        screen.nodelay(True)

        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            key = screen.getch()
            if key == ord("q"):
                break

            self.life.step()
            self.draw(screen)
            time.sleep(self.speed)


def main(stdscr):
    life = GameOfLife((25, 50), randomize=True, max_generations=None)
    ui = ConsoleUI(life, speed=0.05)
    ui.run(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
