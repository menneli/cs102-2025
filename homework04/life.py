"""
Game of Life
"""

import random
from typing import List, Optional, Tuple

import pygame
from pygame.locals import K_SPACE, KEYDOWN, QUIT

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


class GUI:
    """Graphic interface"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        """Initializes the Game"""

        self.life = life
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        self.paused = False

    def draw_grid(self) -> None:
        """Creates the grid"""

        self.screen.fill(pygame.Color("white"))
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, pygame.Color("black"), rect, 1)

    def handle_pause_events(self) -> bool:
        """Handles events while paused; toggles cell state on mouse click"""

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // self.cell_size
                col = mouse_pos[0] // self.cell_size
                if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                    current = self.life.curr_generation[row][col]
                    self.life.curr_generation[row][col] = 0 if current == 1 else 1
            elif event.type == QUIT:
                return False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.paused = not self.paused
        return True

    def run(self) -> None:
        """Begins the Game"""

        pygame.init()  # pylint: disable=no-member
        clock = pygame.time.Clock()
        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            if self.paused:
                running = self.handle_pause_events()
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            self.paused = not self.paused

                if not self.paused:
                    self.life.step()

            self.draw_grid()

            if self.paused:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // self.cell_size
                col = mouse_pos[0] // self.cell_size
                if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                    rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, pygame.Color("red"), rect, 2)  # red border

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    life = GameOfLife((30, 50), randomize=True, max_generations=None)
    gui = GUI(life, cell_size=15, speed=5)
    gui.run()
