import pygame
import math
import sys
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense with Path Blocking & Rewards")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (240, 240, 0)
GRAY = (80, 80, 80)

# Game settings
FPS = 60
ENEMY_SIZE = 20
BASE_ENEMY_SPEED = 1.2
BULLET_SPEED = 6

# Tower costs
TOWER_COSTS = {
    "basic": 50,
    "sniper": 120,
    "aoe": 80
}

# Path
PATH = [
    (50, 100),
    (200, 100),
    (200, 250),
    (600, 250),
    (600, 400),
    (300, 400),
    (300, 500),
    (750, 500),
]

class Enemy:
    def __init__(self, hp, speed, reward=10, color=RED):
        self.x, self.y = PATH[0]
        self.hp = hp
        self.speed = speed
        self.reward = reward
        self.waypoint = 1
        self.finished = False
        self.color = color

    def move(self):
        if self.waypoint < len(PATH):
            tx, ty = PATH[self.waypoint]
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx, dy = dx / dist, dy / dist
                self.x += dx * self.speed
                self.y += dy * self.speed
            if dist < 2:
                self.waypoint += 1
        if self.waypoint >= len(PATH):
            self.finished = True

    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x - ENEMY_SIZE//2, self.y - ENEMY_SIZE//2, ENEMY_SIZE, ENEMY_SIZE))

    def is_alive(self):
        return self.hp > 0 and not self.finished

class SplitterEnemy(Enemy):
    def __init__(self, hp, speed, splits_into=2, generation=1):
        super().__init__(hp, speed, reward=5, color=YELLOW)
        self.splits_into = splits_into
        self.generation = generation

    def on_death(self):
        children = []
        if self.generation > 0:
            for _ in range(self.splits_into):
                child = SplitterEnemy(
                    max(1, self.hp // 2),
                    self.speed + 0.2,
                    splits_into=self.splits_into,
                    generation=self.generation - 1
                )
                child.x = self.x + random.randint(-12, 12)
                child.y = self.y + random.randint(-12, 12)
                child.waypoint = self.waypoint
                children.append(child)
        return children

class TankEnemy(Enemy):
    def __init__(self, hp, speed):
        super().__init__(hp, speed, reward=20, color=GRAY)

    def draw(self):
        pygame.draw.circle(WIN, self.color, (int(self.x), int(self.y)), ENEMY_SIZE // 2 + 12)

class Tower:
    def __init__(self, x, y, tower_type="basic"):
        self.x, self.y = x, y
        self.cooldown = 0
        self.type = tower_type
        if tower_type == "basic":
            self.range = 120
            self.fire_rate = 25
            self.damage = 1
        elif tower_type == "sniper":
            self.range = 250
            self.fire_rate = 60
            self.damage = 4
        elif tower_type == "aoe":
            self.range = 90
            self.fire_rate = 15
            self.damage = 1

    def draw(self):
        color = BLUE if self.type == "basic" else (0, 0, 0) if self.type == "sniper" else (0, 200, 200)
        pygame.draw.circle(WIN, color, (self.x, self.y), 20)
        pygame.draw.circle(WIN, (150,150,150), (self.x, self.y), self.range, 1)

    def shoot(self, enemies, bullets):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        if self.type == "aoe":
            hit = False
            for enemy in enemies:
                dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if dist <= self.range and enemy.is_alive():
                    enemy.hp -= self.damage
                    hit = True
            if hit:
                self.cooldown = self.fire_rate
        else:
            for enemy in enemies:
                dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if dist <= self.range and enemy.is_alive():
                    bullets.append(Bullet(self.x, self.y, enemy, damage=self.damage))
                    self.cooldown = self.fire_rate
                    break

class Bullet:
    def __init__(self, x, y, target, damage=1):
        self.x, self.y = x, y
        self.target = target
        self.damage = damage

    def move(self):
        if not self.target.is_alive():
            return False
        dx, dy = self.target.x - self.x, self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist < 8:
            self.target.hp -= self.damage
            return False
        dx, dy = dx / dist, dy / dist
        self.x += dx * BULLET_SPEED
        self.y += dy * BULLET_SPEED
        return True

    def draw(self):
        pygame.draw.circle(WIN, BLACK, (int(self.x), int(self.y)), 4)

def draw_path():
    pygame.draw.lines(WIN, GREEN, False, PATH, 5)

def point_to_segment_dist(px, py, x1, y1, x2, y2):
    """distance from point (px,py) to segment (x1,y1)-(x2,y2)"""
    line_mag = math.hypot(x2 - x1, y2 - y1)
    if line_mag == 0:
        return math.hypot(px - x1, py - y1)
    u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
    u = max(0, min(1, u))
    ix, iy = x1 + u * (x2 - x1), y1 + u * (y2 - y1)
    return math.hypot(px - ix, py - iy)

def valid_tower_position(x, y, towers):
    # Prevent overlap with path
    for i in range(len(PATH) - 1):
        if point_to_segment_dist(x, y, PATH[i][0], PATH[i][1], PATH[i+1][0], PATH[i+1][1]) < 40:
            return False
    # Prevent overlap with other towers
    for tower in towers:
        if math.hypot(x - tower.x, y - tower.y) < 40:
            return False
    return True

def main():
    clock = pygame.time.Clock()
    enemies = []
    towers = []
    bullets = []

    lives = 10
    money = 200
    wave = 1
    enemies_to_spawn = 0
    spawn_timer = 0
    in_wave = False
    wave_cooldown = 180  # 3 seconds

    selected_tower_type = "basic"
    font = pygame.font.SysFont(None, 28)

    while True:
        clock.tick(FPS)
        WIN.fill(WHITE)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: selected_tower_type = "basic"
                if event.key == pygame.K_2: selected_tower_type = "sniper"
                if event.key == pygame.K_3: selected_tower_type = "aoe"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                cost = TOWER_COSTS[selected_tower_type]
                if money >= cost and valid_tower_position(mx, my, towers):
                    towers.append(Tower(mx, my, selected_tower_type))
                    money -= cost

        # Wave handling
        if not in_wave:
            wave_cooldown -= 1
            if wave_cooldown <= 0:
                in_wave = True
                enemies_to_spawn = 5 + wave * 2
                spawn_timer = 0

        if in_wave and enemies_to_spawn > 0:
            spawn_timer += 1
            if spawn_timer > 40:
                spawn_timer = 0
                if wave % 5 == 0:
                    enemies.append(TankEnemy(60 + wave * 10, BASE_ENEMY_SPEED * 0.6))
                elif wave % 3 == 0:
                    enemies.append(SplitterEnemy(8 + wave, BASE_ENEMY_SPEED + 0.2, splits_into=2, generation=2))
                else:
                    enemies.append(Enemy(3 + wave // 2, BASE_ENEMY_SPEED + wave*0.05))
                enemies_to_spawn -= 1

        # Update enemies
        for enemy in enemies[:]:
            enemy.move()
            if enemy.finished:
                enemies.remove(enemy)
                lives -= 1
            elif enemy.hp <= 0:
                children = []
                if isinstance(enemy, SplitterEnemy):
                    children = enemy.on_death()
                enemies.remove(enemy)
                enemies.extend(children)
                money += enemy.reward

        # End wave check
        if in_wave and enemies_to_spawn == 0 and not enemies:
            in_wave = False
            wave += 1
            wave_cooldown = 180

        # Towers shoot
        for tower in towers:
            tower.shoot(enemies, bullets)

        # Bullets
        new_bullets = []
        for bullet in bullets:
            if bullet.move():
                new_bullets.append(bullet)
        bullets = new_bullets

        # Draw path, enemies, towers, bullets
        draw_path()
        for enemy in enemies: enemy.draw()
        for tower in towers: tower.draw()
        for bullet in bullets: bullet.draw()

        # Tower preview + price
        mx, my = pygame.mouse.get_pos()
        cost = TOWER_COSTS[selected_tower_type]
        valid = valid_tower_position(mx, my, towers)
        preview_color = (0, 255, 0) if money >= cost and valid else (255, 0, 0)
        pygame.draw.circle(WIN, preview_color, (mx, my), 20, 2)
        price_text = font.render(f"${cost}", True, BLACK)
        WIN.blit(price_text, (mx + 15, my - 25))

        # HUD
        hud_text = font.render(f"Lives: {lives}  Money: {money}  Wave: {wave}", True, BLACK)
        WIN.blit(hud_text, (10, 10))

        # Wave timer display
        if not in_wave:
            countdown = max(0, wave_cooldown // FPS)
            timer_text = font.render(f"Next wave in: {countdown}", True, RED)
            WIN.blit(timer_text, (WIDTH//2 - 80, 50))

        if lives <= 0:
            go_text = font.render("GAME OVER! Press ESC to quit.", True, RED)
            WIN.blit(go_text, (WIDTH//2 - 150, HEIGHT//2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            continue

        pygame.display.update()

if __name__ == "__main__":
    main()
