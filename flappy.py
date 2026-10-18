import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_JUMP = -6
INITIAL_PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500 # milliseconds

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0.0
        self.radius = 15
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.centery = self.y

    def jump(self):
        self.velocity = BIRD_JUMP

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.top_rect = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, 50, SCREEN_HEIGHT - (self.height + PIPE_GAP))
        self.passed = False

    def update(self, speed):
        self.x -= speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def main():
    bird = Bird()
    pipes = []
    score = 0
    high_score = load_high_score()
    last_pipe_time = pygame.time.get_ticks()
    game_active = False
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True
                        game_active = True
                        bird.jump()
                    elif game_active:
                        bird.jump()
                    else:
                        # Reset Game
                        bird = Bird()
                        pipes = []
                        score = 0
                        game_active = True
                        last_pipe_time = pygame.time.get_ticks()

        screen.fill(BLUE)

        if not game_started:
            # Start Screen
            start_text = font.render("FLAPPY BIRD", True, WHITE)
            hint_text = font.render("Press SPACE to Start", True, BLACK)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        elif game_active:
            # Calculate current pipe speed based on score
            current_pipe_speed = INITIAL_PIPE_SPEED + (score // 5) * 0.5

            # Bird logic
            bird.update()
            bird.draw()

            # Pipe logic
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_time > PIPE_FREQUENCY:
                pipes.append(Pipe(SCREEN_WIDTH))
                last_pipe_time = current_time

            for pipe in pipes[:]:
                pipe.update(current_pipe_speed)
                pipe.draw()

                # Collision detection
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    game_active = False

                # Score tracking
                if not pipe.passed and pipe.x < bird.x:
                    score += 1
                    pipe.passed = True

                # Remove off-screen pipes
                if pipe.x < -50:
                    pipes.remove(pipe)

            # Screen boundary collision
            if bird.y <= 0 or bird.y >= SCREEN_HEIGHT:
                game_active = False

            # Draw score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        else:
            # Game Over Screen
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press SPACE to Restart", True, BLACK)
            score_final = font.render(f"Score: {score}", True, BLACK)
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            
            screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(score_final, (SCREEN_WIDTH // 2 - score_final.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
