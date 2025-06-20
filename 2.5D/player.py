import pygame
import math

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle  # in radians
        self.move_speed = 3.0  # units per second
        self.rot_speed = 2.5  # radians per second
        self.radius = 0.1  # for collision

    def update(self, dt, game):
        keys = pygame.key.get_pressed()

        # Rotation (left/right arrows or A/D)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle -= self.rot_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += self.rot_speed * dt

        # Movement (W/S or Up/Down)
        dx = 0
        dy = 0
        forward = keys[pygame.K_w] or keys[pygame.K_UP]
        backward = keys[pygame.K_s] or keys[pygame.K_DOWN]

        if forward:
            dx += math.cos(self.angle) * self.move_speed * dt
            dy += math.sin(self.angle) * self.move_speed * dt
        if backward:
            dx -= math.cos(self.angle) * self.move_speed * dt
            dy -= math.sin(self.angle) * self.move_speed * dt

        # Collision check before moving
        if not game.is_blocked(self.x + dx, self.y):
            self.x += dx
        if not game.is_blocked(self.x, self.y + dy):
            self.y += dy
