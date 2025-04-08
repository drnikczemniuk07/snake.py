import pygame
import random
import sys

# Konfiguracja
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 50)

clock = pygame.time.Clock()

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(win, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(win, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    win.blit(text, (10, 10))

def get_random_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return [x, y]

def draw_text_center(text, size, color, y_offset=0):
    f = pygame.font.SysFont("Arial", size)
    rendered = f.render(text, True, color)
    win.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, HEIGHT // 2 - rendered.get_height() // 2 + y_offset))

def difficulty_menu():
    selecting = True
    while selecting:
        win.fill(BLACK)
        draw_text_center("Choose Difficulty", 40, WHITE, -60)
        draw_text_center("1 - Easy (5 FPS)", 30, GREEN, 0)
        draw_text_center("2 - Medium (10 FPS)", 30, WHITE, 40)
        draw_text_center("3 - Hard (15 FPS)", 30, RED, 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 5
                elif event.key == pygame.K_2:
                    return 10
                elif event.key == pygame.K_3:
                    return 15

def game_over_screen(score):
    win.fill(BLACK)
    draw_text_center("Game Over", 50, RED, -40)
    draw_text_center(f"Your Score: {score}", 35, WHITE, 20)
    draw_text_center("Press ENTER to play again or ESC to quit", 25, WHITE, 70)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    speed = difficulty_menu()

    snake = [[100, 100]]
    direction = [CELL_SIZE, 0]
    food = get_random_food()
    score = 0

    running = True
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Sterowanie
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction[1] == 0:
            direction = [0, -CELL_SIZE]
        elif keys[pygame.K_DOWN] and direction[1] == 0:
            direction = [0, CELL_SIZE]
        elif keys[pygame.K_LEFT] and direction[0] == 0:
            direction = [-CELL_SIZE, 0]
        elif keys[pygame.K_RIGHT] and direction[0] == 0:
            direction = [CELL_SIZE, 0]

        head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        snake.insert(0, head)

        if head == food:
            score += 1
            food = get_random_food()
        else:
            snake.pop()

        if (head in snake[1:] or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT):
            game_over_screen(score)

        # Rysowanie
        win.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.update()

if __name__ == "__main__":
    main()
