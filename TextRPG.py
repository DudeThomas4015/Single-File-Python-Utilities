import random

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
            choice = int(input("Enter attack number: ")) - 1  # Adjust index here
            if choice < 0 or choice >= len(all_attacks):
                print("Invalid choice. Please choose a valid attack number.")
            elif all_attacks[choice] in available_attacks:
                return all_attacks[choice]
            else:
                print(f"{all_attacks[choice]['name']} is on cooldown. Please choose another attack.")


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
    Enemy("Skeleton", 100, [{'name': 'Bone Club', 'damage': 12, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Arrow Shot', 'damage': 10, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Summon Minions', 'damage': 15, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Bone Shield', 'damage': 0, 'cooldown': 4, 'current_cooldown': 0}]),
    Enemy("Dragon", 150, [{'name': 'Fire Breath', 'damage': 25, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Tail Swipe', 'damage': 20, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Claw Strike', 'damage': 22, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Wing Buffet', 'damage': 0, 'cooldown': 5, 'current_cooldown': 0}]),
    Enemy("Witch", 90, [{'name': 'Hex', 'damage': 15, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Cursed Bolt', 'damage': 18, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Summon Familiar', 'damage': 10, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Dark Ritual', 'damage': 0, 'cooldown': 4, 'current_cooldown': 0}]),
    Enemy("Bandit", 70, [{'name': 'Ambush', 'damage': 10, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Snipe', 'damage': 12, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Dodge', 'damage': 8, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Escape', 'damage': 0, 'cooldown': 3, 'current_cooldown': 0}])
]

# Define bosses in order of difficulty
bosses = [
    Enemy("Giant", 200, [{'name': 'Smash', 'damage': 30, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Stomp', 'damage': 25, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Roar', 'damage': 20, 'cooldown': 1, 'current_cooldown': 0}, {'name': 'Boulder Throw', 'damage': 35, 'cooldown': 4, 'current_cooldown': 0}]),
    Enemy("Troll King", 250, [{'name': 'Club Smash', 'damage': 35, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Regenerate', 'damage': 0, 'heal': 40, 'cooldown': 5, 'current_cooldown': 0}, {'name': 'Frenzy', 'damage': 50, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Roar', 'damage': 20, 'cooldown': 1, 'current_cooldown': 0}]),
    Enemy("Lich", 300, [{'name': 'Dark Magic', 'damage': 40, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Summon Undead', 'damage': 20, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Curse', 'damage': 30, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Life Drain', 'damage': 25, 'heal': 25, 'cooldown': 3, 'current_cooldown': 0}]),
    Enemy("Dragon King", 350, [{'name': 'Inferno', 'damage': 45, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Tail Sweep', 'damage': 35, 'cooldown': 2, 'current_cooldown': 0}, {'name': 'Wing Storm', 'damage': 40, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Fireball', 'damage': 50, 'cooldown': 3, 'current_cooldown': 0}]),
    Enemy("Demon Lord", 400, [{'name': 'Hellfire', 'damage': 60, 'cooldown': 4, 'current_cooldown': 0}, {'name': 'Shadow Strike', 'damage': 50, 'cooldown': 3, 'current_cooldown': 0}, {'name': 'Summon Demons', 'damage': 40, 'cooldown': 5, 'current_cooldown': 0}, {'name': 'Dark Ritual', 'damage': 0, 'heal': 50, 'cooldown': 6, 'current_cooldown': 0}])
]

# Main game logic
def main():
    player_name = input("Enter your name: ")
    player_class = choose_class()
    player = Character(player_name, player_class)

    enemy_count = 0
    base_enemy_rounds = 10  # Number of rounds to fight base enemies before encountering a boss
    while enemy_count / 10 < len(bosses):
        if enemy_count % base_enemy_rounds == 0 and enemy_count > 0:
            # Boss fight
            boss = bosses[enemy_count // base_enemy_rounds - 1]
            boss.max_health = int(boss.max_health * (1 + 0.1 * (player.level - 1)))  # Scaling boss health based on player level
            for attack in boss.attacks:
                if 'damage' in attack:
                    attack['damage'] = int(attack['damage'] * (1 + 0.1 * (player.level - 1)))  # Scaling boss attacks based on player level
                if 'heal' in attack:
                    attack['heal'] = int(attack['heal'] * (1 + 0.1 * (player.level - 1)))  # Scaling boss heals based on player level
            boss.reset()  # Reset boss's health and cooldowns
            print(f"\nWelcome, {player.name}, the {player.char_class}!\n")
            if not battle(player, boss):
                print("Game Over!")
                break
            print(f"\nCongratulations! You have defeated {boss.name}!\n")
        else:
            # Random base enemy fight
            enemy = random.choice(base_enemies)
            enemy.max_health = int(enemy.max_health * (1 + 0.1 * (player.level - 1)))  # Scaling base enemy health
            for attack in enemy.attacks:
                if 'damage' in attack:
                    attack['damage'] = int(attack['damage'] * (1 + 0.1 * (player.level - 1)))  # Scaling base enemy attacks
            enemy.reset()  # Reset enemy's health and cooldowns
            print(f"\nWelcome, {player.name}, the {player.char_class}!\n")
            if not battle(player, enemy, enemy_count):
                print("Game Over!")
                break
        # Calculate XP gained and level up if applicable
        xp_gained = int(enemy.max_health / 10)
        player.xp += xp_gained
        print(f"{player.name} gained {xp_gained} XP!")
        while player.xp >= 10 * player.level:
            player.level_up()
        enemy_count += 1
        input("Press Enter to continue...")  # Wait for player to continue

    if enemy_count == len(bosses) * base_enemy_rounds:
        print("\nCongratulations! You have defeated the Demon Lord and completed the game!")

def battle(player, enemy, enemy_count):
    print(f"A wild {enemy.name} appears!\n")
    while player.current_health > 0 and enemy.current_health > 0:
        print(f"{player.name}'s HP: {player.current_health}/{player.max_health}")
        print(f"{enemy_count+1}. {enemy.name}'s HP: {enemy.current_health}/{enemy.max_health}\n")

        # Player's turn
        player_attack = player.choose_attack()
        if player_attack is None:
            print("All your moves are on cooldown! You must wait.")
        else:
            if player_attack['name'] == 'Block':
                player.block_active = True
                print(f"{player.name} used {player_attack['name']}!")
            elif 'heal' in player_attack:
                heal_amount = player_attack['heal'] + int(player.level * 0.1 * player_attack['heal'])
                player.heal(heal_amount)
                print(f"{player.name} used {player_attack['name']} and healed for {heal_amount} HP!")
            else:
                player.block_active = False
                for attack in player.attacks[player.char_class]:
                    if attack['name'] == player_attack['name']:
                        damage = attack['damage'] + int(player.level * 0.1 * attack['damage'])
                        enemy.take_damage(damage)
                        print(f"{player.name} used {player_attack['name']} on {enemy.name} and dealt {damage} damage!")
                        if 'heal' in attack:
                            heal_amount = attack['heal'] + int(player.level * 0.1 * attack['heal'])
                            player.heal(heal_amount)
                            print(f"{player.name} healed for {heal_amount} HP!")
                        break
            player_attack['current_cooldown'] = player_attack['cooldown']


        # Enemy's turn
        if enemy.current_health > 0:  # Enemy attacks only if they are alive
            enemy_attack = enemy.choose_attack()
            if enemy_attack is None:
                print(f"{enemy.name} has no moves available this turn!")
            else:
                for attack in enemy.attacks:
                    if attack['name'] == enemy_attack['name']:
                        damage = attack['damage']
                        player.take_damage(damage)  # Enemy attacks the player
                        print(f"{enemy.name} used {enemy_attack['name']} on {player.name} and dealt {damage} damage!\n")
                        break
                enemy_attack['current_cooldown'] = enemy_attack['cooldown']

        # Reduce cooldowns at the end of each turn
        player.reduce_cooldowns()
        enemy.reduce_cooldowns()

    # Battle outcome
    if player.current_health <= 0:
        print(f"{player.name} was defeated by {enemy.name}!")
        return False
    elif enemy.current_health <= 0:
        print(f"{player.name} defeated {enemy.name}!")
        return True

# Start the game
if __name__ == "__main__":
    main()
