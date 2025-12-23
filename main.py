#인천원당고들학교 2025 동아리 NEXTLAB 게임 학교탈출/SchoolBreak
#Devs: @Thunderman48, @he8834-dev, @, @, @, @, @

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

title_image = pygame.image.load('title_screen.png').convert()
title_image = pygame.transform.scale(title_image, (screen_width, screen_height))
title_rect = title_image.get_rect(topleft=(0, 0))

player_images = [
    pygame.image.load('player_1.png').convert_alpha(),
    pygame.image.load('player_2.png').convert_alpha()
]
player_images = [pygame.transform.scale(img, (50, 70)) for img in player_images]
player_frame = 0
player_animation_speed = 10  # Change image every 10 frames
player_animation_timer = 0

player_image = player_images[player_frame]
player_rect = player_image.get_rect()
player_mask = pygame.mask.from_surface(player_image)

# Button positioning
start_rect = pygame.Rect(30, 94, 146, 84)
credits_rect = pygame.Rect(39, 196, 129, 83)
quit_rect = pygame.Rect(44, 296, 135, 81)

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
stage_1_background_image = pygame.image.load('stage_1_background.png').convert()
stage_1_background_image = pygame.transform.scale(stage_1_background_image, (screen_width, screen_height))
table_image = pygame.image.load('tem_table.png').convert_alpha()
chair_image = pygame.image.load('tem_chair.png').convert_alpha()
table_mask = pygame.mask.from_surface(table_image)
chair_mask = pygame.mask.from_surface(chair_image)

stage_obstacles = {
    1: [],
    2: [],
    3: []
}

table_coords = [
    (301, 156), (261, 679), (343, 700), (593, 451), (618, 750),
    (812, 700), (923, 241), (1175, 730), (1258, 449), (1400, 223),
    (100, 300), (100, 300), (100, 500), (1000, 100), (1000, 500)
]
chair_coords = [
    (187, 750), (711, 226), (1006, 700), (1394, 730), (1349, 199),
    (1430, 643), (200, 100), (200, 300), (200, 500), (1100, 100),
    (1100, 500)
]

for pos in table_coords:
    table_rect = table_image.get_rect(topleft=pos)
    stage_obstacles[1].append({'image': table_image, 'rect': table_rect, 'mask': table_mask})

for pos in chair_coords:
    chair_rect = chair_image.get_rect(topleft=pos)
    stage_obstacles[1].append({'image': chair_image, 'rect': chair_rect, 'mask': chair_mask})

# Stage-specific settings
stage_backgrounds = {
    1: stage_1_background_image,
    2: (200, 200, 255), # A light blue for stage 2
    3: (200, 255, 200), # A light green for stage 3
}

# Define goals for each stage
stage_goals = {
    1: pygame.Rect(1118, 820, 315, 45), # Bottom-right for stage 1
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
    if game_state == 'game':
        player_animation_timer += 1
        if player_animation_timer >= player_animation_speed:
            player_animation_timer = 0
            player_frame = (player_frame + 1) % len(player_images)
            player_image = player_images[player_frame]
            # Important: Update the mask with the new image
            player_mask = pygame.mask.from_surface(player_image)
        # Get mouse position to use as the character's position
        player_pos = pygame.mouse.get_pos()

        # Create a rect for the player for collision detection, centered on the mouse
        player_rect = player_image.get_rect(center=player_pos)

        # Check for collision with obstacles
        for obstacle in stage_obstacles.get(current_stage, []):
            if isinstance(obstacle, dict) and 'mask' in obstacle:
                offset_x = obstacle['rect'].x - player_rect.x
                offset_y = obstacle['rect'].y - player_rect.y
                if player_mask.overlap(obstacle['mask'], (offset_x, offset_y)):
                    game_state = 'game_over'
            elif isinstance(obstacle, dict):
                if player_rect.colliderect(obstacle['rect']):
                    game_state = 'game_over'
            else:
                if player_rect.colliderect(obstacle):
                    game_state = 'game_over'
        # Get the goal for the current stage
        current_goal_rect = stage_goals.get(current_stage)
        # Check if the player touches the goal area
        if current_goal_rect and player_rect.colliderect(current_goal_rect):
            if current_stage < len(stage_backgrounds):
                current_stage += 1
            else:
                final_time = pygame.time.get_ticks() - start_time # Record final time
                game_state = 'fade_out' # Start the fade effect



    # --- Drawing ---
    if game_state == 'start_menu':
        pygame.mouse.set_visible(True)
        # Draw title image
        screen.blit(title_image, title_rect)
        
        
        # The buttons are now invisible but still clickable.

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
        background = stage_backgrounds.get(current_stage, WHITE)
        if isinstance(background, pygame.Surface):
            screen.blit(background, (0, 0))
        else:
            screen.fill(background)
        current_goal_rect = stage_goals.get(current_stage)
        pygame.draw.rect(screen, GREEN, current_goal_rect)
        
        # Draw the obstacles
        for obstacle in stage_obstacles.get(current_stage, []):
            if isinstance(obstacle, dict):
                screen.blit(obstacle['image'], obstacle['rect'])
            else:
                pygame.draw.rect(screen, BLACK, obstacle)
        
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
        background = stage_backgrounds.get(current_stage, WHITE)
        if isinstance(background, pygame.Surface):
            screen.blit(background, (0, 0))
        else:
            screen.fill(background)

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


