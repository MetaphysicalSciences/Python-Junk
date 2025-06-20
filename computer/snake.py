import pygame
import sys
import random

def run(screen, font):
    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()

    # Grid size for snake (classic 20x15 blocks for 320x200)
    grid_size = 20
    cols = screen_width // grid_size
    rows = screen_height // grid_size

    # Colors
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 100, 0)

    # Snake start position
    snake = [(cols//2, rows//2)]
    direction = (1, 0)  # moving right initially

    # Place first food
    def place_food():
        while True:
            pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if pos not in snake:
                return pos

    food = place_food()
    score = 0
    game_over = False

    def draw_scanlines():
        scanline_color = (0, 40, 0)
        for y in range(0, screen_height, 4):
            pygame.draw.line(screen, scanline_color, (0, y), (screen_width, y), 1)

    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        if not game_over:
            # Move snake
            new_head = ((snake[0][0] + direction[0]) % cols, (snake[0][1] + direction[1]) % rows)
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = place_food()
                else:
                    snake.pop()

        # Draw everything
        screen.fill(BLACK)
        draw_scanlines()

        # Draw snake
        for segment in snake:
            rect = pygame.Rect(segment[0]*grid_size, segment[1]*grid_size, grid_size, grid_size)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, DARK_GREEN, rect, 1)

        # Draw food
        food_rect = pygame.Rect(food[0]*grid_size, food[1]*grid_size, grid_size, grid_size)
        pygame.draw.rect(screen, (255, 0, 0), food_rect)

        # Score and instructions
        score_surf = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_surf, (20, 20))

        instr = font.render("Arrow keys to move, ESC to exit", True, GREEN)
        screen.blit(instr, (20, screen_height - 40))

        if game_over:
            over_text = font.render("Game Over! Press ESC to return", True, (255, 0, 0))
            screen.blit(over_text, (screen_width//2 - over_text.get_width()//2, screen_height//2))

        pygame.display.flip()
