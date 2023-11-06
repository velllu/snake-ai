import game

if __name__ == "__main__":
    snake = game.Snake(500, 500)

    while not snake.should_close():
        snake.tick()