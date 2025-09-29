import random
import time
import os

# Character and Enemy classes (from your fighting game code)
class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.max_health = 100
        self.current_health = self.max_health
        self.xp = 0
        self.damage_multiplier = 1.0
        self.attacks = {
            'warrior': [
                {'name': 'Slash', 'damage': 20, 'cooldown': 1, 'current_cooldown': 0},
                {'name': 'Bash', 'damage': 28, 'cooldown': 2, 'current_cooldown': 0},
                {'name': 'Healing Potion', 'heal': 45, 'cooldown': 3, 'current_cooldown': 0},
                {'name': 'Block', 'damage': 0, 'cooldown': 1, 'current_cooldown': 0}  # Block will nullify incoming damage for one turn
            ],
            'mage': [
                {'name': 'Fireball', 'damage': 30, 'cooldown': 4, 'current_cooldown': 0},
                {'name': 'Ice Bolt', 'damage': 15, 'cooldown': 1, 'current_cooldown': 0},
                {'name': 'Thunder Shock', 'damage': 23, 'cooldown': 2, 'current_cooldown': 0},
                {'name': 'Healing Aura', 'heal': 80, 'cooldown': 3, 'current_cooldown': 0}  # Healing Aura heals 20 HP
            ],
            'rogue': [
                {'name': 'Backstab', 'damage': 22, 'cooldown': 1, 'current_cooldown': 0},
                {'name': 'Poison Dagger', 'damage': 18, 'cooldown': 1, 'current_cooldown': 0},
                {'name': 'Shadow Step', 'damage': 30, 'cooldown': 2, 'current_cooldown': 0},
                {'name': 'Vampiric Blade', 'damage': 15, 'heal': 20, 'cooldown': 2, 'current_cooldown': 0}  # Vampiric Blade deals 16 damage and heals 10 HP
            ]
        }
        self.block_active = False  # Flag to track if block is active this turn

    def choose_attack(self):
        available_attacks = []
        all_attacks = []
        print(f"Choose an attack for {self.name}:")

        for i, attack in enumerate(self.attacks[self.char_class], start=1):
            if attack['current_cooldown'] == 0:
                if 'damage' in attack and 'heal' in attack:
                    damage = attack['damage'] + int(self.level * 0.1 * attack['damage'])
                    heal = attack['heal'] + int(self.level * 0.1 * attack['heal'])
                    print(f"{i}. {attack['name']} - Damage: {damage} - Heal: {heal} HP (Cooldown: {attack['cooldown']} turns)")
                elif 'damage' in attack:
                    damage = attack['damage'] + int(self.level * 0.1 * attack['damage'])
                    print(f"{i}. {attack['name']} - Damage: {damage} (Cooldown: {attack['cooldown']} turns)")
                elif 'heal' in attack:
                    heal = attack['heal'] + int(self.level * 0.1 * attack['heal'])
                    print(f"{i}. {attack['name']} - Heal: {heal} HP (Cooldown: {attack['cooldown']} turns)")
                available_attacks.append(attack)
            else:
                print(f"{i}. {attack['name']} - On Cooldown ({attack['current_cooldown']} turns left)")
            all_attacks.append(attack)

        # Check if any attack in all_attacks is available (i.e., in available_attacks)
        if not any(attack in available_attacks for attack in all_attacks):
            print("No attacks available, all moves are on cooldown!")
            return None

        while True:
            try:
                choice = int(input("Enter attack number: ")) - 1  # Adjust index here
                if choice < 0 or choice >= len(all_attacks):
                    print("Invalid choice. Please choose a valid attack number.")
                elif all_attacks[choice] in available_attacks:
                    return all_attacks[choice]
                else:
                    print(f"{all_attacks[choice]['name']} is on cooldown. Please choose another attack.")
            except:
                print("Invalid input. Please enter a number.")

    def reduce_cooldowns(self):
        for attack in self.attacks[self.char_class]:
            if attack['current_cooldown'] > 0:
                attack['current_cooldown'] -= 1

    def take_damage(self, damage):
        if self.block_active:
            print(f"{self.name} used Block and blocked the attack!")
        else:
            self.current_health -= damage
            if self.current_health < 0:
                self.current_health = 0
            print(f"{self.name} took {damage} damage!")
        self.block_active = False  # Reset block status after damage is taken

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def level_up(self):
        self.level += 1
        old_max_health = self.max_health
        self.max_health = int(self.max_health * 1.1)
        self.current_health += int(self.max_health / 10)
        self.damage_multiplier *= 1.1
        print(f"{self.name} leveled up to level {self.level}!")
        print(f"Max health increased to {self.max_health}.")
        print(f"Damage increased by 10%.")

class Enemy:
    def __init__(self, name, max_health, attacks):
        self.name = name
        self.max_health = max_health
        self.current_health = self.max_health
        self.attacks = attacks

    def reset(self):
        self.current_health = self.max_health
        for attack in self.attacks:
            attack['current_cooldown'] = 0

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def choose_attack(self):
        available_attacks = [attack for attack in self.attacks if attack['current_cooldown'] == 0]
        if not available_attacks:
            return None
        return random.choice(available_attacks)

    def reduce_cooldowns(self):
        for attack in self.attacks:
            if attack['current_cooldown'] > 0:
                attack['current_cooldown'] -= 1

def choose_name():
    return input("Enter your character's name: ")

# Function to let player choose class
def choose_class():
    while True:
        print("Choose your class:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Rogue")
        class_choice = input("Enter class number: ")
        if class_choice == '1':
            return 'warrior'
        elif class_choice == '2':
            return 'mage'
        elif class_choice == '3':
            return 'rogue'
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Define base enemies
base_enemies = [
    Enemy("Goblin", 80, [{'name': 'Swipe', 'damage': 15, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Stab', 'damage': 10, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Throw Rock', 'damage': 12, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Call Reinforcements', 'damage': 0, 'cooldown': 3, 'current_cooldown': 0}]),
    Enemy("Orc", 120, [{'name': 'Crush', 'damage': 18, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Roar', 'damage': 14, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Smash', 'damage': 20, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'War Cry', 'damage': 0, 'cooldown': 4, 'current_cooldown': 0}]),
    Enemy("Skeleton", 100, [{'name': 'Bone Club', 'damage': 12, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Arrow Shot', 'damage': 10, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Curse', 'damage': 0, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Regenerate', 'damage': 0, 'cooldown': 5, 'current_cooldown': 0}]),
    Enemy("Dragon", 200, [{'name': 'Fire Breath', 'damage': 25, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Tail Whip', 'damage': 20, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Bite', 'damage': 30, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Wing Flap', 'damage': 15, 'cooldown': 1, 'current_cooldown': 0}])
]
bosses = [
    Enemy("Giant", 200, [{'name': 'Smash', 'damage': 30, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Stomp', 'damage': 25, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Roar', 'damage': 20, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Boulder Throw', 'damage': 35, 'cooldown': 4, 'current_cooldown': 0}]),
    Enemy("Troll King", 250, [{'name': 'Club Smash', 'damage': 35, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Regenerate', 'damage': 0, 'heal': 40, 'cooldown': 5, 'current_cooldown': 0}, {'name': 'Frenzy', 'damage': 50, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Roar', 'damage': 20, 'cooldown': 1, 'current_cooldown': 0}]),
    Enemy("Lich", 300, [{'name': 'Dark Magic', 'damage': 40, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Summon Undead', 'damage': 20, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Curse', 'damage': 30, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Life Drain', 'damage': 25, 'heal': 25, 'cooldown': 3, 'current_cooldown': 0}]),
    Enemy("Dragon King", 350, [{'name': 'Inferno', 'damage': 45, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Tail Sweep', 'damage': 35, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Wing Storm', 'damage': 40, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Fireball', 'damage': 50, 'cooldown': 3, 'current_cooldown': 0}]),
    Enemy("Demon Lord", 400, [{'name': 'Hellfire', 'damage': 60, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Shadow Strike', 'damage': 50, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Summon Demons', 'damage': 40, 'cooldown': 5, 'current_cooldown': 0}, {'name': 'Dark Ritual', 'damage': 0, 'heal': 50, 'cooldown': 6, 'current_cooldown': 0}])
]

# Function to start a battle
def battle(player, enemy):
    enemy.reset()
    print(f"A wild {enemy.name} appears!")
    while player.current_health > 0 and enemy.current_health > 0:
        print(f"\n{player.name}'s Health: {player.current_health}/{player.max_health}")
        print(f"{enemy.name}'s Health: {enemy.current_health}/{enemy.max_health}")
        
        # Player's turn
        attack = player.choose_attack()
        if attack is not None:
            if 'damage' in attack:
                damage = attack['damage'] + int(player.level * 0.1 * attack['damage'])
                enemy.take_damage(damage)
                print(f"{player.name} used {attack['name']}! {enemy.name} took {damage} damage!")
                if attack['name'] == 'Block':
                    player.block_active = True
            if 'heal' in attack:
                heal = attack['heal'] + int(player.level * 0.1 * attack['heal'])
                player.heal(heal)
                print(f"{player.name} used {attack['name']} and healed {heal} HP!")
            attack['current_cooldown'] = attack['cooldown']

        if enemy.current_health <= 0:
            print(f"{enemy.name} is defeated!")
            player.xp += 50  # Increase XP by 50 for each enemy defeated
            if player.xp >= 100:  # Level up every 100 XP
                player.level_up()
                player.xp -= 100  # Reduce XP by 100 after leveling up
            break

        # Enemy's turn
        enemy_attack = enemy.choose_attack()
        if enemy_attack is not None:
            if 'damage' in enemy_attack:
                player.take_damage(enemy_attack['damage'])
                print(f"{enemy.name} used {enemy_attack['name']}! {player.name} took {enemy_attack['damage']} damage!")
            enemy_attack['current_cooldown'] = enemy_attack['cooldown']

        if player.current_health <= 0:
            print(f"{player.name} has been defeated by {enemy.name}!")
            print("Try again next time")
            time.sleep(3)
            quit()
            

        player.reduce_cooldowns()
        enemy.reduce_cooldowns()

# Maze game integration
class PacmanGame:
    def __init__(self):
        self.maze = [
            ['#', 'P', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
            ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#']
        ]
        self.maze2 = [
            ['#', 'P', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
            ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]
        self.maze3 = [
            ['#', 'P', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', 'H', '#'],
            ['#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
            ['#', ' ', ' ', 'E', '#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#'],
            ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', '#', '#'],
            ['#', 'H', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', 'E', ' ', ' ', '#'],
            ['#', ' ', '#', '#', '#', '#', '#', 'E', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]
        self.maze4 = [
            ['#', 'P', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', '#', ' ', '#', 'H', '#', ' ', ' ', ' ', 'E', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', 'E', '#'],
            ['#', 'E', '#', ' ', ' ', ' ', ' ', '#', 'H', ' ', '#', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', '#', ' ', ' '],
            ['#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', 'E', ' ', ' ', ' ', 'E', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]
        self.maze5 = [
            ['#', 'P', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', '#', '#', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', 'H', ' ', '#', 'O', '#', ' ', 'H', ' ', '#', ' ', '#'],
            ['#', ' ', '#', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', ' ', '#', ' ', '#'],
            ['#', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]
        self.goal_posx = 10
        self.goal_posy = 13
        self.player_pos = [0, 1]  # Starting position of the player
        self.enemies_pos = [[1, 10], [5, 10], [9, 12]]  # Positions of enemies
        self.potions_pos = [[3, 10], [7, 3]]  # Positions of health potions
        self.iter = 0
        
        for pos in self.enemies_pos:
            self.maze[pos[0]][pos[1]] = 'E'  # Place enemies in the maze
            
        for pos in self.potions_pos:
            self.maze[pos[0]][pos[1]] = 'H'  # Place health potions in the maze

    def display_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.maze:
            print(''.join(row))
        print(f"Player's Health: {player.current_health}/{player.max_health}, XP: {player.xp}, Level: {player.level}")

    def move_player(self, direction):
        x, y = self.player_pos
        if direction == 'W':
            new_x, new_y = x - 1, y
        elif direction == 'S':
            new_x, new_y = x + 1, y
        elif direction == 'A':
            new_x, new_y = x, y - 1
        elif direction == 'D':
            new_x, new_y = x, y + 1
        else:
            return self.player_pos
        
        if new_x == self.goal_posx and new_y == self.goal_posy:
            
            if self.iter == 0:
                print("Entering new map...")
                time.sleep(2)
                
                self.maze = self.maze2
                self.player_pos = [0, 1]
                self.goal_posx = 0
                self.goal_posy = 12
                
                self.enemies_pos = [[1, 5], [9, 1], [3, 11]]  # Positions of enemies
                self.potions_pos = [[7, 1], [5, 13]]  # Positions of health potions
        
                for pos in self.enemies_pos:
                    self.maze[pos[0]][pos[1]] = 'E'  # Place enemies in the maze
            
                for pos in self.potions_pos:
                    self.maze[pos[0]][pos[1]] = 'H'  # Place health potions in the maze
                    
            elif self.iter == 1:
                print("Entering new map...")
                time.sleep(2)
                
                self.maze = self.maze3
                self.player_pos = [0, 1]
                self.goal_posx = 10
                self.goal_posy = 1
                
                self.enemies_pos = [[5, 3], [7, 11], [8, 7]]  # Positions of enemies
                self.potions_pos = [[7, 1], [1, 13]]  # Positions of health potions
        
                for pos in self.enemies_pos:
                    self.maze[pos[0]][pos[1]] = 'E'  # Place enemies in the maze
            
                for pos in self.potions_pos:
                    self.maze[pos[0]][pos[1]] = 'H'  # Place health potions in the maze
                    
            elif self.iter == 2:
                print("Entering new map...")
                time.sleep(2)
                
                self.maze = self.maze4
                self.player_pos = [0, 1]
                self.goal_posx = 7
                self.goal_posy = 14
                
                self.enemies_pos = [[5, 1], [1, 10], [4, 13], [9, 7], [9, 11]]  # Positions of enemies
                self.potions_pos = [[1, 5], [5, 8]]  # Positions of health potions
        
                for pos in self.enemies_pos:
                    self.maze[pos[0]][pos[1]] = 'E'  # Place enemies in the maze
            
                for pos in self.potions_pos:
                    self.maze[pos[0]][pos[1]] = 'H'  # Place health potions in the maze
                    
            elif self.iter == 3:
                print("Entering new map...")
                time.sleep(2)
                
                self.maze = self.maze5
                self.player_pos = [0, 1]
                self.goal_posx = 6
                self.goal_posy = 7
                
                self.enemies_pos = []  # Positions of enemies
                self.potions_pos = [[6, 4], [6, 10]]  # Positions of health potions
        
                for pos in self.enemies_pos:
                    self.maze[pos[0]][pos[1]] = 'E'  # Place enemies in the maze
            
                for pos in self.potions_pos:
                    self.maze[pos[0]][pos[1]] = 'H'  # Place health potions in the maze
                    
            elif self.iter == 4:
                print("Entering the boss fight...")
                time.sleep(2)
                
                battle(player, random.choice(bosses))
                print(f"\n\n\n\n\nCongratulations {player.name}! You beat the game as a {player_class}! Try again to fight more monsters and different bosses!")
                input("\nPress enter to close...")
                quit()
                    
            self.iter += 1
            return self.player_pos

        if self.maze[new_x][new_y] in [' ', 'E', 'H']:
            self.maze[x][y] = ' '
            self.player_pos = [new_x, new_y]
            self.maze[new_x][new_y] = 'P'
            if [new_x, new_y] in self.enemies_pos:
                enemy = random.choice(base_enemies)
                battle(player, enemy)
                self.enemies_pos.remove([new_x, new_y])
                if player.current_health <= 0:
                    print("Game Over!")
                    return False
            elif [new_x, new_y] in self.potions_pos:
                player.heal(50)
                print(f"{player.name} found a health potion and healed 50 HP!")
                self.potions_pos.remove([new_x, new_y])
            return True
        else:
            return True


# Main game loop
player_name = choose_name()
player_class = choose_class()
player = Character(player_name, player_class)

game = PacmanGame()
game.maze[game.player_pos[0]][game.player_pos[1]] = 'P'

while True:
    game.display_maze()
    move = input("Move (WASD): ").upper()
    if not game.move_player(move):
        break
