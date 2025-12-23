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

# --- Cutscene Assets ---
cutscene_images = ['tem_cut_1.png', 'tem_cut_2.png', 'tem_cut_3.png']
cutscenes = [pygame.image.load(img).convert() for img in cutscene_images]
cutscene_index = 0
CUTSCENE_DURATION = 3000  # 3 seconds
FADE_SPEED = 5
cutscene_state = 'fading_in'
cutscene_timer = 0
cutscene_fade_alpha = 255


cut_after_image = pygame.image.load('cut_after.png').convert()
cut_after_image = pygame.transform.scale(cut_after_image, (screen_width, screen_height))
cut_after_rect = pygame.Rect(17, 13, 77, 77)

# --- Menu Assets ---
title_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 80)
timer_font = pygame.font.Font(None, 50)

title_image = pygame.image.load('title_screen.png').convert()
title_image = pygame.transform.scale(title_image, (screen_width, screen_height))
title_rect = title_image.get_rect(topleft=(0, 0))

last_mouse_x = 0
player_images_right = [
    pygame.image.load('player_1.png').convert_alpha(),
    pygame.image.load('player_2.png').convert_alpha()
]
player_images_left = [
    pygame.image.load('player_3.png').convert_alpha(),
    pygame.image.load('player_4.png').convert_alpha()
]
player_images = player_images_right # Start by facing right
player_direction = 'right' # New variable to track direction

player_images_right = [pygame.transform.scale(img, (100, 140)) for img in player_images_right]
player_images_left = [pygame.transform.scale(img, (100, 140)) for img in player_images_left]
player_images = [pygame.transform.scale(img, (100, 140)) for img in player_images]
player_frame = 0
player_animation_speed = 10  # Change image every 10 frames
player_animation_timer = 0

player_image = player_images[player_frame]
player_rect = player_image.get_rect()
player_mask = pygame.mask.from_surface(player_image)

class MovingObstacle:
    def __init__(self, start_pos, end_pos, images_left, images_right):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.images_left = images_left
        self.images_right = images_right
        self.rect = self.images_left[0].get_rect(topleft=start_pos)
        self.speed = 3
        self.moving_right = True
        self.animation_frame = 0
        self.animation_speed = 15  # Slower animation
        self.animation_timer = 0
        self.image = self.images_right[0]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Movement
        if self.moving_right:
            self.rect.x += self.speed
            if self.rect.x >= self.end_pos[0]:
                self.moving_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.x <= self.start_pos[0]:
                self.moving_right = True

        # Animation
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2
            if self.moving_right:
                self.image = self.images_right[self.animation_frame]
            else:
                self.image = self.images_left[self.animation_frame]
            self.mask = pygame.mask.from_surface(self.image)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Button positioning
start_rect = pygame.Rect(30, 94, 146, 84)
credits_rect = pygame.Rect(39, 196, 129, 83)
quit_rect = pygame.Rect(44, 296, 135, 81)

credits_content_text = title_font.render("Made by NEXTLAB", True, WHITE)
credits_content_rect = credits_content_text.get_rect(center=(screen_width / 2, screen_height / 2))

default_game_over_image = pygame.image.load('death_hit.png').convert()
default_game_over_image = pygame.transform.scale(default_game_over_image, (screen_width, screen_height))
game_over_image = default_game_over_image # Set initial game over image
game_over_text = title_font.render("GAME OVER", True, BLACK)
game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))

# --- Ending Credits Assets ---
credit_names = [
    "Game Director",
    "Patrick Yang",
    "",
    "Lead Programmer",
    "Yoon Ha Ji",
    "",
    "Character Design",
    "Club Story Art",
    "",
    "Art Director",
    "Sung Hoon Choi",
    "",
    "Our Team",
    "Haeun Kim",
    "Yewon Kim",
    "Si woon Kim",
    "He Hoo Shin",
    "",
    "Art Slave 1",
    "Sung Hoon Choi"
    "",
    "Dog",
    "Rouis",
    "",
    "Special Thanks to...",
    "",
    "",
    "You!"
]
credit_renders = []

# --- Stage 1 Assets ---
stage_1_background_image = pygame.image.load('stage_1_background.png').convert()
stage_1_background_image = pygame.transform.scale(stage_1_background_image, (screen_width, screen_height))
stage_2_background_image = pygame.image.load('stage_2_bakcground.png').convert()
stage_2_background_image = pygame.transform.scale(stage_2_background_image, (screen_width, screen_height))
stage_3_background_image = pygame.image.load('stage_3_background.png').convert()
stage_3_background_image = pygame.transform.scale(stage_3_background_image, (screen_width, screen_height))
stage_4_background_image = pygame.image.load('stage_4.jpg').convert()
stage_4_background_image = pygame.transform.scale(stage_4_background_image, (screen_width, screen_height))
stage_underground_image = pygame.image.load('stage_underground.png').convert()
stage_underground_image = pygame.transform.scale(stage_underground_image, (screen_width, screen_height))
table_image = pygame.image.load('table.png').convert_alpha()
table_size = table_image.get_size()
table_image = pygame.transform.scale(table_image, (int(table_size[0] * 0.4), int(table_size[1] * 0.4)))
chair_image = pygame.image.load('chair.png').convert_alpha()
chair_size = chair_image.get_size()
chair_image = pygame.transform.scale(chair_image, (int(chair_size[0] * 0.4), int(chair_size[1] * 0.4)))
obstacle_size = (80, 80)
trash_1_image = pygame.image.load('trash_1.png').convert_alpha()
trash_1_image = pygame.transform.scale(trash_1_image, obstacle_size)
trash_2_image = pygame.image.load('trash_2.png').convert_alpha()
trash_2_image = pygame.transform.scale(trash_2_image, obstacle_size)
puddle_image = pygame.image.load('puddle.png').convert_alpha()
puddle_image = pygame.transform.scale(puddle_image, obstacle_size)
death_slip_image = pygame.image.load('death_slip.png').convert()
death_slip_image = pygame.transform.scale(death_slip_image, (screen_width, screen_height))
table_mask = pygame.mask.from_surface(table_image)
chair_mask = pygame.mask.from_surface(chair_image)
trash_1_mask = pygame.mask.from_surface(trash_1_image)
trash_2_mask = pygame.mask.from_surface(trash_2_image)
puddle_mask = pygame.mask.from_surface(puddle_image)

student_images_left = [
    pygame.transform.scale(pygame.image.load('student_1.png').convert_alpha(), (100, 140)),
    pygame.transform.scale(pygame.image.load('student_2.png').convert_alpha(), (100, 140))
]
student_images_right = [
    pygame.transform.scale(pygame.image.load('student_3.png').convert_alpha(), (100, 140)),
    pygame.transform.scale(pygame.image.load('student_4.png').convert_alpha(), (100, 140))
]

moving_obstacles = {
    1: [],
    2: [
        MovingObstacle(start_pos=(829, 700), end_pos=(1487, 700), images_left=student_images_left, images_right=student_images_right),
        MovingObstacle(start_pos=(17, 187), end_pos=(678, 187), images_left=student_images_left, images_right=student_images_right),
        MovingObstacle(start_pos=(663, 444), end_pos=(1420, 444), images_left=student_images_left, images_right=student_images_right),
        MovingObstacle(start_pos=(20, 516), end_pos=(698, 516), images_left=student_images_left, images_right=student_images_right)
    ],
    3: []
}

stage_obstacles = {
    1: [],
    2: [
        {'image': trash_1_image, 'rect': trash_1_image.get_rect(topleft=(1311,430)), 'mask': trash_1_mask, 'death_image_path': 'death_slip.png'},
        {'image': trash_2_image, 'rect': trash_2_image.get_rect(topleft=(820,656)), 'mask': trash_2_mask, 'death_image_path': 'death_slip.png'},
        {'image': puddle_image, 'rect': puddle_image.get_rect(topleft=(319,466)), 'mask': puddle_mask, 'death_image_path': 'death_slip.png'}
    ],
    3: []
}

table_coords = [
    (301, 156), (261, 679), (343, 700), (593, 451), (618, 750),
    (812, 700), (923, 241), (1175, 730), (1258, 449), (1400, 223),
    (100, 300), (100, 300), (100, 500), (1000, 100), (1000, 500), (31, 781)
]
chair_coords = [
    (187, 750), (711, 226), (1006, 700), (1394, 730), (1349, 199),
    (1430, 643), (200, 100), (200, 300), (200, 500), (1100, 100),
    (1100, 500), (118, 752), (215, 709)
]

for pos in table_coords:
    table_rect = table_image.get_rect(topleft=pos)
    stage_obstacles[1].append({'image': table_image, 'rect': table_rect, 'mask': table_mask, 'death_image_path': 'death_hit.png'})

for pos in chair_coords:
    chair_rect = chair_image.get_rect(topleft=pos)
    stage_obstacles[1].append({'image': chair_image, 'rect': chair_rect, 'mask': chair_mask, 'death_image': default_game_over_image})



# Stage-specific settings
stage_backgrounds = {
    1: stage_1_background_image,
    2: stage_2_background_image, # A light blue for stage 2
    3: stage_3_background_image,
    4: stage_4_background_image,
    5: stage_1_background_image, # Placeholder
    's-1': stage_underground_image
}

death_fall_image = pygame.image.load('death_fall.png').convert()
death_fall_image = pygame.transform.scale(death_fall_image, (screen_width, screen_height))

stage_3_game_over_zones = [
    ((589, 0), (1217, 101), (1536, 101)),
    ((0, 288), (322, 309), (1069, 441)),
    ((1069, 441), (295, 542), (0, 542)),
    ((1536, 747), (1106, 745), (503, 864))
]

stage_3_rect_fall_zones = [
    pygame.Rect(1345, 225, 140, 184) # From (1345,225) to (1485,409)
]

def point_in_triangle(pt, v1, v2, v3):
    """ Checks if a point pt is inside the triangle defined by v1, v2, and v3. """
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return ((b1 == b2) and (b2 == b3))

# Define goals for each stage
stage_goals = {
    1: [{'rect': pygame.Rect(1118, 820, 315, 45), 'dest': 2}], # Bottom-right for stage 1
    2: [{'rect': pygame.Rect(0, 0, 314, 110), 'dest': 3}],     # Left edge for stage 2
    3: [{'rect': pygame.Rect(0, 650, 10, 864), 'dest': 4}],
    4: [
        {'rect': pygame.Rect(1132, 0, 306, 23), 'dest': 5},
        {'rect': pygame.Rect(1238, 761, 298, 103), 'dest': 's-1'}
    ],
    5: [{'rect': pygame.Rect(0, 0, 10, 10), 'dest': 99}], # Win condition
    's-1': [{'rect': pygame.Rect(0, 0, 10, 10), 'dest': 99}] # Win condition
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
                    game_state = 'cutscene' # Start the cutscene
                    cutscene_index = 0
                    cutscene_state = 'fading_in'
                    cutscene_fade_alpha = 255
                    cutscene_timer = 0
                elif credits_rect.collidepoint(event.pos):
                    game_state = 'credits' # Go to credits
                elif quit_rect.collidepoint(event.pos):
                    running = False # Quit the game
            elif game_state == 'cut_after':
                if cut_after_rect.collidepoint(event.pos):
                    game_state = 'game'
                    start_time = pygame.time.get_ticks()
            elif game_state == 'credits':
                game_state = 'start_menu' # Click anywhere to go back
            elif game_state == 'cutscene':
                if cutscene_state == 'showing': # Only allow skipping when the scene is fully visible
                    cutscene_state = 'fading_out'
                    cutscene_timer = 0
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
        for obstacle in moving_obstacles.get(current_stage, []):
            obstacle.update()

        player_animation_timer += 1
        if player_animation_timer >= player_animation_speed:
            player_animation_timer = 0
            player_frame = (player_frame + 1) % len(player_images)
            player_image = player_images[player_frame]
            # Important: Update the mask with the new image
            player_mask = pygame.mask.from_surface(player_image)
        # Get mouse position to use as the character's position
        player_pos = pygame.mouse.get_pos()
        current_mouse_x = player_pos[0]
        
        if current_mouse_x < last_mouse_x and player_direction != 'left':
            player_images = player_images_left
            player_direction = 'left'
        elif current_mouse_x > last_mouse_x and player_direction != 'right':
            player_images = player_images_right
            player_direction = 'right'
        last_mouse_x = current_mouse_x

        # Create a rect for the player for collision detection, centered on the mouse
        player_rect = player_image.get_rect(center=player_pos)

        
        # Check for collision with stage 3 game over zones
        if current_stage == 3:
            # Triangular zones
            for tri in stage_3_game_over_zones:
                if point_in_triangle(player_pos, tri[0], tri[1], tri[2]):
                    game_over_image = death_fall_image
                    game_state = 'game_over'
                    break
            
            # Rectangular fall zones, only check if not already game over
            if game_state != 'game_over':
                for rect in stage_3_rect_fall_zones:
                    if player_rect.colliderect(rect):
                        game_over_image = death_fall_image
                        game_state = 'game_over'
                        break
        
        # Check for collision with obstacles
        if game_state != 'game_over':
            for obstacle in stage_obstacles.get(current_stage, []):
                collision = False
                if isinstance(obstacle, dict) and 'mask' in obstacle:
                    offset_x = obstacle['rect'].x - player_rect.x
                    offset_y = obstacle['rect'].y - player_rect.y
                    if player_mask.overlap(obstacle['mask'], (offset_x, offset_y)):
                        collision = True
                        if 'death_image_path' in obstacle:
                            game_over_image = pygame.image.load(obstacle['death_image_path']).convert()
                            game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height))
                        else:
                            game_over_image = default_game_over_image
                elif isinstance(obstacle, dict):
                    if player_rect.colliderect(obstacle['rect']):
                        collision = True
                        game_over_image = default_game_over_image
                else:
                    if player_rect.colliderect(obstacle):
                        collision = True
                        game_over_image = default_game_over_image
                
                if collision:
                    game_state = 'game_over'
                    break # Exit loop once a collision is found

        if game_state != 'game_over':
            for obstacle in moving_obstacles.get(current_stage, []):
                offset_x = obstacle.rect.x - player_rect.x
                offset_y = obstacle.rect.y - player_rect.y
                if player_mask.overlap(obstacle.mask, (offset_x, offset_y)):
                    game_over_image = default_game_over_image # Or a specific one for students
                    game_state = 'game_over'
                    break

        # Get the goal for the current stage
        current_goals = stage_goals.get(current_stage, [])
        # Check if the player touches the goal area
        for goal in current_goals:
            if player_rect.colliderect(goal['rect']):
                destination = goal['dest']
                # Check if the destination stage exists in our backgrounds dictionary
                if destination in stage_backgrounds:
                    current_stage = destination
                else:
                    # If destination doesn't exist, it's a win condition
                    final_time = pygame.time.get_ticks() - start_time
                    game_state = 'fade_out'
                break # Goal was reached, no need to check others



    # --- Drawing ---
    if game_state == 'start_menu':
        pygame.mouse.set_visible(True)
        # Draw title image
        screen.blit(title_image, title_rect)
        
        
        # The buttons are now invisible but still clickable.

    elif game_state == 'cutscene':
        pygame.mouse.set_visible(True)

        # --- Cutscene Logic ---
        if cutscene_state == 'fading_in':
            cutscene_fade_alpha -= FADE_SPEED
            if cutscene_fade_alpha <= 0:
                cutscene_fade_alpha = 0
                cutscene_state = 'showing'
                cutscene_timer = pygame.time.get_ticks()
        
        elif cutscene_state == 'showing':
            if pygame.time.get_ticks() - cutscene_timer > CUTSCENE_DURATION:
                cutscene_state = 'fading_out'

        elif cutscene_state == 'fading_out':
            cutscene_fade_alpha += FADE_SPEED
            if cutscene_fade_alpha >= 255:
                cutscene_fade_alpha = 255
                cutscene_index += 1
                if cutscene_index >= len(cutscenes):
                    game_state = 'cut_after' # Transition to the new cut_after screen
                else:
                    cutscene_state = 'fading_in'

        # --- Cutscene Drawing ---
        # Draw the current cutscene image, scaled to fit the screen
        if cutscene_index < len(cutscenes):
            cutscene_image = pygame.transform.scale(cutscenes[cutscene_index], (screen_width, screen_height))
            screen.blit(cutscene_image, (0, 0))

        # Draw the fade surface
        fade_surface.set_alpha(cutscene_fade_alpha)
        fade_surface.fill(BLACK)
        screen.blit(fade_surface, (0, 0))


    elif game_state == 'cut_after':
        pygame.mouse.set_visible(True)
        screen.blit(cut_after_image, (0, 0))

    elif game_state == 'credits':
        pygame.mouse.set_visible(True)
        screen.fill(BLACK)
        screen.blit(credits_content_text, credits_content_rect)

    elif game_state == 'game_over':
        pygame.mouse.set_visible(True)
        screen.blit(game_over_image, (0, 0))

    elif game_state == 'fade_out':
        # Draw the last game frame
        background = stage_backgrounds.get(current_stage, WHITE)
        if isinstance(background, pygame.Surface):
            screen.blit(background, (0, 0))
        else:
            screen.fill(background)
        current_goal_rect = stage_goals.get(current_stage)
        if current_stage != 1:
            # pygame.draw.rect(screen, GREEN, current_goal_rect)
            pass
        
        # Draw the obstacles
        for obstacle in stage_obstacles.get(current_stage, []):
            if isinstance(obstacle, dict):
                screen.blit(obstacle['image'], obstacle['rect'])
            else:
                pygame.draw.rect(screen, BLACK, obstacle)
        
        for obstacle in moving_obstacles.get(current_stage, []):
            obstacle.draw(screen)
        
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
        # Draw the obstacles
        for obstacle in stage_obstacles.get(current_stage, []):
            if isinstance(obstacle, dict):
                screen.blit(obstacle['image'], obstacle['rect'])
            else:
                pygame.draw.rect(screen, BLACK, obstacle)

        for obstacle in moving_obstacles.get(current_stage, []):
            obstacle.draw(screen)

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


