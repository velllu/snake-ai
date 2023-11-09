import pygame
import sys
from enum import Enum
from typing import Tuple

class Cell(Enum):
    EMPTY = (0, 0, 255)
    SNAKE = (0, 255, 0)
    APPLE = (255, 0, 0)

class Direction(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

class Snake:
    def __init__(self, size: Tuple[int, int], board_size: int, cell_size: int) -> None:
        self.width = size[0]
        self.height = size[1]
        self.snake_position: Tuple[int, int] = (0, 0)
        self.current_direction: Direction = Direction.RIGHT
        self.board_size = board_size
        self.cell_size = cell_size

        self.board: list[list[Cell]] = [[Cell.EMPTY for _ in range(board_size)] for _ in range(board_size)]

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def spawn_snake(self) -> None:
        self.set_tile((self.snake_position[0], self.snake_position[1]), Cell.SNAKE)

    def set_tile(self, position: Tuple[int, int], cell_type: Cell) -> None:
        self.board[position[0]][position[1]] = cell_type

        if cell_type == Cell.SNAKE:
            self.snake_position = position

    def draw_board(self) -> None:
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

    def tick(self) -> None:
        # TODO: Add left, down, and up, and check if the next position is gonna be valid
        # or not
        if self.current_direction == Direction.RIGHT and self.board_size > self.snake_position[0] + 1:
            self.set_tile((self.snake_position[0] + 1, self.snake_position[1]), Cell.SNAKE)

        self.draw_board()
                
        pygame.display.flip()

    def should_close(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False