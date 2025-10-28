import pygame
import sys
import random

# ---- Game Config ----
CELL = 20
COLUMNS = 30
ROWS = 20
WIDTH = CELL * COLUMNS
HEIGHT = CELL * ROWS
FPS = 10  # starting speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
GRAY = (50, 50, 50)
BLUE = (30, 144, 255)
BORDER = (200, 200, 200)

# ---- Helper functions ----
def random_food_position(snake):
    while True:
        pos = (random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos

def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

# ---- Main Game ----
def main():
    global FPS  # must be declared before using FPS inside the function

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 40))  # space for score
    pygame.display.set_caption("🐍 Snake Game by Vakula Reddy")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Consolas', 20)
    big_font = pygame.font.SysFont('Consolas', 36)

    # initial snake (center)
    start_x = COLUMNS // 2
    start_y = ROWS // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = (1, 0)
    food = random_food_position(snake)
    score = 0
    game_over = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    # restart
                    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
                    direction = (1, 0)
                    food = random_food_position(snake)
                    score = 0
                    game_over = False
                    FPS = 10  # reset speed

        if not paused and not game_over:
            # move snake
            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])

            # check wall collision
            if new_head[0] < 0 or new_head[0] >= COLUMNS or new_head[1] < 0 or new_head[1] >= ROWS:
                game_over = True
            # check self collision
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                # eating food?
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    # increase speed every 5 points
                    if score % 5 == 0:
                        FPS = min(FPS + 2, 25)
                else:
                    snake.pop()

        # draw everything
        screen.fill(BLACK)
        play_surface = pygame.Surface((WIDTH, HEIGHT))
        play_surface.fill(BLACK)

        # border
        pygame.draw.rect(play_surface, BORDER, (0, 0, WIDTH, HEIGHT), 2)

        # draw food
        fx, fy = food
        pygame.draw.rect(play_surface, RED, (fx * CELL, fy * CELL, CELL, CELL))

        # draw snake
        for i, segment in enumerate(snake):
            rect = pygame.Rect(segment[0] * CELL, segment[1] * CELL, CELL, CELL)
            color = BLUE if i == 0 else GREEN
            pygame.draw.rect(play_surface, color, rect)

        # grid optional (comment out if you don’t like it)
        # draw_grid(play_surface)
        screen.blit(play_surface, (0, 0))

        # score area
        pygame.draw.rect(screen, (30, 30, 30), (0, HEIGHT, WIDTH, 40))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT + 8))
        hint_text = font.render("P: Pause  R: Restart  Arrows/WASD to Move", True, WHITE)
        screen.blit(hint_text, (180, HEIGHT + 8))

        if paused:
            pa_text = big_font.render("PAUSED", True, (255, 255, 0))
            screen.blit(pa_text, (WIDTH // 2 - pa_text.get_width() // 2, HEIGHT // 2 - 20))

        if game_over:
            go_text = big_font.render("GAME OVER", True, RED)
            screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 20))
            sub = font.render("Press R to Restart or Close to Exit", True, WHITE)
            screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
