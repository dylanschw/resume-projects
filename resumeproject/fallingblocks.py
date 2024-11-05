import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Falling Blocks!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Item color

# Default player customization settings
player_color = (0, 0, 255)  # Blue
player_size = 50
player_speed = 7
pickup_buffer = 10  # Buffer to make the pickup area larger

# Game settings
item_size = 30
initial_item_speed = 3
min_spacing = 60
max_level_items = 10
level = 1

# Font for displaying text
font = pygame.font.SysFont("monospace", 35)

# Function to detect collision with a buffer zone
def detect_collision(player_pos, obj_pos, obj_size, buffer=0):
    p_x, p_y = player_pos
    o_x, o_y = obj_pos
    expanded_player_size = player_size + buffer

    if (o_x < p_x < o_x + obj_size or o_x < p_x + expanded_player_size < o_x + obj_size) and \
       (o_y < p_y < o_y + obj_size or o_y < p_y + expanded_player_size < o_y + obj_size):
        return True
    return False

# Function to create items with minimum spacing
def create_items(count, size, speed, spacing):
    items = []
    for _ in range(count):
        while True:
            item_pos = [random.randint(0, WIDTH - size), 0]
            if all(abs(item_pos[0] - other['pos'][0]) > spacing for other in items):
                items.append({'pos': item_pos, 'speed': speed})
                break
    return items

# Main menu function
def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Collect the Items Game", True, WHITE)
        start_text = font.render("Press S to Start", True, WHITE)
        customize_text = font.render("Press C to Customize", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(customize_text, (WIDTH // 2 - customize_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Start game
                    main_game()
                elif event.key == pygame.K_c:  # Customize player
                    customize_player()
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    sys.exit()

# Customization menu function
def customize_player():
    global player_color, player_speed, player_size
    while True:
        screen.fill(BLACK)
        color_text = font.render("Press 1 for Blue, 2 for Red, 3 for Green", True, WHITE)
        speed_text = font.render("Press UP/DOWN to change Speed: " + str(player_speed), True, WHITE)
        size_text = font.render("Press LEFT/RIGHT to change Size: " + str(player_size), True, WHITE)
        back_text = font.render("Press B to Go Back", True, WHITE)

        screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, HEIGHT // 2 - 150))
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(size_text, (WIDTH // 2 - size_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_color = (0, 0, 255)  # Blue
                elif event.key == pygame.K_2:
                    player_color = (255, 0, 0)  # Red
                elif event.key == pygame.K_3:
                    player_color = (0, 255, 0)  # Green
                elif event.key == pygame.K_UP:
                    player_speed += 1
                elif event.key == pygame.K_DOWN and player_speed > 1:
                    player_speed -= 1
                elif event.key == pygame.K_RIGHT:
                    player_size += 5
                elif event.key == pygame.K_LEFT and player_size > 10:
                    player_size -= 5
                elif event.key == pygame.K_b:  # Go back to main menu
                    return

# Pause menu function
def pause_menu():
    while True:
        screen.fill(BLACK)
        pause_text = font.render("Game Paused", True, WHITE)
        resume_text = font.render("Press R to Resume", True, WHITE)
        restart_text = font.render("Press T to Restart", True, WHITE)
        main_menu_text = font.render("Press M for Main Menu", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 150))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(main_menu_text, (WIDTH // 2 - main_menu_text.get_width() // 2, HEIGHT // 2 + 150))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume game
                    return
                elif event.key == pygame.K_t:  # Restart game
                    main_game()
                elif event.key == pygame.K_m:  # Go to main menu
                    main_menu()
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    sys.exit()

# Main game function
def main_game():
    global level

    # Initialize player and game variables
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    items = create_items(level + 1, item_size, initial_item_speed, min_spacing)
    score = 0
    game_over = False
    clock = pygame.time.Clock()

    max_item_speed = 8  # Maximum allowable item speed

    # Main game loop
    while not game_over:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game
                    pause_menu()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

        # Update item positions and check for collisions
        for item in items:
            item['pos'][1] += item['speed']
            if item['pos'][1] > HEIGHT:
                game_over = True  # Game over if an item reaches the bottom

            if detect_collision(player_pos, item['pos'], item_size, buffer=pickup_buffer):
                score += 1
                # Reset item to a random position at the top
                item['pos'] = [random.randint(0, WIDTH - item_size), 0]

        # Level up and increase difficulty
        if score >= level * 10:
            level += 1
            # Calculate new item speed but cap it at max_item_speed
            item_speed = min(initial_item_speed + level - 1, max_item_speed)
            item_count = min(level + 1, max_level_items)
            items = create_items(item_count, item_size, item_speed, min_spacing)

        # Draw player and items
        pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))
        for item in items:
            pygame.draw.rect(screen, GREEN, (item['pos'][0], item['pos'][1], item_size, item_size))

        # Display score and level
        score_text = font.render("Score: " + str(score), True, WHITE)
        level_text = font.render("Level: " + str(level), True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        pygame.display.update()
        clock.tick(30)


# Start with the main menu
main_menu()
