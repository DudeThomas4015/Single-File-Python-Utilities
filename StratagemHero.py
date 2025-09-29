import random
import time
import keyboard
import os

# Define stratagems with their associated commands
stratagems = {
    "LIFT-850 Jump Pack": ["↓", "↑", "↑", "↓", "↑"],
    "B-1 Supply Pack": ["↓", "←", "↓", "↑", "↑", "↓"],
    "AX/LAS-5 Guard Dog Rover": ["↓", "↑", "←", "↑", "→", "→"],
    "SH-20 Ballistic Shield Backpack": ["↓", "←", "↓", "↓", "↑", "←"],
    "AX/AR-23 Guard Dog": ["↓", "↑", "←", "↑", "→", "↓"],
    "MG-43 Machine Gun": ["↓", "←", "↓", "↑", "→"],
    "APW-1 Anti-Material Rifle": ["↓", "←", "→", "↑", "↓"],
    "M-105 Stalwart": ["↓", "←", "↓", "↑", "↑", "←"],
    "EAST-17 Expendable Anti-Tank": ["↓", "↓", "←", "↑", "→"],
    "GR-8 Recoiless Rifle": ["↓", "←", "→", "→", "←"],
    "FLAM-40 Flamethrower": ["↓", "←", "↑", "↓", "↑"],
    "AC-8 Autocannon": ["↓", "←", "↓", "↑", "↑", "→"],
    "MG-206 Heavy Machine Gun": ["↓", "←", "↑", "↓", "↓"],
    "RS-422 Railgun": ["↓", "→", "←", "↓", "↑", "←", "→"],
    "FAF-14 Spear Launcher": ["↓", "↓", "↑", "↓", "↓"],
    "GL-21 Grenade Launcher": ["↓", "←", "↑", "←", "↓"],
    "LAS-98 Laser Cannon": ["↓", "←", "↓", "↑", "←"],
    "ARC-3 Arc Thrower": ["↓", "→", "↓", "↑", "←", "←"],
    "LAS-99 Quasar Cannon": ["↓", "↓", "↑", "←", "→"],
    "EXO-45 Patriot Exosuit": ["←", "↓", "→", "↑", "←", "↓", "↓"],
    "Reinforce": ["↑", "↓", "→", "←", "↑"],
    "SOS Beacon": ["↑", "↓", "→", "←"],
    "Resupply": ["↓", "↓", "↑", "→"],
    "NUX-223 Hellbomb": ["↓", "↑", "←", "↓", "↑", "→", "↓", "↑"],
    "SSSD Delivery": ["↓", "↓", "↓", "↑", "↑"],
    "Seismic Probe": ["↑", "↑", "←", "→", "↓", "↓"],
    "Upload Data": ["←", "→", "↑", "↑", "↑"],
    "Eagle Re-arm": ["↑", "↑", "←", "↑", "→"],
    "Illumination Flare": ["→", "→", "←", "←"],
    "SEAF Artillery": ["→", "↑", "↑", "↓"],
    "Super Earth Flag": ["↓", "↑", "↓", "↑"],
    "E/MG-101HMG Emplacement": ["↓", "↑", "←", "→", "→", "←"],
    "FX-12 Shield Generator Relay": ["↓", "↓", "←", "→", "←", "→"],
    "A/ARC-3 Tesla Tower": ["↓", "↑", "→", "↑", "←", "→"],
    "MD-6 Anti-Personnel Minefield": ["↓", "←", "↑", "→"],
    "MD-14 incendiary Mines": ["↓", "←", "←", "↓"],
    "A/MG-43 Machine Sentry": ["↓", "↑", "→", "→", "↑"],
    "A/G-16 Gatling Sentry": ["↓", "↑", "→", "←"],
    "A/M-12 Mortar Sentry": ["↓", "↑", "→", "→", "↓"],
    "A/AC-8 Autocannon Sentry": ["↓", "↑", "→", "↑", "←", "↑"],
    "A/MLS-4X Rocket Sentry": ["↓", "↑", "→", "→", "←"],
    "A/M-23 EMS Sentry": ["↓", "↑", "→", "↓", "→"],
    "Orbital Gatling Barrage": ["→", "↓", "←", "↑", "↑"],
    "Orbital Airburst Strike": ["→", "→", "→"],
    "Orbital 120mm HE Barrage": ["→", "→", "↓", "←", "→", "↓"],
    "Orbital 380mm HS Barrage": ["→", "↓", "↑", "↑", "←", "↓", "↓"],
    "Orbital Walking Barrage": ["→", "↓", "→", "↓", "→", "↓"],
    "Orbital Laser": ["→", "↓", "↑", "→", "↓"],
    "Orbital Rail Cannon Strike": ["→", "↑", "↓", "↓", "→"],
    "Orbital Precision Strike": ["→", "→", "↑"],
    "Orbital Gas Strike": ["→", "→", "↓", "→"],
    "Orbital EMS Strike": ["→", "→", "←", "↓"],
    "Orbital Smoke Strike": ["→", "→", "↓", "↑"],
    "Eagle Strafing Run": ["↑", "→", "→"],
    "Eagle Airstrike": ["↑", "→", "↓", "→"],
    "Eagle Cluster Bomb": ["↑", "→", "↓", "↓", "→"],
    "Eagle Napalm": ["↑", "→", "↓", "↑"],
    "Eagle Smoke Strike": ["↑", "→", "↑", "↓"],
    "Eagle 110mm Rockets": ["↑", "→", "↑", "←"],
    "Eagle 500kg Bomb": ["↑", "→", "↓", "↓", "↓"]
}

# Mapping of keys to commands
key_mapping = {
    "→": "right",
    "←": "left",
    "↑": "up",
    "↓": "down"
}

def get_random_stratagem():
    """Select a random stratagem from the list."""
    return random.choice(list(stratagems.items()))

def display_stratagem(name, commands, stratagems_to_complete):
    """Display the stratagem name and commands."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{name}: {' '.join(commands)}")
    #print(f"#{stratagems_to_complete} {name}: {' '.join(commands)}")

def get_user_input(expected_commands, end_time):
    """Get the user's input for the commands and check for correctness."""
    for command in expected_commands:
        while time.time() < end_time:
            key_pressed = None
            for key, mapped_key in key_mapping.items():
                if keyboard.is_pressed(mapped_key):
                    key_pressed = key
                    time.sleep(0.15)  # Add a small delay to avoid multiple detections
                    break
            if key_pressed:
                if key_pressed == command:
                    print(command, end=" ", flush=True)
                    break
                else:
                    return False
        else:
            return None  # Time's up
    print()  # Newline after input sequence
    return True

def play_round(round_number, time_limit):
    """Play a round of the game."""
    start_time = time.time()
    end_time = start_time + time_limit
    stratagems_to_complete = 5

    while stratagems_to_complete > 0 and time.time() < end_time:
        name, commands = get_random_stratagem()
        while time.time() < end_time:
            display_stratagem(name, commands, stratagems_to_complete)
            result = get_user_input(commands, end_time)
            if result is None:
                return False  # Time's up
            elif result:
                stratagems_to_complete -= 1
                break

    return stratagems_to_complete == 0

def main():
    round_number = 1
    time_limit = 20
    print("Welcome to STRATAGEM HERO!")
    input("Press Enter to start...")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Round {round_number} - Complete 5 stratagems in {time_limit} seconds.")
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        
        if not play_round(round_number, time_limit):
            print(f"Time's up! You reached round {round_number}.")
            break
        
        round_number += 1
        time_limit *= 0.8

    print("Game Over!")
    time.sleep(3)

if __name__ == "__main__":
    main()
