import pygame
import os
import random

# Define colors
WHITE = (255, 255, 255)

# New global variables for the timer, treats eaten, and distance covered
start_time = pygame.time.get_ticks()  # Get the initial time
treats_eaten = 0
distance_covered = 0
pygame.font.init()

# Constants
VEL = 5
GRAVITY = 0.5  # Gravity value to simulate falling
JUMP_VEL = 10  # Initial jump velocity
FPS = 60
DOG_WIDTH, DOG_HEIGHT = 200, 170
GRASS_WIDTH, GRASS_HEIGHT = 900, 300
PUPTREAT_WIDTH, PUPTREAT_HEIGHT = 50, 45

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images
PUP_IMAGE = pygame.image.load(os.path.join('puprun.png'))
PUP = pygame.transform.flip(pygame.transform.scale(PUP_IMAGE, (DOG_WIDTH, DOG_HEIGHT)), 1, 0)

GRASS_IMAGE = pygame.image.load(os.path.join('grass.png'))
GRASS = pygame.transform.scale(GRASS_IMAGE, (GRASS_WIDTH, GRASS_HEIGHT))

PUPTREAT_IMAGE = pygame.image.load(os.path.join('dogtreat.png'))
PUPTREAT = pygame.transform.scale(PUPTREAT_IMAGE, (PUPTREAT_WIDTH, PUPTREAT_HEIGHT))
pygame.display.set_caption("Pet game")

# Functions to manage highscores
HIGHSCORE_FILE = "highscores.txt"


def get_highscores():
    try:
        with open(HIGHSCORE_FILE, "r") as file:
            highscores = [int(score) for score in file.readlines()]
            highscores.sort(reverse=True)
            return highscores[:5]  # Return top 5 highscores
    except FileNotFoundError:
        return []


def save_highscore(score):
    highscores = get_highscores()
    highscores.append(score)
    highscores.sort(reverse=True)
    highscores = highscores[:5]  # Keep only the top 5 scores

    with open(HIGHSCORE_FILE, "w") as file:
        file.write("\n".join(str(score) for score in highscores))


def draw_highscores():
    highscores = get_highscores()
    font = pygame.font.SysFont(None, 30)
    y_pos = 50  # Initial Y position for highscore display
    header = font.render("Highscores:", True, (0, 0, 0))
    WIN.blit(header, (10, 10))

    for index, score in enumerate(highscores, start=1):
        score_text = font.render(f"{index}. {score}", True, (0, 0, 0))
        WIN.blit(score_text, (10, y_pos))
        y_pos += 30  # Increase Y position for the next score


# Draw the game window
def draw_window(brown, green1, green2, yellow1, yellow2):
    WIN.fill(WHITE)
    WIN.blit(PUP, (brown.x, brown.y))
    WIN.blit(GRASS, (green1.x, green1.y))
    WIN.blit(GRASS, (green2.x, green2.y))

    # Only draw the treats if they are visible (not eaten)
    if yellow1.x > -PUPTREAT_WIDTH:
        WIN.blit(PUPTREAT, (yellow1.x, yellow1.y))
    if yellow2.x > -PUPTREAT_WIDTH:
        WIN.blit(PUPTREAT, (yellow2.x, yellow2.y))

    # Draw the counters
    draw_counters()
    pygame.display.update()


# Check collision between dog and treats
def check_collision(brown, yellow1, yellow2):
    global treats_eaten
    if brown.colliderect(yellow1):
        reset_treat(yellow1)
        update_counters()
    if brown.colliderect(yellow2):
        reset_treat(yellow2)
        update_counters()


# Move the dog based on key presses
def pup_movement(keys_pressed, brown):
    if keys_pressed[pygame.K_a] and brown.x - VEL > 0:  # left
        brown.x -= VEL
    if keys_pressed[pygame.K_d] and brown.x + VEL < 700:  # right
        brown.x += VEL


# Set maximum jump height for treats
MAX_JUMP_HEIGHT = 150


# Reset treat position
def reset_treat(treat):
    treat.x = WIDTH + random.randint(100, 500)
    treat.y = random.randint(310 - MAX_JUMP_HEIGHT, 310)


# Draw the pause screen
def draw_pause_screen():
    pause_surface = pygame.Surface((WIDTH, HEIGHT))
    pause_surface.set_alpha(128)
    pause_surface.fill((0, 0, 0))

    font = pygame.font.SysFont(None, 48)
    text = font.render("Paused", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pause_surface.blit(text, text_rect)

    # Draw the highscores on the pause screen
    draw_highscores()
    WIN.blit(pause_surface, (0, 0))
    pygame.display.update()


# Update treat counters
def update_counters():
    global treats_eaten
    treats_eaten += 1
    save_highscore(treats_eaten)


# Draw treat counters
def draw_counters():
    font = pygame.font.SysFont(None, 30)
    treats_text = font.render(f"Treats: {treats_eaten}", True, (0, 0, 0))
    WIN.blit(treats_text, (10, 10))


# Main function to run the game
def main():
    pygame.mixer.init()
    pygame.mixer.music.load('Backgroundmusic.wav')
    pygame.mixer.music.play(-1)

    brown = pygame.Rect(100, 310, DOG_WIDTH, DOG_HEIGHT)
    green1 = pygame.Rect(0, 310, GRASS_WIDTH, GRASS_HEIGHT)
    green2 = pygame.Rect(900, 310, GRASS_WIDTH, GRASS_HEIGHT)
    yellow1 = pygame.Rect(400, 410, PUPTREAT_WIDTH, PUPTREAT_HEIGHT)
    yellow2 = pygame.Rect(900, 400, PUPTREAT_WIDTH, PUPTREAT_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    grass_speed = 1
    jumping = False
    jump_vel = JUMP_VEL
    paused = False

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not jumping:
                    jumping = True
                    jump_vel = JUMP_VEL
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused

        if not paused:
            if jumping:
                brown.y -= jump_vel
                jump_vel -= GRAVITY

                if brown.y >= 310:
                    jumping = False
                    brown.y = 310

            yellow1.x -= 1
            yellow2.x -= 1
            green1.x -= grass_speed
            green2.x -= grass_speed

            if green1.right <= 0:
                green1.x = green2.right
            if green2.right <= 0:
                green2.x = green1.right

            if yellow1.right <= 0:
                reset_treat(yellow1)
            if yellow2.right <= 0:
                reset_treat(yellow2)

            check_collision(brown, yellow1, yellow2)

            keys_pressed = pygame.key.get_pressed()
            pup_movement(keys_pressed, brown)
            draw_window(brown, green1, green2, yellow1, yellow2)
        else:
            draw_pause_screen()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
