import pygame
import sys

pygame.init()

# Ablak mérete és cím beállítása
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Beállítások")

# Színek definiálása
background_color = (30, 30, 30)
text_color = (255, 255, 255)
button_color = (50, 50, 50)
button_hover_color = (70, 70, 70)

# Fontok létrehozása
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Játékbeállítások kezdeti értékei
game_settings = {
    'game_speed': 75,
    'difficulty': 'Normál'
}

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_settings_menu():
    running = True

    speed_text = font_medium.render(f"Sebesség: {game_settings['game_speed']}", True, text_color)
    difficulty_text = font_medium.render(f"Nehézség: {game_settings['difficulty']}", True, text_color)

    while running:
        screen.fill(background_color)

        draw_text("Beállítások", font_large, text_color, width // 2, height // 4)

        # Sebesség beállítása gombokkal
        speed_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 50)
        pygame.draw.rect(screen, button_color, speed_rect)
        pygame.draw.rect(screen, text_color, speed_rect, 2)
        screen.blit(speed_text, speed_rect.move(10, 10))

        # Nehézség beállítása gombokkal
        difficulty_rect = pygame.Rect(width // 2 - 150, height // 2 + 50, 300, 50)
        pygame.draw.rect(screen, button_color, difficulty_rect)
        pygame.draw.rect(screen, text_color, difficulty_rect, 2)
        screen.blit(difficulty_text, difficulty_rect.move(10, 10))

        # Mentés gomb
        save_rect = pygame.Rect(width // 2 - 100, height // 2 + 150, 200, 50)
        pygame.draw.rect(screen, button_color, save_rect)
        pygame.draw.rect(screen, text_color, save_rect, 2)
        draw_text("Mentés", font_medium, text_color, save_rect.centerx, save_rect.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Sebesség gomb interakció
                if speed_rect.collidepoint(mouse_pos):
                    game_settings['game_speed'] = max(10, min(100, game_settings['game_speed'] + 10))  # Min 10, max 100
                    speed_text = font_medium.render(f"Sebesség: {game_settings['game_speed']}", True, text_color)

                # Nehézség gomb interakció
                elif difficulty_rect.collidepoint(mouse_pos):
                    difficulties = ['Könnyű', 'Normál', 'Nehéz']
                    current_index = difficulties.index(game_settings['difficulty'])
                    game_settings['difficulty'] = difficulties[(current_index + 1) % len(difficulties)]
                    difficulty_text = font_medium.render(f"Nehézség: {game_settings['difficulty']}", True, text_color)

                # Mentés gomb interakció
                elif save_rect.collidepoint(mouse_pos):
                    save_settings()
                    print("Beállítások mentve!")
                    return  # Visszatérés a fő ciklushoz (main függvény)

def save_settings():
    # Játékbeállítások mentése egy fájlba
    with open('game_settings.txt', 'w') as file:
        file.write(f"game_speed={game_settings['game_speed']}\n")
        file.write(f"difficulty={game_settings['difficulty']}\n")

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    draw_settings_menu()

        screen.fill(background_color)
        draw_text("Nyomd meg az 's' billentyűt a beállítások megjelenítéséhez", font_medium, text_color, width // 2, height // 2)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
