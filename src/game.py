import pygame
import sys

class Snake:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        pygame.init()
        screen = pygame.display.set_mode((width, height))

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    def tick(self) -> None:
        pass

    def should_close(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False