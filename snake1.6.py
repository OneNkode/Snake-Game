import pygame
import sys
import random

pygame.init()

# Window size and title
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Modern Snake Game")

# Colors
background_color = (30, 30, 30)
text_color = (255, 255, 255)
button_color = (50, 50, 50)
button_hover_color = (70, 70, 70)
snake_color = (0, 255, 0)
food_color = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Initial game settings
game_settings = {
    'game_speed': 10,
    'difficulty': 'Normal',
    'music_volume': 5,
    'sound_effects_volume': 5,
    'controls': 'Arrow Keys'
}

# Functions to handle settings options cycling
def cycle_value(options, current_value):
    current_index = options.index(current_value)
    return options[(current_index + 1) % len(options)]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, font, rect, is_hover):
    color = button_hover_color if is_hover else button_color
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, text_color, rect, 2)
    draw_text(text, font, text_color, rect.centerx, rect.centery)

def draw_settings_menu():
    running = True

    # Define setting options
    difficulties = ['Easy', 'Normal', 'Hard']
    control_options = ['Arrow Keys', 'WASD', 'Custom']

    while running:
        screen.fill(background_color)

        draw_text("Settings", font_large, text_color, width // 2, height // 6)

        # Define button rects
        speed_rect = pygame.Rect(width // 2 - 150, height // 3 - 20, 300, 40)
        difficulty_rect = pygame.Rect(width // 2 - 150, height // 3 + 50, 300, 40)
        music_vol_rect = pygame.Rect(width // 2 - 150, height // 3 + 120, 300, 40)
        sound_vol_rect = pygame.Rect(width // 2 - 150, height // 3 + 190, 300, 40)
        controls_rect = pygame.Rect(width // 2 - 150, height // 3 + 260, 300, 40)
        save_rect = pygame.Rect(width // 2 - 100, height // 3 + 350, 200, 50)

        # Draw setting buttons
        draw_button(f"Speed: {game_settings['game_speed']}", font_medium, speed_rect, speed_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(f"Difficulty: {game_settings['difficulty']}", font_medium, difficulty_rect, difficulty_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(f"Music Volume: {game_settings['music_volume']}", font_medium, music_vol_rect, music_vol_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(f"Sound Effects: {game_settings['sound_effects_volume']}", font_medium, sound_vol_rect, sound_vol_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(f"Controls: {game_settings['controls']}", font_medium, controls_rect, controls_rect.collidepoint(pygame.mouse.get_pos()))

        # Draw save button
        draw_button("Save and Back", font_medium, save_rect, save_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Speed button interaction
                if speed_rect.collidepoint(mouse_pos):
                    game_settings['game_speed'] = max(1, min(30, game_settings['game_speed'] + 1))

                # Difficulty button interaction
                elif difficulty_rect.collidepoint(mouse_pos):
                    game_settings['difficulty'] = cycle_value(difficulties, game_settings['difficulty'])

                # Music volume button interaction
                elif music_vol_rect.collidepoint(mouse_pos):
                    game_settings['music_volume'] = (game_settings['music_volume'] + 1) % 11

                # Sound effects volume button interaction
                elif sound_vol_rect.collidepoint(mouse_pos):
                    game_settings['sound_effects_volume'] = (game_settings['sound_effects_volume'] + 1) % 11

                # Controls button interaction
                elif controls_rect.collidepoint(mouse_pos):
                    game_settings['controls'] = cycle_value(control_options, game_settings['controls'])

                # Save button interaction
                elif save_rect.collidepoint(mouse_pos):
                    save_settings()
                    return  # Return to main menu

def save_settings():
    # Save game settings to a file
    with open('game_settings.txt', 'w') as file:
        for key, value in game_settings.items():
            file.write(f"{key}={value}\n")

def load_settings():
    try:
        with open('game_settings.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                if key == 'game_speed':
                    game_settings[key] = int(value)
                elif key in ['music_volume', 'sound_effects_volume']:
                    game_settings[key] = int(value)
                else:
                    game_settings[key] = value
    except FileNotFoundError:
        pass  # No settings file found, use default settings

def play_snake():
    block_size = 20
    snake = [(width // 2, height // 2)]
    snake_dir = (0, -block_size)
    food_pos = (random.randint(0, (width - block_size) // block_size) * block_size,
                random.randint(0, (height - block_size) // block_size) * block_size)
    clock = pygame.time.Clock()
    score = 0
    running = True

    def check_collision(pos1, pos2):
        return pos1[0] == pos2[0] and pos1[1] == pos2[1]

    while running:
        screen.fill(background_color)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit to main menu
                elif event.key == pygame.K_UP and snake_dir[1] == 0:
                    snake_dir = (0, -block_size)
                elif event.key == pygame.K_DOWN and snake_dir[1] == 0:
                    snake_dir = (0, block_size)
                elif event.key == pygame.K_LEFT and snake_dir[0] == 0:
                    snake_dir = (-block_size, 0)
                elif event.key == pygame.K_RIGHT and snake_dir[0] == 0:
                    snake_dir = (block_size, 0)

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

        if new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height or new_head in snake:
            return  # Game over, exit to main menu

        if check_collision(new_head, food_pos):
            score += 1
            food_pos = (random.randint(0, (width - block_size) // block_size) * block_size,
                        random.randint(0, (height - block_size) // block_size) * block_size)
        else:
            snake.pop()

        snake.insert(0, new_head)

        for segment in snake:
            pygame.draw.rect(screen, snake_color, (*segment, block_size, block_size))
        pygame.draw.rect(screen, food_color, (*food_pos, block_size, block_size))

        draw_text(f"Score: {score}", font_small, text_color, width // 2, 20)
        pygame.display.flip()
        clock.tick(game_settings['game_speed'])  # Dynamic game speed

def main():
    load_settings()
    running = True

    # Button rectangles
    play_rect = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 50)
    settings_rect = pygame.Rect(width // 2 - 100, height // 2 + 20, 200, 50)
    quit_rect = pygame.Rect(width // 2 - 100, height // 2 + 90, 200, 50)

    while running:
        screen.fill(background_color)
        draw_text("Snake Game", font_large, text_color, width // 2, height // 4)

        # Draw buttons
        draw_button("Play", font_medium, play_rect, play_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button("Settings", font_medium, settings_rect, settings_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button("Quit", font_medium, quit_rect, quit_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if play_rect.collidepoint(mouse_pos):
                    play_snake()
                elif settings_rect.collidepoint(mouse_pos):
                    draw_settings_menu()
                elif quit_rect.collidepoint(mouse_pos):
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()

icon = pygame.image.load('icon.ico')  # Load your icon image
pygame.display.set_icon(icon)  # Set the icon for the window