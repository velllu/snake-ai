import pygame
import time
import sys
import random
from enum import Enum
from typing import List, Tuple

# Examples
# Input: (5, 2) and (2, 2)
# Output: (7, 4)
def add_positions(tuple1: Tuple[int, int], tuple2: Tuple[int, int]) -> Tuple[int, int]:
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])

class Cell(Enum):
    EMPTY = (0, 0, 255)
    SNAKE = (0, 255, 0)
    APPLE = (255, 0, 0)

# The tuples represent the position that will be added to the snake's position
class Direction(Enum):
    UP = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, 1)

class Snake:
    def __init__(self, size: Tuple[int, int], board_size: int, cell_size: int) -> None:
        self.width = size[0]
        self.height = size[1]
        self.board_size = board_size
        self.cell_size = cell_size

        self.snake_position: Tuple[int, int] = (0, 0)
        self.snake_positions: List[Tuple[int, int]] = []
        self.snake_size = 1
        self.current_direction: Direction = Direction.RIGHT

        self.is_apple_spawned = False

        self.events = []
        self.board: list[list[Cell]] = [[Cell.EMPTY for _ in range(board_size)] for _ in range(board_size)]

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

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

    # Checks if the position is inside the board
    def is_position_valid(self, position: Tuple[int, int]) -> bool:
        if position[0] < self.board_size and position[0] >= 0 \
            and position[1] < self.board_size and position[1] >= 0:

            return True

        return False

    def get_random_empty_position(self) -> Tuple[int, int]:
        empty_positions: List[Tuple[int, int]] = []

        for y_coordinate, y in enumerate(self.board):
            for x_coordinate, _ in enumerate(y):
                if self.board[x_coordinate][y_coordinate] == Cell.EMPTY:
                    empty_positions.append((x_coordinate, y_coordinate))

        return random.choice(empty_positions)

    def game_over(self):
        self.quit()

    def tick(self) -> None:
        self.update_events()

        # Snake mover
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.current_direction = Direction.UP
                elif event.key == pygame.K_a:
                    self.current_direction = Direction.LEFT
                elif event.key == pygame.K_s:
                    self.current_direction = Direction.DOWN
                elif event.key == pygame.K_d:
                    self.current_direction = Direction.RIGHT

        self.snake_positions.append(self.snake_position)
        if self.is_position_valid((self.snake_position[0], self.snake_position[1])):
            new_position = add_positions(self.snake_position, self.current_direction.value)

            # Before moving the snake, we check if the snake is gonna be on top of an
            # apple, if it's gonna eat itself or if it's even a valid position
            if not self.is_position_valid(new_position):
                self.game_over()
            elif self.board[new_position[0]][new_position[1]] == Cell.APPLE:
                self.snake_size += 1
                self.is_apple_spawned = False
            elif self.board[new_position[0]][new_position[1]] == Cell.SNAKE:
                self.game_over()

            # Moving the snake
            self.set_tile(new_position, Cell.SNAKE)

        # Snake size controller
        if len(self.snake_positions) > self.snake_size:
            self.set_tile(self.snake_positions[-self.snake_size], Cell.EMPTY)
            self.snake_positions.pop(-self.snake_size)

        # Apple spawner
        if not self.is_apple_spawned:
            self.set_tile(self.get_random_empty_position(), Cell.APPLE)
            self.is_apple_spawned = True

        self.draw_board()
                
        pygame.display.flip()
        pygame.time.delay(600)

    # We cannot call `pygame.event.get()` multiple times so we just store it in a variable
    def update_events(self):
        self.events = pygame.event.get()

    def should_close(self) -> bool:
        for event in self.events:
            if event.type == pygame.QUIT:
                return True

        return False