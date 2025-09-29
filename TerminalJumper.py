import keyboard
import time
import os 
import random

# Game parameters
screen_width = 50
player_pos = 10
player_char = 'P'
ground_char = '-'
ground_level = screen_width - 1
speed = 0.1  # Initial speed (lower values make the game faster)
jump_height = 3
gravity = 0.5
is_jumping = False
jump_speed = 0
player_y = ground_level
points = 0

# Define an initial list of obstacles
obstacles = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_screen():
    # Create an empty screen
    screen = [' ' * screen_width for _ in range(screen_width)]
    
    # Ensure player_y is an integer
    player_y_int = int(player_y)

    # Place player on the screen
    if player_y_int < screen_width:
        screen[player_y_int] = screen[player_y_int][:player_pos] + player_char + screen[player_y_int][player_pos + 1:]

    # Place obstacles on the screen
    for obstacle in obstacles:
        pos = obstacle['pos']
        shape = obstacle['shape']
        position_y = obstacle['position_y']
        for i, row in enumerate(shape):
            row_y = position_y + i  # Determine the y-position for each part of the obstacle
            if row_y < screen_width:
                for j, char in enumerate(row):
                    if pos + j < screen_width and char != ' ':
                        screen[row_y] = screen[row_y][:pos + j] + char + screen[row_y][pos + j + 1:]
                        # Check for collision
                        if player_pos == pos + j and player_y_int == row_y:
                            print("You hit an obstacle! You got " + str(points) + " points! Game Over!")
                            time.sleep(3)
                            exit()

    # Print the screen
    for line in screen:
        print(line)
    
    print(ground_char * screen_width)

def update_player():
    global is_jumping, jump_speed, player_y

    if is_jumping:
        player_y -= jump_speed
        jump_speed -= gravity
        if player_y >= ground_level:
            player_y = ground_level
            is_jumping = False

def handle_input():
    global is_jumping, jump_speed

    if keyboard.is_pressed('right'):
        global player_pos
        player_pos += 1
        if player_pos >= screen_width:
            player_pos = 0

    if keyboard.is_pressed('left'):
        player_pos -= 1
        if player_pos < 0:
            player_pos = screen_width - 1

    if keyboard.is_pressed('space') and player_y == ground_level:
        is_jumping = True
        jump_speed = jump_height

def generate_random_obstacle():
    """Generate a random obstacle with a random height between 2 and 5 rows."""
    height = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5])
    
    width = random.choice([2, 2, 2, 2, 2, 3, 3, 4])
    
    shape = ['O' * width] * height  # Generate a column of 'OO' with the specified height
    
    position_y = ground_level - height + 1  # Position the tower at the ground level

    return {
        'pos': screen_width - 1,
        'shape': shape,
        'position_y': position_y
    }

def move_obstacles():
    global obstacles
    for obstacle in obstacles:
        obstacle['pos'] -= 1
    # Remove obstacles that move off the screen
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle['pos'] >= 0]

def game_loop():
    obstacle_spawn_timer = 0
    obstacle_spawn_delay = random.choice([15, 15, 15, 15, 15, 15, 20, 20, 20, 10, 10, 10, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6])  # Number of frames between obstacle spawns
    global speed  # Make speed accessible in the loop
    global points

    while True:
        clear_screen()
        handle_input()
        update_player()
        move_obstacles()

        # Spawn obstacles more frequently
        if obstacle_spawn_timer >= obstacle_spawn_delay:
            obstacles.append(generate_random_obstacle())
            obstacle_spawn_timer = 0
        else:
            obstacle_spawn_timer += 1

        print_screen()
        points +=1

        # Increase speed slightly over time
        speed -= 0.0001  # Decrease sleep time, making the game faster

        time.sleep(speed)

if __name__ == "__main__":
    game_loop()
    