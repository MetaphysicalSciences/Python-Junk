import pygame
import sys
import random
import time
import math

def run(screen, font):
    sw, sh = screen.get_size()
    clock = pygame.time.Clock()

    GREEN = (0, 255, 0)
    BG = (0, 0, 0)
    SCANLINE = (0, 40, 0)

    player = pygame.Rect(sw // 2 - 25, sh - 60, 50, 20)
    player_speed = 6
    bullets = []
    bullet_speed = -12
    shoot_cooldown = 350
    last_shot = 0

    current_wave = 1
    max_waves = 5
    enemies = []
    enemy_dx = 1
    enemy_dy = 10
    enemy_direction = 1
    enemy_move_down_next = False
    enemy_move_timer = 0
    enemy_move_delay = 200
    score = 0

    boss = None
    boss_health = 300
    boss_phase = 1
    boss_timer = 0
    boss_attacks = []
    boss_attack_cooldown = 2000
    boss_last_attack = 0
    boss_anim_offset = 0

    def create_wave(wave):
        enemies.clear()
        cols = min(10, 5 + wave // 2)
        rows = min(5, 2 + wave // 3)
        spacing_x = 50
        spacing_y = 40
        start_x = (sw - (cols - 1) * spacing_x) // 2
        start_y = 60
        for row in range(rows):
            for col in range(cols):
                enemies.append(pygame.Rect(start_x + col * spacing_x, start_y + row * spacing_y, 40, 30))

    def draw_scanlines():
        for y in range(0, sh, 4):
            pygame.draw.line(screen, SCANLINE, (0, y), (sw, y), 1)

    def draw_text(text, x, y):
        screen.blit(font.render(text, True, GREEN), (x, y))

    def spawn_boss():
        return pygame.Rect(sw // 2 - 100, 80, 200, 80)

    def draw_boss_bar(hp):
        w = 300
        h = 20
        x = sw // 2 - w // 2
        y = 20
        pygame.draw.rect(screen, (0, 100, 0), (x, y, w, h))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, int(w * (hp / 300)), h))

    def boss_attack(boss_rect):
        attacks = []
        phase = boss_phase
        now = pygame.time.get_ticks()
        if phase == 1:
            for _ in range(8):
                attacks.append(pygame.Rect(random.randint(0, sw), boss_rect.bottom, 5, 15))
        elif phase == 2:
            x = boss_rect.centerx
            attacks.append(pygame.Rect(x - 3, boss_rect.bottom, 6, sh))
        elif phase == 3:
            missile = pygame.Rect(boss_rect.centerx, boss_rect.bottom, 8, 20)
            missile.dx = random.choice([-4, 4])
            attacks.append(missile)
        else:
            orb = pygame.Rect(boss_rect.centerx - 12, boss_rect.bottom, 24, 24)
            attacks.append(orb)
        return attacks

    create_wave(current_wave)

    running = True
    enemy_move_timer = pygame.time.get_ticks()

    while running:
        screen.fill(BG)
        draw_scanlines()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < sw:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - last_shot > shoot_cooldown:
                last_shot = now
                bullets.append(pygame.Rect(player.centerx - 3, player.y, 6, 14))

        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        if current_wave < max_waves:
            now = pygame.time.get_ticks()
            if now - enemy_move_timer > enemy_move_delay:
                edge_hit = False
                for enemy in enemies:
                    enemy.x += enemy_dx * enemy_direction
                    if enemy.right >= sw - 10 or enemy.left <= 10:
                        edge_hit = True
                if edge_hit:
                    enemy_direction *= -1
                    for enemy in enemies:
                        enemy.y += enemy_dy
                enemy_move_timer = now

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.colliderect(enemy):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 10
                        break

            if not enemies:
                current_wave += 1
                if current_wave < max_waves:
                    create_wave(current_wave)
                    enemy_dx = 1 + current_wave * 0.2
                    enemy_move_delay = max(200, 600 - current_wave * 30)
                    enemy_direction = 1
                else:
                    boss = spawn_boss()
                    boss_health = 300
                    boss_phase = 1
                    boss_last_attack = pygame.time.get_ticks()

        else:
            if boss:
                boss_anim_offset += 0.05
                boss.y = 80 + int(10 * math.sin(boss_anim_offset))
                now = pygame.time.get_ticks()
                if boss_health <= 200 and boss_phase == 1:
                    boss_phase = 2
                    shoot_cooldown = 300
                    enemy_move_delay = 300
                if boss_health <= 100 and boss_phase == 2:
                    boss_phase = 3
                    shoot_cooldown = 200
                    enemy_move_delay = 150
                if boss_health <= 50 and boss_phase == 3:
                    boss_phase = 4
                    shoot_cooldown = 150
                    enemy_move_delay = 100

                if now - boss_last_attack > boss_attack_cooldown - (boss_phase * 300):
                    boss_attacks.extend(boss_attack(boss))
                    boss_last_attack = now

                for atk in boss_attacks[:]:
                    if hasattr(atk, 'dx'):
                        atk.x += atk.dx
                    atk.y += 5 + boss_phase
                    if atk.colliderect(player):
                        running = False
                    if atk.y > sh:
                        boss_attacks.remove(atk)

                for bullet in bullets[:]:
                    if bullet.colliderect(boss):
                        bullets.remove(bullet)
                        boss_health -= 5
                        score += 5

                pygame.draw.rect(screen, GREEN, boss)
                draw_boss_bar(boss_health)

                for atk in boss_attacks:
                    pygame.draw.rect(screen, (0, 255, 255), atk)

                if boss_health <= 0:
                    draw_text(f"BOSS DEFEATED! FINAL SCORE: {score}", sw // 2 - 180, sh // 2)
                    pygame.display.flip()
                    time.sleep(4)
                    return

        pygame.draw.rect(screen, GREEN, player)
        for bullet in bullets:
            pygame.draw.rect(screen, GREEN, bullet)
        if current_wave < max_waves:
            for enemy in enemies:
                pygame.draw.rect(screen, GREEN, enemy)

        draw_text(f"Wave: {current_wave}/{max_waves}", 10, 10)
        draw_text(f"Score: {score}", 10, 30)

        if any(e.bottom >= player.top for e in enemies):
            draw_text("YOU LOSE - Press ESC to return", sw // 2 - 200, sh // 2)
            pygame.display.flip()
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        return

        pygame.display.flip()
        clock.tick(60)
