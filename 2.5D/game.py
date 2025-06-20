import pygame
import math

class Game:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.width, self.height = self.screen.get_size()

        self.map = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,2,0,0,0,1],
            [1,2,0,0,0,0,0,1,2,1],
            [1,0,0,0,0,0,0,1,0,1],
            [1,1,0,0,0,0,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1],
        ]

        self.block_shapes = {
            1: [  # full block
                ((0,0),(1,0)), ((1,0),(1,1)), ((1,1),(0,1)), ((0,1),(0,0)),
            ],
            2: [  # pillar
                ((0.4,0.4),(0.6,0.4)), ((0.6,0.4),(0.6,0.6)),
                ((0.6,0.6),(0.4,0.6)), ((0.4,0.6),(0.4,0.4)),
            ],
        }

        self.fov = math.pi / 3
        self.num_rays = 160
        self.max_depth = 20

    def is_blocked(self, x, y):
        cx, cy = int(x), int(y)
        if cy < 0 or cy >= len(self.map) or cx < 0 or cx >= len(self.map[0]):
            return True
        block_type = self.map[cy][cx]
        if block_type == 0:
            return False
        lx, ly = x - cx, y - cy
        shape = self.block_shapes.get(block_type)
        if not shape: return False
        min_x = min(p[0] for seg in shape for p in seg)
        max_x = max(p[0] for seg in shape for p in seg)
        min_y = min(p[1] for seg in shape for p in seg)
        max_y = max(p[1] for seg in shape for p in seg)
        return min_x <= lx <= max_x and min_y <= ly <= max_y

    def cast_ray(self, angle):
        px, py = self.player.x, self.player.y
        sin_a, cos_a = math.sin(angle), math.cos(angle)
        for depth in range(1, int(self.max_depth * 100)):
            d = depth / 100.0
            x, y = px + cos_a * d, py + sin_a * d
            cx, cy = int(x), int(y)
            if cy < 0 or cy >= len(self.map) or cx < 0 or cx >= len(self.map[0]):
                return self.max_depth, 0
            block = self.map[cy][cx]
            if block == 0: continue
            lx, ly = x - cx, y - cy
            shape = self.block_shapes.get(block)
            if not shape: continue
            min_x = min(p[0] for seg in shape for p in seg)
            max_x = max(p[0] for seg in shape for p in seg)
            min_y = min(p[1] for seg in shape for p in seg)
            max_y = max(p[1] for seg in shape for p in seg)
            if min_x <= lx <= max_x and min_y <= ly <= max_y:
                return d, block
        return self.max_depth, 0

    def render(self):
        half_fov = self.fov / 2
        angle_step = self.fov / self.num_rays

        for ray in range(self.num_rays):
            angle = self.player.angle - half_fov + ray * angle_step
            dist, block = self.cast_ray(angle)
            dist *= math.cos(angle - self.player.angle)
            height = min(int(self.height / (dist + 0.0001)), self.height)

            color_map = {
                1: (180, 60, 60),
                2: (100, 180, 100),
            }
            color = color_map.get(block, (80, 80, 80))
            shade = max(0.15, 1 - (dist / self.max_depth)**1.5)
            lit_color = tuple(int(c * shade) for c in color)

            x = int(ray * (self.width / self.num_rays))
            pygame.draw.line(
                self.screen,
                lit_color,
                (x, (self.height - height) // 2),
                (x, (self.height + height) // 2),
                max(1, int(self.width / self.num_rays))
            )
