import pygame
import sys

def run(screen, font, beep_sound=None):
    clock = pygame.time.Clock()
    input_text = ""
    output_lines = [
        "RetroDOS v1.0 - Type HELP for commands",
        ""
    ]

    def draw_screen():
        screen.fill((0, 0, 0))
        scanline_color = (0, 40, 0)
        sw, sh = screen.get_size()
        for y in range(0, sh, 4):
            pygame.draw.line(screen, scanline_color, (0, y), (sw, y), 1)

        y_offset = 20
        # Show last 20 lines
        for line in output_lines[-20:]:
            rendered = font.render(line, True, (0, 255, 0))
            screen.blit(rendered, (20, y_offset))
            y_offset += 30

        prompt = font.render("> " + input_text, True, (0, 255, 0))
        screen.blit(prompt, (20, y_offset))
        pygame.display.flip()

    def process_command(cmd):
        cmd = cmd.strip().upper()
        if cmd == "HELP":
            output_lines.append("Available commands: HELP, DIR, CLS, EXIT")
        elif cmd == "CLS":
            output_lines.clear()
        elif cmd == "DIR":
            output_lines.append("Volume in drive C has no label.")  # Could change wording to "Volume in RetroDOS drive"
            output_lines.append("Volume Serial Number is 1234-ABCD")
            output_lines.append("Directory of RetroDOS drive")
            output_lines.append("01/01/2025  12:00AM <DIR> SYSTEM")
            output_lines.append("01/01/2025  12:00AM <DIR> USERS")
            output_lines.append("01/01/2025  12:00AM     12345 AUTOEXEC.BAT")
            output_lines.append("01/01/2025  12:00AM     23456 CONFIG.SYS")
        elif cmd == "EXIT":
            return False
        else:
            output_lines.append(f"'{cmd}' is not recognized as an internal or external command.")
        return True

    running = True
    while running:
        draw_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    output_lines.append("> " + input_text)
                    running = process_command(input_text)
                    input_text = ""
                else:
                    if event.unicode.isprintable():
                        input_text += event.unicode
                        if beep_sound and event.unicode.strip():
                            beep_sound.play()
        clock.tick(30)
