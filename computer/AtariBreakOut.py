import pygame
import random
import sys
import time

def run(screen, font):
    # Retro colors
    BG_COLOR = (0, 0, 0)
    GREEN = (0, 255, 0)
    SCANLINE_COLOR = (0, 40, 0)
    screen_width, screen_height = screen.get_size()

    paddle_width = 100
    paddle_height = 15
    ball_radius = 10

    # Paddle
    paddle_x = screen_width // 2 - paddle_width // 2
    paddle_y = screen_height - 60
    paddle_speed = 8

    # Ball
    ball_x = screen_width // 2
    ball_y = paddle_y - ball_radius - 1
    ball_speed_x = 5 * random.choice([-1, 1])
    ball_speed_y = -5

    # Bricks
    brick_rows = 6
    brick_cols = 10
    brick_width = (screen_width - 100) // brick_cols
    brick_height = 25
    bricks = []

    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = 50 + col * brick_width
            brick_y = 50 + row * brick_height
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width - 4, brick_height - 4))

    score = 0
    lives = 3

    clock = pygame.time.Clock()

    def draw_scanlines():
        for y in range(0, screen_height, 4):
            pygame.draw.line(screen, SCANLINE_COLOR, (0, y), (screen_width, y), 1)

    def draw_text(text, x, y):
        rendered = font.render(text, True, GREEN)
        screen.blit(rendered, (x, y))

    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_scanlines()

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle_x += paddle_speed
        paddle_x = max(0, min(screen_width - paddle_width, paddle_x))

        # Move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

        # Ball collision with paddle
        if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
            ball_speed_y *= -1
            # Change horizontal speed based on where it hits the paddle
            hit_pos = (ball_x - paddle_x) / paddle_width - 0.5
            ball_speed_x = 7 * hit_pos

        # Ball collision with walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
            ball_speed_x *= -1
        if ball_y - ball_radius <= 0:
            ball_speed_y *= -1

        # Ball missed paddle
        if ball_y - ball_radius > screen_height:
            lives -= 1
            if lives <= 0:
                # Game over screen
                screen.fill(BG_COLOR)
                draw_scanlines()
                game_over_text = font.render("GAME OVER - Press ESC to return", True, GREEN)
                screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2))
                pygame.display.flip()
                waiting = True
                while waiting:
                    for e in pygame.event.get():
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                            return
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            else:
                # Reset ball and paddle position
                ball_x = screen_width // 2
                ball_y = paddle_y - ball_radius - 1
                ball_speed_x = 5 * random.choice([-1, 1])
                ball_speed_y = -5
                paddle_x = screen_width // 2 - paddle_width // 2
                time.sleep(1)

        # Ball collision with bricks
        hit_index = ball_rect.collidelist(bricks)
        if hit_index != -1:
            hit_brick = bricks.pop(hit_index)
            ball_speed_y *= -1
            score += 10

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        # Draw paddle
        pygame.draw.rect(screen, GREEN, paddle_rect)


        pygame.draw.circle(screen, GREEN, (int(ball_x), int(ball_y)), ball_radius)

 
        draw_text(f"Score: {score}", 20, screen_height - 40)
        draw_text(f"Lives: {lives}", screen_width - 140, screen_height - 40)

        pygame.display.flip()
        clock.tick(60)
