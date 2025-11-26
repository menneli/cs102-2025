"""
Prototype for Game of Life
"""

import random
from typing import List, Tuple

import pygame
from pygame.locals import *

Cell = Tuple[int, int]
Grid = List[List[int]]


class GameOfLife:
    """Defines the Game"""

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed

        self.generations = 0
        self.max_generations = None
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Draws lines"""

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """Draw all cells with color based on their state."""
        for i, row in enumerate(self.curr_generation):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        """Starts the Game"""

        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.step()
            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """Creates a grid"""

        grid = []
        for _ in range(self.cell_height):
            if randomize:
                grid.append([random.randint(0, 1) for _ in range(self.cell_width)])
            else:
                grid.append([0 for _ in range(self.cell_width)])
        return grid

    def get_neighbours(self, cell: Cell) -> List[int]:
        """Finds neighbours of a cell"""

        i, j = cell
        neighbours = []
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if (x, y) != (i, j) and 0 <= x < self.cell_height and 0 <= y < self.cell_width:
                    neighbours.append(self.curr_generation[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """Finds next generation of cells"""

        new_grid = self.create_grid()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    if neighbours in [2, 3]:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if neighbours == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
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

    @property
    def grid(self) -> Grid:
        return self.curr_generation

    @grid.setter
    def grid(self, new_grid: Grid) -> None:
        self.curr_generation = new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
