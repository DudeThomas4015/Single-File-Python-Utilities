import pygame
import sys
import random
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
GRAY = (120, 120, 120)
ORANGE = (255, 140, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 18)

# Player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = 15
player_speed = 5
max_health = 100
player_health = max_health
score = 0

#Prices
shotgun_cost = 240
smg_cost = 100
lmg_cost = 300
damage_cost = 50
fireRate_cost = 40
magsize_cost = 25
health_cost = 75
speed_cost = 25

# Melee
melee_range = 80          # how far the slash reaches
melee_damage = 500         # light damage
melee_knockback = 40      # how far zombies get pushed
melee_cooldown = 2400      # ms between slashes
last_melee = 0            # time tracker
melee_active = False
slashes = []  # each slash: {"x","y","angle","timer"}
slash_duration = 150  # ms visible


# Global upgrade multipliers (apply to all weapons)
damage_mult = 1.0           # multiplies base damage
firerate_mult = 1.0         # multiplies base fire_rate (lower = faster)
mag_mult = 1.0              # multiplies base mag size

# Weapons definitions (store base stats). We'll keep per-weapon runtime fields: 'mag' and 'reserve' and 'owned'
weapon_keys = ["pistol", "shotgun", "smg", "lmg", "sniper"]
weapons = {
    "pistol":  {"base_damage": 20, "base_fire_rate": 300, "base_mag": 10, "cost": 0,  "mag": 10,  "reserve": float("inf"), "owned": True},
    "shotgun": {"base_damage": 60, "base_fire_rate": 800, "base_mag": 5,  "cost": shotgun_cost, "mag": 0,   "reserve": 0, "owned": False},
    "smg":     {"base_damage": 12, "base_fire_rate": 100, "base_mag": 25, "cost": smg_cost, "mag": 0, "reserve": 0, "owned": False},
    "lmg":     {"base_damage": 25, "base_fire_rate": 200, "base_mag": 50, "cost": lmg_cost, "mag": 0, "reserve": 0, "owned": False},
    "sniper":  {"base_damage": 200,"base_fire_rate": 1200,"base_mag": 3,  "cost": 350, "mag": 0, "reserve": 0, "owned": False}
}
# current weapon index into weapon_keys
current_weapon_index = 0  # pistol by default

def get_current_weapon_key():
    return weapon_keys[current_weapon_index]

def get_effective_damage(key):
    return int(weapons[key]["base_damage"] * damage_mult)

def get_effective_fire_rate(key):
    # smaller is faster; firerate_mult defaults to 1.0; you can reduce it to speed up
    return max(20, int(weapons[key]["base_fire_rate"] * firerate_mult))

def get_effective_mag_size(key):
    return max(1, int(round(weapons[key]["base_mag"] * mag_mult)))

# Shooting
bullets = []
bullet_speed = 12
bullet_radius = 5
last_shot = 0
reloading = False
last_reload = 0
reload_time = 1200  # ms

# Grenade system
grenades = []  # each: {"x","y","dx","dy","timer"}
grenade_radius = 6
grenade_speed = 8
grenade_timer = 700   # ms until explode
grenade_base_damage = 80
grenade_explosion_radius = 80
player_grenades = 2
max_grenades = 4
last_grenade = 0
grenade_cooldown = 300  # ms between throws

# Zombies
zombies = []
zombie_size = 28

# Powerups & shop
powerups = []         # [x, y, type] type in {"ammo","health"}
POWERUP_SIZE = 20
shop_items = []       # [x, y, type]
SHOP_ITEM_SIZE = 36

# Upgrade price lookup (upgrades apply to all weapons)
upgrade_costs = {"Damage": damage_cost, "Fire Rate": fireRate_cost, "Mag Size": magsize_cost, "Health": health_cost, "Speed": speed_cost}

# Waves
wave = 1
zombies_remaining = 5
wave_in_progress = True
in_store = False
zombies_to_spawn = 5
spawn_interval = 900   # ms between spawns in a wave
last_spawn_time = 0

# Zombie type unlock flags
runner_unlocked = False
tank_unlocked = False

# Shop feedback
shop_message = ""
shop_message_time = 0
shop_message_duration = 1400  # ms for red message

# Helper: pick next owned weapon index when scrolling
def cycle_weapon_index(delta):
    global current_weapon_index
    owned_indices = [i for i, k in enumerate(weapon_keys) if weapons[k]["owned"]]
    if not owned_indices:
        return
    if current_weapon_index not in owned_indices:
        current_weapon_index = owned_indices[0]
        return
    idx = owned_indices.index(current_weapon_index)
    idx = (idx + delta) % len(owned_indices)
    current_weapon_index = owned_indices[idx]

# Spawning zombies
def spawn_zombie():
    """Spawn one zombie at random edge. Chooses type depending on unlocks."""
    z_type = "normal"
    if tank_unlocked and random.random() < 0.12:
        z_type = "tank"
    elif runner_unlocked and random.random() < 0.28:
        z_type = "runner"

    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x, y = random.randint(0, WIDTH), -zombie_size
    elif side == "bottom":
        x, y = random.randint(0, WIDTH), HEIGHT + zombie_size
    elif side == "left":
        x, y = -zombie_size, random.randint(0, HEIGHT)
    else:
        x, y = WIDTH + zombie_size, random.randint(0, HEIGHT)

    if z_type == "normal":
        base_hp = 20 + (wave - 1) * 6
        health = base_hp
        speed = 1.5 + (wave - 1) * 0.18
    elif z_type == "runner":
        base_hp = 15 + (wave - 1) * 4
        health = base_hp
        speed = 3.5 + (wave - 1) * 0.25
    else:  # tank
        base_hp = 120 + (wave - 1) * 12
        health = base_hp
        speed = 0.8 + (wave - 1) * 0.1

    zombies.append({
        "x": x,
        "y": y,
        "health": health,
        "max_health": health,
        "speed": speed,
        "type": z_type
    })

def move_zombies():
    # move toward player
    for z in zombies:
        dx = player_pos[0] - z["x"]
        dy = player_pos[1] - z["y"]
        dist = math.hypot(dx, dy)
        if dist != 0:
            z["x"] += z["speed"] * dx / dist
            z["y"] += z["speed"] * dy / dist

    # collision resolution between zombies (push apart)
    for i in range(len(zombies)):
        for j in range(i + 1, len(zombies)):
            z1, z2 = zombies[i], zombies[j]
            dx = z2["x"] - z1["x"]
            dy = z2["y"] - z1["y"]
            dist = math.hypot(dx, dy)
            min_dist = zombie_size
            if dist < min_dist and dist > 0:
                overlap = (min_dist - dist) / 2
                ux, uy = dx / dist, dy / dist
                z1["x"] -= ux * overlap
                z1["y"] -= uy * overlap
                z2["x"] += ux * overlap
                z2["y"] += uy * overlap

def move_bullets():
    for b in bullets[:]:
        b[0] += b[2] * bullet_speed
        b[1] += b[3] * bullet_speed
        if not (0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT):
            bullets.remove(b)

def check_collisions():
    global score, player_health, zombies_remaining, shop_message, shop_message_time

    # bullets vs zombies
    for b in bullets[:]:
        for z in zombies[:]:
            if math.hypot(b[0] - z["x"], b[1] - z["y"]) < (zombie_size / 2 + bullet_radius):
                pellet_damage = b[4]
                z["health"] -= pellet_damage
                if z["health"] <= 0:
                    if z in zombies:
                        zombies.remove(z)
                    score += 10 if z["type"] == "normal" else (14 if z["type"] == "runner" else 35)
                    zombies_remaining -= 1
                    if random.random() < 0.18:
                        powerups.append([z["x"], z["y"], random.choice(["ammo", "health"])])

                # remove non-piercing bullets
                if not b[6]:  
                    if b in bullets:
                        bullets.remove(b)
                # piercing bullets keep going → continue to hit others
                break

    # grenade explosions handled elsewhere (they directly damage zombies on explode)

    # zombies vs player
    for z in zombies[:]:
        if math.hypot(player_pos[0] - z["x"], player_pos[1] - z["y"]) < (player_radius + zombie_size / 2):
            if z in zombies:
                zombies.remove(z)
            player_health -= 10
            zombies_remaining -= 1

    # powerups vs player
    for p in powerups[:]:
        if math.hypot(player_pos[0] - p[0], player_pos[1] - p[1]) < (player_radius + POWERUP_SIZE / 2):
            if p[2] == "ammo":
                # ammo pickup: refill current weapon/mag or add reserves and also refill one grenade
                handle_ammo_pickup()
                # refill one grenade up to max
                global player_grenades
                player_grenades = min(max_grenades, player_grenades + 1)
            elif p[2] == "health":
                player_health = min(max_health, player_health + 35)
            powerups.remove(p)

    # shop collisions if in_store
    if in_store:
        for item in shop_items[:]:
            if math.hypot(player_pos[0] - item[0], player_pos[1] - item[1]) < (player_radius + SHOP_ITEM_SIZE / 2):
                kind = item[2]
                cost = upgrade_costs.get(kind, weapons.get(kind, {}).get("cost", 0))
                if score >= cost:
                    buy_item(kind)
                    shop_items.remove(item)
                else:
                    shop_message = "Not enough points!"
                    shop_message_time = pygame.time.get_ticks()

def shoot(mx, my, now):
    global last_shot
    key = get_current_weapon_key()
    gun = weapons[key]
    mag = gun["mag"]
    # can't shoot while reloading or without mag ammo
    if reloading or mag <= 0:
        return
    eff_fire = get_effective_fire_rate(key)
    if now - last_shot >= eff_fire:
        dx, dy = mx - player_pos[0], my - player_pos[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        base_angle = math.atan2(dy, dx)

        # --- SHOTGUN: spawn multiple pellets in a spread ---
        if key == "shotgun":
            pellets = 7                    # number of pellets
            spread_deg = 45                # total cone in degrees
            spread = math.radians(spread_deg)
            # total damage for a shell = effective damage; split across pellets
            total_dmg = get_effective_damage(key)
            # distribute damage roughly evenly
            pellet_dmg = max(1, total_dmg // pellets)
            # If there's remainder, add it to the central pellet
            remainder = total_dmg - pellet_dmg * pellets
            for i in range(pellets):
                # offset pellets across the cone [-spread/2 .. +spread/2]
                t = 0 if pellets == 1 else (i / (pellets - 1))  # 0..1
                offset = (t - 0.5) * spread
                angle = base_angle + offset
                pdx, pdy = math.cos(angle), math.sin(angle)
                dmg = pellet_dmg + (remainder if i == pellets // 2 else 0)
                bullets.append([player_pos[0], player_pos[1], pdx, pdy, dmg, key, False])
            # one shotgun shell consumes one magazine unit
            gun["mag"] -= 1
            last_shot = now
            return
        
                # --- SNIPER: piercing shot ---
        if key == "sniper":
            nx, ny = dx / dist, dy / dist
            bullet_dmg = get_effective_damage(key)
            # mark it as piercing
            bullets.append([player_pos[0], player_pos[1], nx, ny, bullet_dmg, key, True])  
            gun["mag"] -= 1
            last_shot = now
            return


        # --- Default: single projectile for other weapons ---
        nx, ny = dx / dist, dy / dist
        bullet_dmg = get_effective_damage(key)
        bullets.append([player_pos[0], player_pos[1], nx, ny, bullet_dmg, key, False])
        gun["mag"] -= 1
        last_shot = now


def start_reload(now):
    global reloading, last_reload
    key = get_current_weapon_key()
    gun = weapons[key]
    mag_size = get_effective_mag_size(key)
    if not reloading and gun["mag"] < mag_size:
        # check if there is reserve or infinite
        if gun["reserve"] > 0 or gun["reserve"] == float("inf"):
            reloading = True
            last_reload = now

def finish_reload(now):
    global reloading
    if not reloading:
        return
    key = get_current_weapon_key()
    gun = weapons[key]
    if now - last_reload >= reload_time:
        mag_size = get_effective_mag_size(key)
        needed = mag_size - gun["mag"]
        if needed <= 0:
            reloading = False
            return
        if gun["reserve"] == float("inf"):
            taken = needed
        else:
            taken = min(needed, gun["reserve"])
        gun["mag"] += taken
        if gun["reserve"] != float("inf"):
            gun["reserve"] -= taken
        reloading = False

def next_wave():
    global wave, zombies_remaining, wave_in_progress, in_store, zombies_to_spawn, runner_unlocked, tank_unlocked, player_grenades, max_grenades
    player_grenades = min(max_grenades, player_grenades + 1)
    wave += 1
    if wave % 5 == 0:
        in_store = True
        zombies.clear()
        zombies_remaining = 0
        spawn_shop_items()
        if wave >= 5:
            runner_unlocked = True
        if wave >= 10:
            tank_unlocked = True
    else:
        zombies_remaining = 5 + wave * 2
        zombies_to_spawn = zombies_remaining
        wave_in_progress = True

def spawn_shop_items():
    global shop_items
    shop_items = []
    cx, cy = WIDTH // 2, HEIGHT // 2
    spacing = 120

    # --- Weapons (top row) ---
    weapon_list = ["shotgun", "smg", "lmg", "sniper"]
    visible_weapons = [w for w in weapon_list if not weapons[w]["owned"]]

    for i, w in enumerate(visible_weapons):
        x = cx + (i - (len(visible_weapons) - 1) / 2) * spacing
        y = cy - 160   # top row
        shop_items.append([int(x), y, w])

    # --- Upgrades (bottom row) ---
    upgrade_list = ["Damage", "Fire Rate", "Mag Size", "Health", "Speed"]
    for i, u in enumerate(upgrade_list):
        x = cx + (i - (len(upgrade_list) - 1) / 2) * spacing
        y = cy + 160   # bottom row
        shop_items.append([int(x), y, u])


def buy_item(kind):
    """Buy upgrades or weapons. Weapons are one-time purchases; upgrades apply global multipliers."""
    global score, current_weapon_index, max_health, player_health, player_speed, damage_mult, firerate_mult, mag_mult
    if kind in upgrade_costs:
        cost = upgrade_costs[kind]
        if score < cost:
            return False
        score -= cost
        if kind == "Damage":
            damage_mult += 0.20   # +20% damage
        elif kind == "Fire Rate":
            firerate_mult *= 0.9  # 10% faster (fire_rate lower)
        elif kind == "Mag Size":
            mag_mult += 0.25      # +25% mag size
            # optionally increase current mags proportionally
            for k in weapon_keys:
                cur_mag = weapons[k]["mag"]
                new_mag_size = get_effective_mag_size(k)
                # boost current mag a bit (not exceed new cap)
                weapons[k]["mag"] = min(new_mag_size, cur_mag + int(round(new_mag_size * 0.25)))
        elif kind == "Health":
            max_health += 25
            player_health = max_health
        return True
    elif kind in weapons:
        # weapon purchase (one-time)
        cost = weapons[kind]["cost"]
        if score < cost:
            return False
        if weapons[kind]["owned"]:
            # already owned; do nothing (caller removes item)
            return True
        score -= cost
        weapons[kind]["owned"] = True
        # give starting ammo and set current weapon to it
        weapons[kind]["mag"] = get_effective_mag_size(kind)
        # give some reserve depending on weapon
        if kind == "shotgun":
            weapons[kind]["reserve"] += 30
        elif kind == "smg":
            weapons[kind]["reserve"] += 60
        elif kind == "lmg":
            weapons[kind]["reserve"] += 120
        elif kind == "sniper":
            weapons[kind]["reserve"] += 36
        # switch current weapon index to this weapon
        if kind in weapon_keys:
            current_weapon_index = weapon_keys.index(kind)
        return True
    return False

def handle_ammo_pickup():
    """Ammo pickup affects currently selected weapon, and also refills one grenade (handled by caller)."""
    key = get_current_weapon_key()
    gun = weapons[key]
    if key == "pistol":
        # refill pistol mag from infinite reserve
        gun["mag"] = get_effective_mag_size(key)
    else:
        # add reserves per rules
        if key == "shotgun":
            gun["reserve"] += gun["mag"] * 2
        elif key == "smg":
            gun["reserve"] += gun["mag"] * 2
        elif key == "lmg":
            gun["reserve"] += gun["mag"] * 2
        elif key == "sniper":
            gun["reserve"] += gun["mag"] * 2

def draw_ui():
    # Health bar
    health_bar_width = 220
    pygame.draw.rect(screen, GRAY, (10, 10, health_bar_width, 22))
    pygame.draw.rect(screen, RED, (10, 10, health_bar_width, 22))
    pygame.draw.rect(screen, GREEN, (10, 10, int(health_bar_width * player_health / max_health), 22))
    # Ammo text
    key = get_current_weapon_key()
    gun = weapons[key]
    mag_display = int(gun["mag"]) if gun["mag"] != float("inf") else "∞"
    res_display = "∞" if gun["reserve"] == float("inf") else int(gun["reserve"])
    screen.blit(font.render(f"Ammo: {mag_display}/{res_display}", True, WHITE), (10, 42))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 70))
    screen.blit(font.render(f"Wave: {wave}", True, WHITE), (10, 98))
    screen.blit(font.render(f"Weapon: {get_current_weapon_key().upper()}", True, YELLOW), (10, 126))
    screen.blit(font.render(f"Grenades: {player_grenades}/{max_grenades}", True, ORANGE), (10, 158))
    # multipliers display (optional)
    screen.blit(small_font.render(f"Dmg x{damage_mult:.2f}  FR x{firerate_mult:.2f}  Mag x{mag_mult:.2f}", True, WHITE), (10, 186))
    if reloading:
        screen.blit(font.render("Reloading...", True, YELLOW), (10, 210))
    # shop message (red)
    if shop_message and pygame.time.get_ticks() - shop_message_time < shop_message_duration:
        msg = font.render(shop_message, True, RED)
        screen.blit(msg, (player_pos[0] - msg.get_width() // 2, player_pos[1] - 40))

def draw_shop_items():
    for s in shop_items:
        item_x, item_y, kind = s
        color = YELLOW if kind in upgrade_costs else BLUE
        pygame.draw.rect(screen, color, (item_x - SHOP_ITEM_SIZE // 2, item_y - SHOP_ITEM_SIZE // 2, SHOP_ITEM_SIZE, SHOP_ITEM_SIZE))
        name_text = str(kind).upper()
        cost = upgrade_costs.get(kind, weapons.get(kind, {}).get("cost", 0))
        name_surf = small_font.render(name_text, True, WHITE)
        cost_surf = small_font.render(f"${cost}", True, WHITE)
        screen.blit(name_surf, (item_x - name_surf.get_width() // 2, item_y - SHOP_ITEM_SIZE // 2 - 18))
        screen.blit(cost_surf, (item_x - cost_surf.get_width() // 2, item_y + SHOP_ITEM_SIZE // 2 + 4))

# initialize wave spawning
zombies_to_spawn = zombies_remaining
last_spawn_time = pygame.time.get_ticks()

running = True
while running:
    screen.fill(BLACK)
    now = pygame.time.get_ticks()

    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # left click = shoot
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            shoot(mx, my, now)

        # right click = grenade throw
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if player_grenades > 0 and now - last_grenade >= grenade_cooldown:
                mx, my = pygame.mouse.get_pos()
                dx, dy = mx - player_pos[0], my - player_pos[1]
                dist = math.hypot(dx, dy)
                if dist != 0:
                    dx, dy = dx / dist, dy / dist
                    grenades.append({"x": player_pos[0], "y": player_pos[1], "dx": dx, "dy": dy, "vx": dx * grenade_speed, "vy": dy * grenade_speed, "timer": grenade_timer})
                    player_grenades -= 1
                    last_grenade = now

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if now - last_melee >= melee_cooldown:
                melee_active = True
                last_melee = now
                mx, my = pygame.mouse.get_pos()
                dx, dy = mx - player_pos[0], my - player_pos[1]
                slash_angle = math.atan2(dy, dx)
                slashes.append({"x": player_pos[0], "y": player_pos[1], "angle": slash_angle, "timer": slash_duration})



        # mouse wheel to switch weapons
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                cycle_weapon_index(1)
            elif event.y < 0:
                cycle_weapon_index(-1)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                start_reload(now)
            elif event.key == pygame.K_RETURN and in_store:
                # leave store and spawn next wave
                in_store = False
                zombies_remaining = 5 + wave * 2
                zombies_to_spawn = zombies_remaining
                last_spawn_time = now

    # hold shooting when left mouse is held
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        shoot(mx, my, now)

    # finish any reload
    finish_reload(now)

    # movement and clamp to screen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed

    player_pos[0] = max(player_radius, min(WIDTH - player_radius, player_pos[0]))
    player_pos[1] = max(player_radius, min(HEIGHT - player_radius, player_pos[1]))

    # spawn zombies gradually if not in store
    if not in_store:
        if zombies_to_spawn > 0 and now - last_spawn_time >= spawn_interval:
            spawn_zombie()
            zombies_to_spawn -= 1
            last_spawn_time = now
        move_zombies()
        move_bullets()
    
        # --- MELEE (directional cone slash) ---
    if melee_active:
        # Player -> mouse direction
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_pos[0], my - player_pos[1]
        slash_angle = math.atan2(dy, dx)  # radians

        cone_angle = math.radians(90)     # total width of cone
        half_cone = cone_angle / 2

        # Draw visual slash arc (approximate with line for now)
        end_x = player_pos[0] + math.cos(slash_angle) * melee_range
        end_y = player_pos[1] + math.sin(slash_angle) * melee_range

        # Damage & knockback any zombies in cone
        for z in zombies[:]:
            zx, zy = z["x"] - player_pos[0], z["y"] - player_pos[1]
            dist = math.hypot(zx, zy)
            if dist <= melee_range:
                angle_to_z = math.atan2(zy, zx)
                # smallest angular difference
                diff = (angle_to_z - slash_angle + math.pi) % (2 * math.pi) - math.pi
                if abs(diff) <= half_cone:
                    # In cone → hit
                    z["health"] -= melee_damage

                    # Knockback
                    d = math.hypot(zx, zy)
                    if d != 0:
                        nx, ny = zx / d, zy / d
                        z["x"] += nx * melee_knockback
                        z["y"] += ny * melee_knockback

                    # Kill/reward
                    if z["health"] <= 0:
                        if z in zombies:
                            zombies.remove(z)
                        score += 10 if z["type"] == "normal" else (14 if z["type"] == "runner" else 35)
                        zombies_remaining -= 1
                        if random.random() < 0.18:
                            powerups.append([z["x"], z["y"], random.choice(["ammo", "health"])])

        melee_active = False

        

        # --- Draw melee slashes (fade out arcs) ---
    for s in slashes[:]:
        # Fade alpha based on time left
        alpha = max(0, int(255 * (s["timer"] / slash_duration)))

        # Arc geometry
        start_angle = -s["angle"] - math.radians(22.5)
        end_angle   = -s["angle"] + math.radians(22.5)

        # Create surface with alpha
        arc_surface = pygame.Surface((melee_range*2, melee_range*2), pygame.SRCALPHA)
        pygame.draw.arc(
            arc_surface,
            (255, 80, 80, alpha),
            (0, 0, melee_range*2, melee_range*2),
            start_angle,
            end_angle,
            6
        )

        # Blit centered on player
        screen.blit(arc_surface, (s["x"] - melee_range, s["y"] - melee_range))

        # Update timer
        s["timer"] -= clock.get_time()
        if s["timer"] <= 0:
            slashes.remove(s)

    # update grenades: move, timer, explode
    for g in grenades[:]:
        # Move
        g["x"] += g["vx"]
        g["y"] += g["vy"]

        # Apply friction (slows down gradually)
        friction = .95  # closer to 1.0 = slower stop, lower = faster stop
        g["vx"] *= friction
        g["vy"] *= friction

        # If speed is nearly zero, stop completely
        if abs(g["vx"]) < 0.05 and abs(g["vy"]) < 0.05:
            g["vx"], g["vy"] = 0, 0

        # Timer countdown
        g["timer"] -= clock.get_time()

        # Draw grenade
        pygame.draw.circle(screen, ORANGE, (int(g["x"]), int(g["y"])), grenade_radius)

        # Explosion
        if g["timer"] <= 0:
            eff_grenade_damage = int(grenade_base_damage * damage_mult)
            for z in zombies[:]:
                if math.hypot(z["x"] - g["x"], z["y"] - g["y"]) <= grenade_explosion_radius:
                    z["health"] -= eff_grenade_damage
                    if z["health"] <= 0:
                        if z in zombies:
                            zombies.remove(z)
                        score += 10
                        zombies_remaining -= 1
                        if random.random() < 0.18:
                            powerups.append([z["x"], z["y"], random.choice(["ammo", "health"])])
            pygame.draw.circle(screen, RED, (int(g["x"]), int(g["y"])), grenade_explosion_radius, 2)
            grenades.remove(g)

    # collisions & pickups
    check_collisions()

    # wave progression
    if zombies_remaining <= 0 and not in_store and zombies_to_spawn <= 0:
        next_wave()

    # draw player
    pygame.draw.circle(screen, BLUE, (int(player_pos[0]), int(player_pos[1])), player_radius)

    # --- MELEE COOLDOWN BAR ---
    elapsed = now - last_melee
    progress = min(1, elapsed / melee_cooldown)

    bar_width = 40
    bar_height = 6
    bar_x = player_pos[0] - bar_width // 2
    bar_y = player_pos[1] - 40  # slightly above player

    # Background (gray)
    pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))

    # Fill (red grows as slash recharges)
    pygame.draw.rect(
        screen,
        (200, 50, 50),
        (bar_x, bar_y, int(bar_width * progress), bar_height)
    )


    # draw bullets
    for b in bullets:
        pygame.draw.circle(screen, WHITE, (int(b[0]), int(b[1])), bullet_radius)

    # draw zombies with health bars
    for z in zombies:
        color = GREEN if z["type"] == "normal" else (RED if z["type"] == "runner" else GRAY)
        rect_x = int(z["x"] - zombie_size // 2)
        rect_y = int(z["y"] - zombie_size // 2)
        pygame.draw.rect(screen, color, (rect_x, rect_y, zombie_size, zombie_size))

        # health bar above zombie
        max_hp = z.get("max_health", 1)
        hp_ratio = max(0.0, z["health"]) / max_hp if max_hp > 0 else 0.0
        bar_w = zombie_size
        bar_h = 5
        bar_x = rect_x
        bar_y = rect_y - 8
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))

    # draw powerups
    for p in powerups:
        color = YELLOW if p[2] == "ammo" else RED
        pygame.draw.rect(screen, color, (p[0] - POWERUP_SIZE // 2, p[1] - POWERUP_SIZE // 2, POWERUP_SIZE, POWERUP_SIZE))
        label = small_font.render(("A" if p[2] == "ammo" else "+"), True, WHITE)
        screen.blit(label, (p[0] - label.get_width() // 2, p[1] - label.get_height() // 2))

    # draw shop items when in store
    if in_store:
        inst = font.render("STORE (walk over item to buy) - Press ENTER to leave store", True, WHITE)
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 8))
        draw_shop_items()

    # draw ui
    draw_ui()

    pygame.display.flip()
    clock.tick(60)

    # ensure shop message clears automatically (handled in draw_ui by time check)
    if shop_message and pygame.time.get_ticks() - shop_message_time > shop_message_duration:
        shop_message = ""

    # END condition
    if player_health <= 0:
        running = False

pygame.quit()
sys.exit()
