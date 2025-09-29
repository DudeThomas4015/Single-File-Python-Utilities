import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
HALF_HEIGHT = HEIGHT // 2
FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = 80
SPEED = 0.25
TURN_SPEED = 0.03
TILE_SIZE = 5
MAP_SCALE = 10

# Mini-map constants
MINIMAP_SCALE = .5
MINIMAP_TILE_SIZE = TILE_SIZE // MINIMAP_SCALE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
RED = (255, 0, 0)

# Map
game_map = [
    "11111111111111111111111111111111111111111111111111111111111111111111111111111111",
    "10000000000000100000000001000000000000001000000000000000000000000000000000000001",
    "10111110001110111100001111111110001110111110001111011111111111111100111000111101",
    "10000000001000000001000000000000000001000000001000000001111111111100111100000001",
    "11111111111111111111111111100000000001111111111000011111111111111100111111101111",
    "10000000000000100000000000000000000000000000000000000001000000000000000000001111",
    "10111111111110111100111111111111111111111111111110111111110111111100111111100011",
    "10000000000000000000000000000000000000000000000001000000000000011100111111110001",
    "10111111110011111111110011111110001110111111111111111111100111111100111111110001",
    "10000000000000000000001000000000000000000000000000000000000000000000000000000001",
    "11111111111111111111111111111111111111111111111111111111111111111111111111111111",
]

MAP_WIDTH = len(game_map[0])
MAP_HEIGHT = len(game_map)

# Player starting position and direction
player_x, player_y = 8, 8
player_angle = 0

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text-Based 3D Game with Mini-Map")
font = pygame.font.SysFont("Courier", 24)

def cast_rays():
    """Improved raycasting function to calculate wall distances."""
    rays = []
    for ray in range(NUM_RAYS):
        # Angle of current ray
        ray_angle = player_angle - FOV / 2 + FOV * ray / NUM_RAYS
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Step sizes for ray traversal
        step_size = 0.1
        distance = 0
        hit_wall = False

        while not hit_wall and distance < MAX_DEPTH:
            distance += step_size
            target_x = player_x + distance * cos_a
            target_y = player_y + distance * sin_a

            col, row = int(target_x / TILE_SIZE), int(target_y / TILE_SIZE)

            # Check for out-of-bounds or wall collision
            if 0 <= row < MAP_HEIGHT and 0 <= col < MAP_WIDTH:
                if game_map[row][col] == "1":
                    # Correct distance for fisheye effect
                    corrected_distance = distance * math.cos(player_angle - ray_angle)
                    rays.append((corrected_distance, ray))
                    hit_wall = True

    return rays

def draw_scene(rays):
    """Improved rendering of the 3D scene."""
    screen.fill(BLACK)

    # Draw ceiling and floor
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HALF_HEIGHT))
    pygame.draw.rect(screen, (50, 50, 50), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    # Draw walls
    for distance, ray in rays:
        wall_height = int((HEIGHT*2) / (distance + 0.01))  # Avoid division by zero
        color_intensity = max(50, 255 - int(distance * 10))  # Diminish brightness by distance
        color = (color_intensity, color_intensity, color_intensity)

        wall_x = int(WIDTH / NUM_RAYS * ray)
        wall_y = HALF_HEIGHT - wall_height // 2

        pygame.draw.rect(screen, color, (wall_x, wall_y, WIDTH // NUM_RAYS, wall_height))

def draw_minimap():
    """Render the mini-map in the top-left corner."""
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            tile_x = col * MINIMAP_TILE_SIZE
            tile_y = row * MINIMAP_TILE_SIZE
            color = GRAY if game_map[row][col] == "1" else BLACK
            pygame.draw.rect(screen, color, (tile_x, tile_y, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

    # Draw player on the mini-map
    player_mini_x = int(player_x / TILE_SIZE * MINIMAP_TILE_SIZE)
    player_mini_y = int(player_y / TILE_SIZE * MINIMAP_TILE_SIZE)
    pygame.draw.circle(screen, RED, (player_mini_x, player_mini_y), 4)

    # Draw player's direction on the mini-map
    end_x = player_mini_x + 10 * math.cos(player_angle)
    end_y = player_mini_y + 10 * math.sin(player_angle)
    pygame.draw.line(screen, RED, (player_mini_x, player_mini_y), (end_x, end_y), 2)

# Projectile class
class Projectile:
    def __init__(self, x, y, angle):
        # Start the projectile at the center of the player's position 
        self.start_x = x*2
        self.start_y = y*2
        self.x = x*2
        self.y = y*2
        self.angle = angle
        self.speed = 0.8
        self.radius = max(2, TILE_SIZE // 2)
        self.active = True
        self.max_distance = 40  # Set the maximum distance the projectile can travel

    def move(self):
        """Move the projectile in its direction."""
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Check if the projectile has exceeded its maximum range
        distance_traveled = math.sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2)
        if distance_traveled > self.max_distance:
            self.active = False

        """# Check for collision with walls
        col, row = int(self.x / TILE_SIZE), int(self.y / TILE_SIZE)
        if 0 <= row < MAP_HEIGHT and 0 <= col < MAP_WIDTH and game_map[row][col] == "1":
            self.active = False"""

    def draw(self):
        """Draw the projectile on the screen."""
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        
class ProjectileShow:
    def __init__(self):
        # Start at the bottom center of the screen
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.radius = 100
        self.speed = 5  # Controls how fast it moves up
        self.shrink_rate = 2  # Controls how quickly the projectile shrinks
        self.active = True

    def move(self):
        """Move the projectile upward and shrink."""
        self.y -= self.speed
        self.radius -= self.shrink_rate

        # Deactivate when the projectile disappears
        if self.radius <= 0 or self.y < 0:
            self.active = False

    def offset(self, offset_x):
        """Offset the projectile when the player turns."""
        self.x += offset_x
        
    def offset_move(self, offset_x, offset_y):
        """Offset the projectile when the player moves."""
        self.x += offset_x
        self.y += offset_y

    def draw(self):
        """Draw the projectile on the screen."""
        if self.active:
            pygame.draw.circle(screen, RED, (self.x, self.y), max(1, int(self.radius)))


# Initialize list of projectiles
projectiles = []
projectile_shows = []  # List of animated projectiles

def move_player():
    """Move player based on key inputs and handle collisions."""
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()

    # Calculate new positions based on movement direction
    move_x, move_y = 0, 0
    if keys[pygame.K_w]:  # Forward
        move_x += SPEED * math.cos(player_angle)
        move_y += SPEED * math.sin(player_angle)
    if keys[pygame.K_s]:  # Backward
        move_x -= SPEED * math.cos(player_angle)
        move_y -= SPEED * math.sin(player_angle)
    if keys[pygame.K_a]:  # Strafe left
        move_x += SPEED * math.sin(player_angle)
        move_y -= SPEED * math.cos(player_angle)
    if keys[pygame.K_d]:  # Strafe right
        move_x -= SPEED * math.sin(player_angle)
        move_y += SPEED * math.cos(player_angle)

    # Update player angle for turning
    if keys[pygame.K_LEFT]:  # Turn left
        player_angle -= TURN_SPEED
    if keys[pygame.K_RIGHT]:  # Turn right
        player_angle += TURN_SPEED

    # Check collisions for X and Y separately
    new_x = player_x + move_x
    new_y = player_y + move_y

    if 0 <= int(new_x / TILE_SIZE) < MAP_WIDTH:
        if game_map[int(player_y / TILE_SIZE)][int(new_x / TILE_SIZE)] != "1":
            player_x = new_x

    if 0 <= int(new_y / TILE_SIZE) < MAP_HEIGHT:
        if game_map[int(new_y / TILE_SIZE)][int(player_x / TILE_SIZE)] != "1":
            player_y = new_y


def handle_projectiles():
    """Update and render all active projectiles."""
    for projectile in projectiles[:]:  # Use a copy of the list to avoid modification during iteration
        projectile.move()
        if not projectile.active:
            projectiles.remove(projectile)
        else:
            projectile.draw()

def handle_projectile_shows():
    """Update and render all animated projectiles."""
    for show in projectile_shows[:]:  # Use a copy to avoid modification issues
        show.move()
        if not show.active:
            projectile_shows.remove(show)
        else:
            show.draw()

def main():
    clock = pygame.time.Clock()
    running = True
    prev_angle = player_angle  # Track player's angle between frames
    prev_x, prev_y = player_x, player_y  # Track player's previous position

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Fire a projectile
                        projectiles.append(Projectile(player_x, player_y, player_angle))  # Collision projectile
                        projectile_shows.append(ProjectileShow())  # Animation projectile 

        move_player()
        rays = cast_rays()
        draw_scene(rays)
        
        # Handle player turning offset for projectiles
        angle_delta = player_angle - prev_angle  # Calculate how much the player has turned
        if angle_delta != 0:
            offset_x = -int((WIDTH / FOV) * angle_delta)  # Calculate horizontal offset
            for show in projectile_shows:
                show.offset(offset_x)
                
        # Handle player movement offset for projectiles
        move_delta_x = player_x - prev_x
        move_delta_y = player_y - prev_y
        if move_delta_x != 0 or move_delta_y != 0:
            # Convert player movement into screen-space offsets
            forward_offset = move_delta_x * math.cos(player_angle) + move_delta_y * math.sin(player_angle)
            sideways_offset = move_delta_y * math.cos(player_angle) - move_delta_x * math.sin(player_angle)

            for show in projectile_shows:
                show.offset_move(-sideways_offset * TILE_SIZE*25, forward_offset * TILE_SIZE)

        prev_angle = player_angle  # Update the previous angle
        prev_x, prev_y = player_x, player_y
        
        draw_minimap()
        handle_projectiles()  # Update and draw projectiles
        handle_projectile_shows()  # Render and animate on-screen projectiles
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
