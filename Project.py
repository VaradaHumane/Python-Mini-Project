import tkinter as tk
import random

# Constants
WIDTH = 400
HEIGHT = 400
DELAY = 200
SNAKE_SIZE = 20


class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Snake Game")

        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.snake = Snake(self.canvas)
        self.apple = Apple(self.canvas)
        self.score = 0

        self.delay = DELAY
        self.game_over = False
        self.game_started = False

        self.bind("<KeyPress>", self.on_key_press)
        self.start_screen()

    def start_screen(self):
        self.canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text="Press any key to start",
            fill="black",
            font=("Trebuchet", 16),
            anchor="center",
        )

    def update(self):
        if not self.game_over and self.game_started:
            self.snake.move()
            self.check_collision()
            self.canvas.delete("all")
            self.draw_snake()
            self.draw_apple()
            self.canvas.create_text(
                50,
                10,
                text=f"Score: {self.score}",
                fill="black",
                font=("Trebuchet", 12),
                anchor="nw",
            )
            self.after(self.delay, self.update)
        elif self.game_over:
            self.canvas.create_text(
                WIDTH / 2,
                HEIGHT / 2,
                text=f"Game Over! Score: {self.score}",
                font=("Trebuchet", 16),
                anchor="center",
            )
            self.canvas.create_text(
                WIDTH / 2,
                HEIGHT / 2 + 30,
                text="Press R to restart",
                font=("Trebuchet", 14),
                anchor="center",
            )

    def draw_snake(self):
        for segment in self.snake.body:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="green"
            )

    def draw_apple(self):
        x, y = self.apple.position
        self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill="red")

    def check_collision(self):
        head = self.snake.body[0]
        apple_pos = self.apple.position

        if head == apple_pos:
            self.snake.grow()
            self.apple.move()
            self.score += 1
            self.delay -= 2

        if head in self.snake.body[1:]:
            self.game_over = True
        # if (
        #     head[0] < 0
        #     or head[0] >= WIDTH
        #     # or head[1] < 0
        #     # or head[1] >= HEIGHT
        #     or head in self.snake.body[1:]
        # ):
        #     self.game_over = True
        # if head[0] >= WIDTH:
        #     self.snake.move()
        # if head[1] >= HEIGHT:
        #     head[1] = 0

    def on_key_press(self, event):
        key = event.keysym
        if key == "r" and self.game_over:
            self.canvas.delete("all")
            self.restart_game()
        elif not self.game_started:
            self.game_started = True
            self.update()
        elif key == "Up" and self.snake.direction != "Down":
            self.snake.change_direction(key)
        elif key == "Down" and self.snake.direction != "Up":
            self.snake.change_direction(key)
        elif key == "Right" and self.snake.direction != "Left":
            self.snake.change_direction(key)
        elif key == "Left" and self.snake.direction != "Right":
            self.snake.change_direction(key)

    def restart_game(self):
        # print("hello")
        self.snake = Snake(self.canvas)
        self.apple = Apple(self.canvas)
        self.score = 0
        self.delay = DELAY
        self.game_over = False
        self.game_started = False
        self.start_screen()


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        x = random.randint(2, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(2, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.body = [(x, y)]
        self.direction = random.choice(["Up", "Down", "Left", "Right"])

    def move(self):
        x, y = self.body[0]

        if self.direction == "Up":
            if y <= 0:
                y = WIDTH
            else:
                y -= SNAKE_SIZE
        elif self.direction == "Down":
            if y >= WIDTH:
                y = 0
            else:
                y += SNAKE_SIZE
        elif self.direction == "Left":
            if x <= 0:
                x = HEIGHT
            else:
                x -= SNAKE_SIZE
        elif self.direction == "Right":
            if x >= HEIGHT:
                x = 0
            else:
                x += SNAKE_SIZE

        self.body.insert(0, (x, y))
        self.body.pop()

        # print(x, y)

    def grow(self):
        tail = self.body[-1]
        x, y = tail

        if self.direction == "Up":
            y += SNAKE_SIZE
        elif self.direction == "Down":
            y -= SNAKE_SIZE
        elif self.direction == "Left":
            x += SNAKE_SIZE
        elif self.direction == "Right":
            x -= SNAKE_SIZE

        self.body.append((x, y))

    def change_direction(self, direction):
        if (
            (self.direction == "Up" or self.direction == "Down")
            and (direction == "Left" or direction == "Right")
        ) or (
            (self.direction == "Left" or self.direction == "Right")
            and (direction == "Up" or direction == "Down")
        ):
            self.direction = direction


class Apple:
    def __init__(self, canvas):
        self.canvas = canvas
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        return x, y

    def move(self):
        self.position = self.generate_position()


game = SnakeGame()
game.mainloop()
