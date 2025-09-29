import pygame
import random
import sys
import math

intro = input("Would you like to play full screen? Y/N")
if intro == "y" or intro == "Y" or intro == "yes" or intro == "Yes":
    W = 1920
    H = 1080
else:
    W = 800
    H = 600

pygame.init()

# Screen setup
WIDTH, HEIGHT = W, H
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FPS Trainer")

# Colors
WHITE = (255, 255, 255)
RED   = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE  = (50, 100, 220)
GRAY  = (30, 30, 30)
BROWN = (139, 69, 19)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Mouse grab (lock to center)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Camera
cam_x, cam_y = 0, 0
yaw = 0.0
pitch = 0.0
sensitivity = 0.002
projection_scale = 300

# Gun settings
gun_length = 120
gun_width_back = 70   # wide near end
gun_width_front = 25  # narrow muzzle end
gun_height = 10
gun_color = (90, 90, 90)
side_depthx = 72
side_depthy = 48

recoil_offset = -12   # pixels up when firing
recoil_time = 120     # ms
flash_time = 70       # ms
recoil = False
flash = False

# "warp" amount toward screen center
warp_offset = 150  # horizontal shift of muzzle toward center

# State
last_shot_time = 0
recoiling = False

def draw_gun(surface, x, y, recoil=False, flash=False):
    offset_y = recoil_offset if recoil else 0

    # Back (player side) trapezoid
    back_left = (x - gun_width_back // 2, y - gun_height + offset_y)
    back_right = (x + gun_width_back // 2, y - gun_height + offset_y)

    # Front (muzzle side), warped inward by warp_offset
    front_left = (x - gun_width_front // 2 - warp_offset, y - gun_length + offset_y)
    front_right = (x + gun_width_front // 2 - warp_offset, y - gun_length + offset_y)

    # Top face (trapezoid)
    barrel_points = [back_left, back_right, front_right, front_left]
    pygame.draw.polygon(surface, gun_color, barrel_points)

    # Side face points
    side_back_left = (back_left[0], back_left[1] + side_depthx)
    side_front_left = (front_left[0], front_left[1] + side_depthy)
    side_back_right = (back_right[0], back_right[1] + side_depthx)
    side_front_right = (front_right[0], front_right[1] + side_depthx)

    # --- Hidden muzzle flashes (draw BEFORE gun body) ---
    if flash:
        flash_color = (255, 240, 120)

        # Right muzzle flash (stick out to the right)
        right_muzzle_x = (front_right[0] + side_front_right[0]) // 2
        right_muzzle_y = (front_left[1] + side_front_left[1]) // 2
        right_flash = [
            (right_muzzle_x + 37, right_muzzle_y),   # tip outward
            (right_muzzle_x, right_muzzle_y - 30),
            (right_muzzle_x, right_muzzle_y + 30),
        ]
        pygame.draw.polygon(surface, flash_color, right_flash)

        # Bottom muzzle flash (stick down)
        bottom_muzzle_x = (side_front_left[0] + side_front_right[0]) // 2
        bottom_muzzle_y = (side_front_left[1] + side_front_right[1]) // 2 - 10
        bottom_flash = [
            (bottom_muzzle_x, bottom_muzzle_y + 35),  # tip downward
            (bottom_muzzle_x - 15, bottom_muzzle_y),
            (bottom_muzzle_x + 15, bottom_muzzle_y),
        ]
        pygame.draw.polygon(surface, flash_color, bottom_flash)

    # --- Gun body (draws OVER hidden flashes) ---
    # Top trapezoid
    
    # Left side
    pygame.draw.polygon(surface, (70, 70, 70), [back_left, front_left, side_front_left, side_back_left])
    # Right side
    pygame.draw.polygon(surface, (70, 70, 70), [back_right, front_right, side_front_right, side_back_right])
    # Back face
    pygame.draw.polygon(surface, (60, 60, 60), [back_left, back_right, side_back_right, side_back_left])
    pygame.draw.polygon(surface, gun_color, [back_left, back_right, front_right, front_left])
    # --- Visible flashes (draw AFTER gun body) ---
    if flash:
        flash_color = (255, 240, 120)

        # Front muzzle flash
        muzzle_x = (front_left[0] + front_right[0]) // 2
        muzzle_y = front_left[1]
        front_flash = [
            (muzzle_x, muzzle_y - 35),
            (muzzle_x - 15, muzzle_y),
            (muzzle_x + 15, muzzle_y),
        ]
        pygame.draw.polygon(surface, flash_color, front_flash)

        # Left muzzle flash
        side_muzzle_x = (front_left[0] + side_front_left[0]) // 2
        side_muzzle_y = (front_left[1] + side_front_left[1]) // 2
        side_flash = [
            (side_muzzle_x - 35, side_muzzle_y),
            (side_muzzle_x, side_muzzle_y - 30),
            (side_muzzle_x, side_muzzle_y + 30),
        ]
        pygame.draw.polygon(surface, flash_color, side_flash)


# -------- Projection helper ----------
def project_point(x, y, z, yaw, pitch):
    xz = x - cam_x
    zz = z
    x_rot = xz * math.cos(yaw) - zz * math.sin(yaw)
    z_rot = xz * math.sin(yaw) + zz * math.cos(yaw)

    y_rot = (y - cam_y) * math.cos(pitch) - z_rot * math.sin(pitch)
    z_final = (y - cam_y) * math.sin(pitch) + z_rot * math.cos(pitch)

    if z_final <= 1:
        return None

    screen_x = WIDTH//2 + int((x_rot / z_final) * projection_scale)
    screen_y = HEIGHT//2 + int((y_rot / z_final) * projection_scale)
    return screen_x, screen_y, z_final

# --------- Target Class ----------
class Target:
    def __init__(self):
        self.base_radius = random.randint(20, 40)
        self.x = random.randint(-200, 200)
        self.y = 0
        self.z = random.randint(300, 800)
        self.speed = random.choice([-2, 2])

    def update(self):
        self.x += self.speed
        if self.x > 300 or self.x < -300:
            self.speed *= -1

    def draw(self, surface, yaw, pitch):
        proj = project_point(self.x, self.y, self.z, yaw, pitch)
        if proj:
            sx, sy, z = proj
            scale = projection_scale / z
            radius = max(5, int(self.base_radius * scale))
            pygame.draw.circle(surface, RED, (sx, sy), radius)
            pygame.draw.circle(surface, WHITE, (sx, sy), radius // 2)
            pygame.draw.circle(surface, RED, (sx, sy), radius // 4)

    def is_hit(self, yaw, pitch):
        proj = project_point(self.x, self.y, self.z, yaw, pitch)
        if not proj:
            return False
        sx, sy, z = proj
        scale = projection_scale / z
        radius = max(5, int(self.base_radius * scale))
        dx = sx - WIDTH//2
        dy = sy - HEIGHT//2
        return dx*dx + dy*dy <= radius*radius

# --------- Fence Posts ----------
def draw_fence(surface, yaw, pitch):
    for side in [-1, 1]:
        for z in range(200, 2000, 200):
            x = side * 300
            y = 100
            proj = project_point(x, y, z, yaw, pitch)
            if proj:
                sx, sy, zf = proj
                scale = projection_scale / zf
                post_h = int(200 * scale)
                post_w = int(40 * scale)
                if post_h > 2:
                    pygame.draw.rect(surface, BROWN,
                        (sx - post_w//2, sy - post_h, post_w, post_h))

# --------- Crosshair ----------
def draw_crosshair(surface):
    cx, cy = WIDTH//2, HEIGHT//2
    size = 20
    thickness = 2
    pygame.draw.line(surface, WHITE, (cx - size, cy), (cx + size, cy), thickness)
    pygame.draw.line(surface, WHITE, (cx, cy - size), (cx, cy + size), thickness)
    pygame.draw.circle(surface, WHITE, (cx, cy), 8, 1)

# --------- Menu ----------
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_QUIT = "quit"

game_state = STATE_MENU
selected_mode = 0
modes = ["Timed 15s", "Reaction (10 targets)"]
high_scores = {modes[0]: 0, modes[1]: None}  # best score or avg reaction

# --------- Game variables ----------
score = 0
targets = []
start_time = 0

reaction_target = None
reaction_start = 0
reaction_times = []
shots_taken = 0
waiting_for_next = False
next_target_time = 0
last_reaction_display = None  # holds frozen reaction time until next spawn

def draw_menu():
    screen.fill((20, 20, 20))
    font = pygame.font.SysFont(None, 60)
    title = font.render("FPS Trainer", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    font = pygame.font.SysFont(None, 40)
    for i, mode in enumerate(modes):
        color = GREEN if i == selected_mode else WHITE
        hs = high_scores[mode]
        if mode == "Timed 15s":
            hs_text = f" | Best: {hs}" if hs else ""
        else:
            hs_text = f" | Best: {hs:.2f}s" if isinstance(hs, float) else ""
        text = font.render(mode + hs_text, True, color)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 250 + i*60))

    subfont = pygame.font.SysFont(None, 28)
    hint = subfont.render("UP/DOWN to select • ENTER to start • ESC to quit", True, WHITE)
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 80))

# --------- Main Loop ----------
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_mode = (selected_mode - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    selected_mode = (selected_mode + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    game_state = STATE_PLAYING
                    score = 0
                    targets = [Target() for _ in range(5)]
                    start_time = pygame.time.get_ticks()
                    reaction_target = None
                    reaction_times = []
                    shots_taken = 0
                    waiting_for_next = False
                    last_reaction_display = None
                elif event.key == pygame.K_ESCAPE:
                    game_state = STATE_QUIT

        elif game_state == STATE_PLAYING:

            now = pygame.time.get_ticks()
            recoil = False
            flash = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if modes[selected_mode] == "Timed 15s":
                    last_shot_time = now
                    recoiling = True
                    for t in targets[:]:
                        if t.is_hit(yaw, pitch):
                            score += 1
                            targets.remove(t)
                            targets.append(Target())
                else:  # Reaction mode
                    last_shot_time = now
                    recoiling = True
                    if reaction_target and reaction_target.is_hit(yaw, pitch):
                        shots_taken += 1
                        reaction_time = (pygame.time.get_ticks() - reaction_start) / 1000
                        reaction_times.append(reaction_time)
                        last_reaction_display = reaction_time
                        reaction_target = None
                        waiting_for_next = True
                        next_target_time = pygame.time.get_ticks() + random.randint(1000, 4000)

    # --------- Draw per state ---------
    if game_state == STATE_MENU:
        draw_menu()

    elif game_state == STATE_PLAYING:
        # Mouse look
        rel_x, rel_y = pygame.mouse.get_rel()
        yaw += rel_x * sensitivity
        pitch -= -rel_y * sensitivity
        pitch = max(-math.pi/3, min(math.pi/3, pitch))

        # Background
        horizon = HEIGHT//2 + int(pitch * projection_scale)
        screen.fill(GRAY)
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, horizon))
        pygame.draw.rect(screen, GRAY, (0, horizon, WIDTH, HEIGHT-horizon))

        draw_fence(screen, yaw, pitch)


        if recoiling:
            if now - last_shot_time < recoil_time:
                recoil = True
            if now - last_shot_time < flash_time:
                flash = True
            if now - last_shot_time >= recoil_time:
                recoiling = False

        # Draw gun anchored near bottom-right
        draw_gun(screen, WIDTH - 10, HEIGHT - 20, recoil=recoil, flash=flash)

        if modes[selected_mode] == "Timed 15s":
            # Update and draw
            for t in targets:
                t.update()
                t.draw(screen, yaw, pitch)

            draw_crosshair(screen)

            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            remaining = max(0, 15 - int(elapsed))
            if remaining <= 0:
                # update high score
                if score > high_scores[modes[0]]:
                    high_scores[modes[0]] = score
                game_state = STATE_MENU

            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            timer_text = font.render(f"Time: {remaining}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(timer_text, (WIDTH - 150, 10))

        elif modes[selected_mode] == "Reaction (10 targets)":
            # Handle spawning delay
            if not reaction_target and not waiting_for_next and shots_taken < 10:
                reaction_target = Target()
                reaction_start = pygame.time.get_ticks()
                last_reaction_display = None
            elif waiting_for_next and pygame.time.get_ticks() >= next_target_time:
                waiting_for_next = False

            # Draw current target
            if reaction_target:
                reaction_target.draw(screen, yaw, pitch)

            draw_crosshair(screen)

            font = pygame.font.SysFont(None, 36)
            shots_text = font.render(f"Shots: {shots_taken}/10", True, WHITE)
            screen.blit(shots_text, (10, 10))

            # Show live/frozen reaction timer
            if reaction_target:
                live_time = (pygame.time.get_ticks() - reaction_start) / 1000
                timer_text = font.render(f"{live_time:.2f}s", True, WHITE)
                screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 20))
            elif last_reaction_display is not None:
                timer_text = font.render(f"{last_reaction_display:.2f}s", True, WHITE)
                screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 20))

            # Show running average (top-right)
            if reaction_times:
                avg_time = sum(reaction_times) / len(reaction_times)
                avg_text = font.render(f"Avg: {avg_time:.2f}s", True, WHITE)
                screen.blit(avg_text, (WIDTH - avg_text.get_width() - 10, 10))

            # End after 10
            if shots_taken >= 10:
                avg_time = sum(reaction_times) / len(reaction_times)
                if high_scores[modes[1]] is None or avg_time < high_scores[modes[1]]:
                    high_scores[modes[1]] = avg_time
                game_state = STATE_MENU

    elif game_state == STATE_QUIT:
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
