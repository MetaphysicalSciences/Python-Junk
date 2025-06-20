import pygame
import sys

def run(screen, font):
    clock = pygame.time.Clock()
    expression = ""
    result = ""

    def draw_screen():
        screen.fill((0, 0, 0))
        scanline_color = (0, 40, 0)
        sw, sh = screen.get_size()
        for y in range(0, sh, 4):
            pygame.draw.line(screen, scanline_color, (0, y), (sw, y), 1)

        title = font.render("Calculator - Type expression and press Enter", True, (0, 255, 0))
        screen.blit(title, (20, 20))

        expr_render = font.render(expression, True, (0, 255, 0))
        screen.blit(expr_render, (20, 60))

        res_render = font.render("Result: " + result, True, (0, 255, 0))
        screen.blit(res_render, (20, 100))

        instr = font.render("Press ESC to exit", True, (0, 255, 0))
        screen.blit(instr, (20, sh - 40))

        pygame.display.flip()

    running = True
    while running:
        draw_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    expression = expression[:-1]
                elif event.key == pygame.K_RETURN:
                    try:
                        allowed_chars = "0123456789+-*/(). "
                        if all(c in allowed_chars for c in expression):
                            result = str(eval(expression))
                        else:
                            result = "Error: Invalid characters"
                    except Exception:
                        result = "Error: Invalid expression"
                else:
                    if event.unicode in "0123456789+-*/(). ":
                        expression += event.unicode
        clock.tick(30)
