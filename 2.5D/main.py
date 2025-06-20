import pygame
from game import Game
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2.5D Engine Demo")

    clock = pygame.time.Clock()

    # Create player starting in middle of map, facing right (0 degrees)
    player = Player(x=3.5, y=3.5, angle=0)

    # Create game instance (map, rendering)
    game = Game(screen, player)

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(dt, game)

        screen.fill((30, 30, 30))
        game.render()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
