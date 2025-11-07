import pygame
import sys
import time
import random

pygame.init()

#music
pygame.mixer.music.load('bg music.mp3')
pygame.mixer.music.set_volume(0.5)  # range is 0.0 to 1.0
pygame.mixer.music.play(-1)

#volume for music
master_volume = 0.5
bg_music_volume = 0.5
event_volume = 0.5
audience_volume = 0.5


# screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 191)
LESS_PALE_YELLOW = (255, 255, 150)


# retro font
font = pygame.font.Font('font.otf', 40)
header_font = pygame.font.Font('font.otf', 100)
smaller_font = pygame.font.Font('font.otf', 30)

#background
loading_background = pygame.image.load('loading.png')
loading_background = pygame.transform.scale(loading_background, (screen_width, screen_height))
menu_background = pygame.image.load('menu.png')
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))
game_bg = pygame.image.load('game bg.png')
game_bg = pygame.transform.scale(game_bg, (screen_width, screen_height))

#scaling for transition images
curtain1 = pygame.image.load('menu.png')
curtain2 = pygame.image.load('transition.png')
curtain3 = pygame.image.load('no mic.png')

curtain1 = pygame.transform.scale(curtain1, (screen_width, screen_height))
curtain2 = pygame.transform.scale(curtain2, (screen_width, screen_height))
curtain3 = pygame.transform.scale(curtain3, (screen_width, screen_height))
#frames for curtain transition
curtain_frames = [
    curtain1,
    curtain2,
    curtain3
]

#loading joke bank
startup_jokes1 = [
    "Six?",
    "Y'know what else is massive?",
    "*UFO zooms past*",
    "Why was the math book sad?",
    "Why did the chicken cross the road?"
]

startup_jokes2 = [
    "Seven!",
    "Low taper fade.",
    "Oh my god, did you see that!",
    "Because it had too many problems.",
    "To get to the other side!"
]

#sliders for volume
def draw_slider(x, y, width, height, value, label):
    # Draw label
    text = smaller_font.render(f"{label}: {int(value * 100)}%", True, YELLOW)
    screen.blit(text, (x, y - 40))
    
    # Slider bar
    pygame.draw.rect(screen, YELLOW, (x, y, width, height), 3)
    
    # Handle position
    handle_x = x + int(value * width)
    pygame.draw.circle(screen, YELLOW, (handle_x, y + height // 2), 10)

    # Return handle rect (for mouse detection)
    return pygame.Rect(handle_x - 10, y, 20, height)

# select random joke
joke_index = random.randint(0, len(startup_jokes1) - 1)
selected_joke = startup_jokes1[joke_index]
selected_joke2 = startup_jokes2[joke_index]

# loading screen
def loading_screen():
    dots = 0
    update_time = time.time()

    start_time = time.time()
    runtimer = True

    while runtimer:
        screen.blit(loading_background, (0, 0))
        if time.time() - update_time >= 0.5:
            dots = (dots + 1) % 4
            update_time = time.time()
            
        loading_text = font.render("Loading" + ("." * dots), True, YELLOW)
        loading_joke = smaller_font.render(selected_joke, True, YELLOW)

        text_w = screen_width // 2 - loading_text.get_width() // 2
        text_h = (screen_height * 4) // 5 - loading_text.get_height() // 2
        joke_w = screen_width // 2 - loading_joke.get_width() // 2
        joke_h = (screen_height * 7) // 8 - loading_joke.get_height() // 2

        screen.blit(loading_text, (text_w, text_h))
        screen.blit(loading_joke, (joke_w, joke_h))

        pygame.display.flip()

        if time.time() - start_time >= 6:
            runtimer = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# function for actual button
def draw_button(text, x, y, width, height, inactive_colour, active_colour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    #check if the mouse hovering, then change the mouse colour
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=((x + (width / 2), (y + (height / 2)))))
    screen.blit(text_surface, text_rect)

#function for text that acts as a button
def text_button(text, x, y, font, colour, hover_colour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(center=(x, y))

    # check hover
    if text_rect.collidepoint(mouse):
        text_surface = font.render(text, True, hover_colour)
        # detect left click
        if click[0] == 1 and action is not None:
            pygame.time.delay(150)  # small delay to prevent multiple triggers
            action()  # <-- actually calls the function here

    screen.blit(text_surface, text_rect)

#function for transition screen using curtains
def curtain_transition(next_screen):
    # Closing
    for frame in curtain_frames:
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500)  # controls the speed

    # Opening (reverse order)
    for frame in reversed(curtain_frames):
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500)

    # Switch to the new scene
    next_screen()

    # Closing
    for frame in curtain_frames:
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500)  # controls the speed

    # Opening (reverse order)
    for frame in reversed(curtain_frames):
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.delay(500)

def main_menu():
    menu_running = True
    while menu_running:
        screen.blit(menu_background, (0, 0))

        menu_text = header_font.render("Main Menu", True, YELLOW)
        menu_joke = smaller_font.render(selected_joke2, True, YELLOW)

        #title position on screen
        title_w = screen_width // 2 - menu_text.get_width() // 2
        title_h = screen_height // 4 - menu_text.get_height() // 2

        #button positions on screen
        text_button("Play", screen_width//2, screen_height * 2//4, font, YELLOW, LESS_PALE_YELLOW, play_game)
        text_button("Tutorial", screen_width//2, screen_height * 2.5//4, font, YELLOW, LESS_PALE_YELLOW, tutorial)
        text_button("Settings", screen_width//2, screen_height * 3//4, font, YELLOW, LESS_PALE_YELLOW, lambda: curtain_transition(settings))
        

        joke_w = screen_width // 2 - menu_joke.get_width() // 2
        joke_h = (screen_height * 7) // 8 - menu_joke.get_height() // 2

        screen.blit(menu_text, (title_w, title_h))
        screen.blit(menu_joke, (joke_w, joke_h)) 
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

def play_game():
    gameplay_running = True

    player_img = pygame.image.load('player.png')
    player_sprite = pygame.transform.scale(player_img, (50, 50))
    player_x = screen_width // 2 - 25
    player_y = screen_height - 100

    
    while gameplay_running:
        screen.blit(game_bg, (0, 0))

        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False




def tutorial():
    print("Tutorial button clicked")

def settings():
    global master_volume, bg_music_volume, event_music_volume, audience_volume

    dragging = None
    settings_running = True
    slider_width = 300
    slider_height = 10
    slider_x = screen_width // 2 - slider_width // 2  # center horizontally

    while settings_running:
        screen.blit(menu_background, (0, 0))

        # title + back button
        settings_text = header_font.render("Settings", True, YELLOW)
        back_text = smaller_font.render("Back", True, YELLOW)

        title_w = screen_width // 2 - settings_text.get_width() // 2
        title_h = 60
        back_w = 20
        back_h = 20

        screen.blit(settings_text, (title_w, title_h))
        screen.blit(back_text, (back_w, back_h))

        #draw sliders 
        bg_rect = draw_slider(slider_x, 250, slider_width, slider_height, bg_music_volume, "Background Music")
        event_rect = draw_slider(slider_x, 350, slider_width, slider_height, event_volume, "Event Music")
        audience_rect = draw_slider(slider_x, 450, slider_width, slider_height, audience_volume, "Audience")
        master_rect = draw_slider(slider_x, 550, slider_width, slider_height, master_volume, "Master Volume")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                back_rect = back_text.get_rect(topleft=(back_w, back_h))
                if back_rect.collidepoint(mouse_x, mouse_y):
                    settings_running = False  # go back

                elif bg_rect.collidepoint(mouse_x, mouse_y):
                    dragging = 'bg'
                elif event_rect.collidepoint(mouse_x, mouse_y):
                    dragging = 'event'
                elif audience_rect.collidepoint(mouse_x, mouse_y):
                    dragging = 'audience'
                elif master_rect.collidepoint(mouse_x, mouse_y):
                    dragging = 'master'

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x = event.pos[0]
                rel_x = max(0, min(mouse_x - slider_x, slider_width)) / slider_width
                if dragging == 'bg':
                    bg_music_volume = rel_x
                    pygame.mixer.music.set_volume(bg_music_volume * master_volume)
                elif dragging == 'event':
                    event_music_volume = rel_x
                elif dragging == 'audience':
                    audience_volume = rel_x
                elif dragging == 'master':
                    master_volume = rel_x
                    pygame.mixer.music.set_volume(bg_music_volume * master_volume)

loading_screen()
main_menu()
pygame.quit()
sys.exit()
