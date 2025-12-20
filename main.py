#인천원당고들학교 2025 동아리 NEXTLAB 게임 학교탈출/SchoolBreak
#Devs: @Thunderman48, @, @, @, @, @, @

import pygame

# 1. Initialize Pygame
pygame.init()

# 2. Screen setup
screen_width, screen_height = 1536, 864
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SchoolBreak")



# 3. Game variables
running = True
clock = pygame.time.Clock()
current_stage = 1
game_state = 'start_menu' # New game state manager
fade_alpha = 0 # For fade effect
fade_surface = pygame.Surface((screen_width, screen_height))
start_time = 0
final_time = 0
time_screen_start = 0

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# --- Menu Assets ---
title_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 80)
timer_font = pygame.font.Font(None, 50)

title_image = pygame.image.load('title.png').convert_alpha()
title_rect = title_image.get_rect(bottomright=(screen_width - 20, screen_height - 20))

player_image = pygame.image.load('test_image.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))

# Button positioning
y_pos = 20
start_text = button_font.render("Start", True, WHITE)
start_rect = start_text.get_rect(topleft=(20, y_pos))

y_pos += start_rect.height + 20
credits_text = button_font.render("Credits", True, WHITE)
credits_rect = credits_text.get_rect(topleft=(20, y_pos))

y_pos += credits_rect.height + 20
quit_text = button_font.render("Quit", True, WHITE)
quit_rect = quit_text.get_rect(topleft=(20, y_pos))

credits_content_text = title_font.render("Made by NEXTLAB", True, WHITE)
credits_content_rect = credits_content_text.get_rect(center=(screen_width / 2, screen_height / 2))

game_over_text = title_font.render("GAME OVER", True, BLACK)
game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))

# --- Ending Credits Assets ---
credit_names = [
    "Game Director",
    "???",
    "",
    "Lead Programmer",
    "???",
    "",
    "Character Design",
    "???",
    "",
    "Music",
    "???",
    "",
    "Sound Effects",
    "???",
    "",
    "Art",
    "???",
    "",
    "Special Thanks",
    "You!"
]
credit_renders = []

# --- Stage 1 Assets ---
table_image = pygame.image.load('tem_table.png').convert_alpha()
chair_image = pygame.image.load('tem_chair.png').convert_alpha()

stage_obstacles = {
    1: [],
    2: [],
    3: []
}

# Assuming a grid layout based on the original obstacle layout
for row in range(6):
    for col in range(5):
        # Add a table
        table_rect = table_image.get_rect(
            topleft=(
                (screen_width / 6) * (col + 0.5),
                (screen_height / 7) * (row + 1)
            )
        )
        stage_obstacles[1].append({'image': table_image, 'rect': table_rect})

        # Add a chair above the table
        chair_rect = chair_image.get_rect(
            midbottom=(
                table_rect.centerx,
                table_rect.top
            )
        )
        stage_obstacles[1].append({'image': chair_image, 'rect': chair_rect})

# Stage-specific settings
stage_backgrounds = {
    1: WHITE,
    2: (200, 200, 255), # A light blue for stage 2
    3: (200, 255, 200), # A light green for stage 3
}

# Define goals for each stage
stage_goals = {
    1: pygame.Rect(screen_width - 220, screen_height - 30, 200, 30), # Bottom-right for stage 1
    2: pygame.Rect(0, 0, 50, screen_height),                         # Left edge for stage 2
    3: pygame.Rect(20, 80, screen_width // 3, 40)                     # Top-left for stage 3, a bit wider
}
# 4. Main game loop
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False
        # Keyboard event to exit fullscreen with ESC
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # Mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == 'start_menu':
                if start_rect.collidepoint(event.pos):
                    game_state = 'game' # Start the game
                    start_time = pygame.time.get_ticks() # Start the timer
                elif credits_rect.collidepoint(event.pos):
                    game_state = 'credits' # Go to credits
                elif quit_rect.collidepoint(event.pos):
                    running = False # Quit the game
            elif game_state == 'credits':
                game_state = 'start_menu' # Click anywhere to go back
            elif game_state == 'game_over':
                # Click to go back to the main menu
                game_state = 'start_menu'
                current_stage = 1 # Reset stage

            elif game_state == 'show_time':
                # Click to proceed to credits
                game_state = 'credits_roll'
                credit_renders = []
                for i, name in enumerate(credit_names):
                    text_surf = button_font.render(name, True, WHITE)
                    text_rect = text_surf.get_rect(center=(screen_width / 2, screen_height + i * 100))
                    credit_renders.append((text_surf, text_rect))
            elif game_state == 'credits_roll':
                # Click to skip credits and go back to menu
                game_state = 'start_menu'
                credit_renders = [] # Clear credits for next time

    # --- Game Logic ---
    # Get mouse position to use as the character's position
    player_pos = pygame.mouse.get_pos()

    # Create a rect for the player for collision detection
    player_rect = pygame.Rect(player_pos[0] - 25, player_pos[1] - 25, 50, 50)

    if game_state == 'game':
        # Check for collision with obstacles
        for obstacle in stage_obstacles.get(current_stage, []):
            if isinstance(obstacle, dict):
                if player_rect.colliderect(obstacle['rect']):
                    game_state = 'game_over'
            else:
                if player_rect.colliderect(obstacle):
                    game_state = 'game_over'
        # Get the goal for the current stage
        current_goal_rect = stage_goals.get(current_stage)
        # Check if the player touches the goal area
        if current_goal_rect and current_goal_rect.collidepoint(player_pos):
            if current_stage < len(stage_backgrounds):
                current_stage += 1
            else:
                final_time = pygame.time.get_ticks() - start_time # Record final time
                game_state = 'fade_out' # Start the fade effect



    # --- Drawing ---
    if game_state == 'start_menu':
        pygame.mouse.set_visible(True)
        screen.fill(BLACK)
        # Draw title and buttons
        screen.blit(title_image, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(credits_text, credits_rect)
        screen.blit(quit_text, quit_rect)

    elif game_state == 'credits':
        pygame.mouse.set_visible(True)
        screen.fill(BLACK)
        screen.blit(credits_content_text, credits_content_rect)

    elif game_state == 'game_over':
        pygame.mouse.set_visible(True)
        screen.fill(RED)
        screen.blit(game_over_text, game_over_rect)

    elif game_state == 'fade_out':
        # Draw the last game frame
        screen.fill(stage_backgrounds.get(current_stage, WHITE))
        current_goal_rect = stage_goals.get(current_stage)
        pygame.draw.rect(screen, GREEN, current_goal_rect)
        screen.blit(player_image, player_rect)

        # Increase alpha and draw the fade surface
        fade_alpha += 4
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill(BLACK)
        screen.blit(fade_surface, (0, 0))

        # When fade is complete, switch to credits
        if fade_alpha >= 255:
            game_state = 'show_time'
            current_stage = 1 # Reset stage for next playthrough
            fade_alpha = 0 # Reset alpha for next time
            time_screen_start = pygame.time.get_ticks() # Record when the time screen appears

    elif game_state == 'show_time':
        pygame.mouse.set_visible(True)
        screen.fill(BLACK)
        # Format and display the final time
        total_seconds = final_time // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = final_time % 1000
        time_string = f"Your Time: {minutes:02}:{seconds:02}:{milliseconds:03}"
        time_surf = title_font.render(time_string, True, WHITE)
        time_rect = time_surf.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(time_surf, time_rect)

        # Automatically proceed to credits after 5 seconds
        if pygame.time.get_ticks() - time_screen_start > 5000:
            game_state = 'credits_roll'
            credit_renders = []
            for i, name in enumerate(credit_names):
                text_surf = button_font.render(name, True, WHITE)
                text_rect = text_surf.get_rect(center=(screen_width / 2, screen_height + i * 100))
                credit_renders.append((text_surf, text_rect))


    elif game_state == 'credits_roll':
        pygame.mouse.set_visible(True)
        screen.fill(BLACK)
        all_off_screen = True
        for text_surf, text_rect in credit_renders:
            # Move text up
            text_rect.y -= 1
            if text_rect.bottom > 0: # Check if the bottom of the text is still on screen
                all_off_screen = False
            screen.blit(text_surf, text_rect)
        # If all credits have scrolled past, go back to menu
        if all_off_screen and credit_renders:
            game_state = 'start_menu'
            credit_renders = [] # Clear credits

    elif game_state == 'game':
        pygame.mouse.set_visible(False)
        # Set the background color based on the current stage
        screen.fill(stage_backgrounds.get(current_stage, WHITE))

        # Draw the goal area for the current stage
        current_goal_rect = stage_goals.get(current_stage)
        pygame.draw.rect(screen, GREEN, current_goal_rect)

        # Draw the obstacles
        for obstacle in stage_obstacles.get(current_stage, []):
            if isinstance(obstacle, dict):
                screen.blit(obstacle['image'], obstacle['rect'])
            else:
                pygame.draw.rect(screen, BLACK, obstacle)

        # Draw the timer
        elapsed_time = pygame.time.get_ticks() - start_time
        total_seconds = elapsed_time // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = elapsed_time % 1000
        time_string = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
        timer_text = timer_font.render(time_string, True, BLACK)
        screen.blit(timer_text, (20, 20))

        # Draw the player at the mouse position
        screen.blit(player_image, player_rect)

    # --- Update the display ---
    pygame.display.flip()

    # --- Frame rate control ---
    clock.tick(60)  # Limit the game to 60 frames per second

# 5. Quit Pygame
pygame.quit()
