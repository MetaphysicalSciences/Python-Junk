import pygame
import sys

# Expanded fake file system data with important system files and folders
fake_fs = {
    "RetroDOSDrive": {
        "SYSTEM": {
            "IO.SYS": "System file essential for boot",
            "MSDOS.SYS": "System core file",
            "COMMAND.COM": "Command interpreter",
            "CONFIG.SYS": "System configuration file",
            "AUTOEXEC.BAT": "Batch file executed on startup"
        },
        "USERS": {
            "Guest": {
                "README.TXT": "Welcome to RetroDOS!\nFeel free to explore.",
                "GUEST.LOG": "Guest user logs."
            },
            "Admin": {
                "SECRET.DAT": "Top secret data.",
                "CONFIG.TXT": "Admin user config file."
            }
        },
        "PROGRAMS": {
            "INSTALL.EXE": "Installer executable",
            "README.TXT": "Important program readme."
        },
        "LOGS": {
            "SYSTEM.LOG": "System event logs",
            "ERROR.LOG": "Error logs"
        },
        "AUTOEXEC.BAT": "Batch file executed on startup",
        "CONFIG.SYS": "System configuration file"
    }
}

def run(screen, font):
    clock = pygame.time.Clock()
    path_stack = ["RetroDOSDrive"]

    def get_current_dir():
        dir = fake_fs
        for p in path_stack:
            dir = dir[p]
        return dir

    def draw_screen(selected_index):
        screen.fill((0, 0, 0))
        scanline_color = (0, 40, 0)
        sw, sh = screen.get_size()
        for y in range(0, sh, 4):
            pygame.draw.line(screen, scanline_color, (0, y), (sw, y), 1)

        header_text = "File Manager - UP/DOWN: Navigate  ENTER: Open  BACKSPACE: Back  ESC: Exit"
        header = font.render(header_text, True, (0, 255, 0))
        screen.blit(header, (20, 10))

        current_dir = get_current_dir()
        items = list(current_dir.keys())
        y_offset = 50

        for i, item in enumerate(items):
            prefix = "<DIR>" if isinstance(current_dir[item], dict) else "     "
            text_color = (0, 255, 0)
            if i == selected_index:
                pygame.draw.rect(screen, (0, 100, 0), (15, y_offset - 5, 700, 30))
                text_color = (0, 255, 255)
            item_text = font.render(f"{prefix} {item}", True, text_color)
            screen.blit(item_text, (20, y_offset))
            y_offset += 35

        pygame.display.flip()
        return items

    selected_index = 0
    running = True
    while running:
        items = draw_screen(selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(items) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    current_dir = get_current_dir()
                    selected_item = items[selected_index]
                    if isinstance(current_dir[selected_item], dict):
                        path_stack.append(selected_item)
                        selected_index = 0
                    else:
                        show_file(screen, font, selected_item, current_dir[selected_item])
                elif event.key == pygame.K_BACKSPACE:
                    if len(path_stack) > 1:
                        path_stack.pop()
                        selected_index = 0
        clock.tick(30)

def show_file(screen, font, filename, content):
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        scanline_color = (0, 40, 0)
        sw, sh = screen.get_size()
        for y in range(0, sh, 4):
            pygame.draw.line(screen, scanline_color, (0, y), (sw, y), 1)

        header = font.render(f"File: {filename}", True, (0, 255, 0))
        screen.blit(header, (20, 20))

        lines = content.split('\n') if isinstance(content, str) else [str(content)]
        y_offset = 60
        for line in lines:
            rendered = font.render(line, True, (0, 255, 0))
            screen.blit(rendered, (20, y_offset))
            y_offset += 30

        instr = font.render("Press ESC to return", True, (0, 255, 0))
        screen.blit(instr, (20, sh - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        clock.tick(30)
