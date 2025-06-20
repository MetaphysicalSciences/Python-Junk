import pygame
import time
import random
import shutil
import datetime
import sys
import os
import dos_prompt
import calculator
import file_manager
import snake
import AtariBreakOut
import SpaceInvaders

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("RetroDos Boot Simulation")
font = pygame.font.SysFont("Courier New", 24)
clock = pygame.time.Clock()
screen_width, screen_height = screen.get_size()

# System Info
total, used, free = shutil.disk_usage("C:/")
free_mb = free // (1024 * 1024)
now = datetime.datetime.now()
current_date = now.strftime("%m-%d-%Y")
current_time = now.strftime("%H:%M:%S.%f")[:-3]

boot_lines = [
    "Starting MS-DOS...",
    "HIMEM.SYS Installed",
    "EMM386.EXE Active",
    "SMARTDRV.SYS Loaded - Disk Caching Enabled",
    "Installing Keyboard Driver... Keyboard Ready",
    "Mouse Driver Loaded - PS/2 Mouse Detected",
    "CONFIG.SYS processed successfully",
    "AUTOEXEC.BAT executed",
    "Checking Drive C: for errors...",
    "Scanning FAT tables... OK",
    "Checking directory structure... OK",
    "Checking available disk space...",
    f"Drive C: {free_mb} MB Free",
    "",
    "Initializing graphics mode 320x200x256 colors...",
    "Setting up sound system... SoundBlaster Compatible Detected",
    "",
    "MS-DOS Version 6.22",
    f"System date is {current_date}",
    f"System time is {current_time}",
    "",
    "Ready.",
    "",
    "Launching RetroDos v1.0",
    "Press any key to start..."
]

def draw_scanlines():
    scanline_color = (0, 40, 0)
    for y in range(0, screen_height, 4):
        pygame.draw.line(screen, scanline_color, (0, y), (screen_width, y), 1)

def type_line(text, y_offset):
    typed = ""
    for char in text:
        typed += char
        render = font.render(typed, True, (0, 255, 0))
        screen.blit(render, (40, y_offset))
        draw_scanlines()
        pygame.display.flip()
        time.sleep(random.uniform(0.01, 0.03))
    return y_offset + 32

def wait_for_keypress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def shutdown_screen():
    screen.fill((0, 0, 0))
    draw_scanlines()
    pygame.display.flip()

    messages = [
        "Saving configuration...",
        "Unmounting drives...",
        "Releasing memory buffers...",
        "Terminating processes...",
        "Shutting down RetroDos..."
    ]

    y = 200
    for message in messages:
        typed = ""
        for char in message:
            typed += char
            render = font.render(typed, True, (0, 255, 0))
            screen.blit(render, (80, y))
            draw_scanlines()
            pygame.display.flip()
            time.sleep(0.02)
        y += 40
        time.sleep(0.6)

    time.sleep(1)
    pygame.quit()
    sys.exit()

def launching_animation(text, y_offset):
    dots = ""
    for _ in range(15):
        dots += "."
        if len(dots) > 3:
            dots = ""
        line = f"{text}{dots}"
        screen.fill((0, 0, 0))
        draw_scanlines()
        render = font.render(line, True, (0, 255, 0))
        screen.blit(render, (40, y_offset))
        pygame.display.flip()
        time.sleep(0.4)

def render_desktop():
    screen.fill((0, 0, 0))
    draw_scanlines()
    header = font.render("RetroDos v1.0", True, (0, 255, 0))
    screen.blit(header, (screen_width // 2 - header.get_width() // 2, 20))

    apps = [
        "[1] DOS Prompt",
        "[2] Calculator",
        "[3] File Manager",
        "[4] Snake",
        "[5] Atari Breakout",
        "[6] Space Invaders",   # <- New line
        "[7] Shutdown"          # <- Moved down
    ]

    y = 100
    for app in apps:
        app_text = font.render(app, True, (0, 255, 0))
        screen.blit(app_text, (60, y))
        y += 40

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == '1':
                    launching_animation("Launching DOS Prompt", 400)
                    dos_prompt.run(screen, font)
                    render_desktop()
                elif event.unicode == '2':
                    launching_animation("Launching Calculator", 400)
                    calculator.run(screen, font)
                    render_desktop()
                elif event.unicode == '3':
                    launching_animation("Launching File Manager", 400)
                    file_manager.run(screen, font)
                    render_desktop()
                elif event.unicode == '4':
                    launching_animation("Launching Snake", 400)
                    snake.run(screen, font)
                    render_desktop()
                elif event.unicode == '5':
                    launching_animation("Launching Atari Breakout", 400)
                    AtariBreakOut.run(screen, font)
                    render_desktop()
                elif event.unicode == '6':
                    launching_animation("Launching Space Invaders", 400)
                    SpaceInvaders.run(screen, font)
                    render_desktop()
                elif event.unicode == '7':
                    shutdown_screen()

def main():
    screen.fill((0, 0, 0))
    y = 40
    for line in boot_lines:
        y = type_line(line, y)
        time.sleep(random.uniform(0.05, 0.15))

    wait_for_keypress()
    render_desktop()

if __name__ == "__main__":
    main()
