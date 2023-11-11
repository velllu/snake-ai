import game

if __name__ == "__main__":
    snake = game.Snake((500, 500), 10, 30)
    snake.spawn_snake()

    while not snake.should_close():
        snake.tick()