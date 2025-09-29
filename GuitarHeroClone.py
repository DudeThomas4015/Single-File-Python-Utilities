import pygame
import random

pygame.init()

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 300
WHITE = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_RED = (255, 100, 100)
LIGHT_GREEN = (100, 255, 100)
LIGHT_BLUE = (100, 100, 255)
LIGHT_YELLOW = (255, 220, 100)

KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
KEY_COLORS = [RED, GREEN, BLUE, YELLOW]
LIGHT_KEY_COLORS = [LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW]
NOTE_SPEED = 5
SPAWN_RATE = 30
HIT_ZONE_Y = SCREEN_HEIGHT - 100
HIT_ZONE_HEIGHT = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero (Without Music)")
clock = pygame.time.Clock()
FPS = 60

def draw_game_over_screen(score):
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 48)

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    text = big_font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 60))

    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 120))

    global retry_button, quit_button
    retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, 180, 120, 40)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 60, 230, 120, 40)

    pygame.draw.rect(screen, GREEN, retry_button)
    pygame.draw.rect(screen, RED, quit_button)

    retry_text = font.render("Retry", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(retry_text, (retry_button.x + 30, retry_button.y + 8))
    screen.blit(quit_text, (quit_button.x + 35, quit_button.y + 8))


class Note:
    def __init__(self, x, key, color):
        self.x = x
        self.y = 0
        self.key = key
        self.color = color

    def update(self, speed):
        self.y += speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))

    def is_in_hit_zone(self):
        return HIT_ZONE_Y <= self.y <= HIT_ZONE_Y + HIT_ZONE_HEIGHT

class Game:
    def __init__(self):
        self.score = 0
        self.notes = []
        self.frame_count = 0
        self.strikes = 0
        self.game_over = False
        self.note_speed = 5


    def spawn_note(self):
        key_index = random.randint(0, len(KEYS) - 1)
        x = key_index * (SCREEN_WIDTH // len(KEYS)) + (SCREEN_WIDTH // len(KEYS) // 2) - 25
        note = Note(x, KEYS[key_index], KEY_COLORS[key_index])
        self.notes.append(note)

    def check_input(self):
        keys = pygame.key.get_pressed()
        for note in self.notes:
            if note.is_in_hit_zone() and keys[note.key]:
                self.notes.remove(note)
                self.score += 1

    def update(self):
        self.frame_count += 1
        if self.frame_count % SPAWN_RATE == 0:
            self.spawn_note()
        for note in self.notes[:]:
            note.update(self.note_speed)
            if note.y > SCREEN_HEIGHT:
                self.notes.remove(note)
                self.strikes += 1
        self.note_speed = 5 + (self.score // 10)


    def draw(self):
        screen.fill(WHITE)
        for note in self.notes:
            note.draw()
        pygame.draw.rect(screen, BLACK, (0, HIT_ZONE_Y + HIT_ZONE_HEIGHT, SCREEN_WIDTH, HIT_ZONE_HEIGHT), 2)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        strikes_text = font.render(f"Strikes: {self.strikes}/3", True, RED)
        screen.blit(strikes_text, (10, 40))


        # Draw key guide at the bottom
        for i, key in enumerate(KEYS):
            x = i * (SCREEN_WIDTH // len(KEYS)) + (SCREEN_WIDTH // len(KEYS) // 2) - 25
            color = LIGHT_KEY_COLORS[i] if pygame.key.get_pressed()[key] else KEY_COLORS[i]
            pygame.draw.rect(screen, color, (x, SCREEN_HEIGHT - 78, 50, 16))
            key_text = font.render(pygame.key.name(key).upper(), True, BLACK)
            screen.blit(key_text, (x + 15, SCREEN_HEIGHT - 82))

def main():
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if retry_button.collidepoint(mouse_x, mouse_y):
                        game = Game()  # Restart the game
                    elif quit_button.collidepoint(mouse_x, mouse_y):
                        running = False

        if not game.game_over:
            game.check_input()
            game.update()
            if game.strikes >= 3:
                game.game_over = True

        game.draw()

        if game.game_over:
            draw_game_over_screen(game.score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

