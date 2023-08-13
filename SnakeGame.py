import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the Snake class
class Snake:
    def __init__(self):
        self.body = [(width // 2, height // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.score = 0

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= 10
        elif self.direction == "DOWN":
            y += 10
        elif self.direction == "LEFT":
            x -= 10
        elif self.direction == "RIGHT":
            x += 10
        self.body.insert(0, (x, y))
        self.body.pop()

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = new_direction
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = new_direction
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = new_direction
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = new_direction

    def grow(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= 10
        elif self.direction == "DOWN":
            y += 10
        elif self.direction == "LEFT":
            x -= 10
        elif self.direction == "RIGHT":
            x += 10
        self.body.insert(0, (x, y))
        self.score += 1

    def check_collision(self):
        x, y = self.body[0]
        if x < 0 or x >= width or y < 0 or y >= height:
            return True
        for segment in self.body[1:]:
            if segment == (x, y):
                return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 10, 10))

# Define the Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, width // 10 - 1) * 10
        self.y = random.randint(0, height // 10 - 1) * 10

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 10, 10))

# Load the best score from a file
def load_best_score():
    try:
        with open("best_score.txt", "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        best_score = 0
    return best_score

# Save the best score to a file
def save_best_score(score):
    with open("best_score.txt", "w") as file:
        file.write(str(score))

# Create the Snake and Food objects
snake = Snake()
food = Food()

# Load the best score
best_score = load_best_score()

# Set up the clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.change_direction("RIGHT")

    # Move the snake
    snake.move()

    # Check for collision with the food
    if snake.body[0] == (food.x, food.y):
        snake.grow()
        food = Food()

    # Check for collision with the walls or itself
    if snake.check_collision():
        # Update the best score if the current score is higher
        if snake.score > best_score:
            best_score = snake.score
            save_best_score(best_score)
        running = False

    # Draw
    screen.fill(BLACK)
    snake.draw()
    food.draw()
    # Show score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(snake.score), True, GREEN)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(10)

# Print the final score
print("Your Score is =", snake.score)
print("Best Score is =", best_score)
# Quit the game
pygame.quit()
