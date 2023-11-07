import pygame
import sys
from enum import Enum
from typing import Tuple

class Cell(Enum):
    EMPTY = (0, 0, 255)
    SNAKE = (0, 255, 0)
    APPLE = (255, 0, 0)

class Snake:
    def __init__(self, size: Tuple[int, int], board_size: int, cell_size: int) -> None:
        self.width = size[0]
        self.height = size[1]
        self.cell_size = cell_size

        self.board: list[list[Cell]] = [[Cell.EMPTY for _ in range(board_size)] for _ in range(board_size)]

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def spawn_snake(self) -> None:
        self.board[1][0] = Cell.SNAKE

    def tick(self) -> None:
        # Draw the cells
        for y_coordinate, y in enumerate(self.board):
            for x_coordinate, x in enumerate(y):
                pygame.draw.rect(
                    self.screen,
                    x.value,
                    (y_coordinate * self.cell_size * 1.1,
                    x_coordinate * self.cell_size * 1.1,
                    self.cell_size,
                    self.cell_size)
                )

        pygame.display.flip()

    def should_close(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False