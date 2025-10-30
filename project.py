import pygame
import sys
import time
import random

pygame.init()

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

    if text_rect.collidepoint(mouse):
        text_surface = font.render(text, True, hover_colour)
        if click[0] == 1 and action is not None:
            return True

    screen.blit(text_surface, text_rect)

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
        text_button("Settings", screen_width//2, screen_height * 3//4, font, YELLOW, LESS_PALE_YELLOW, settings)
        

        joke_w = screen_width // 2 - menu_joke.get_width() // 2
        joke_h = (screen_height * 7) // 8 - menu_joke.get_height() // 2

        screen.blit(menu_text, (title_w, title_h))
        screen.blit(menu_joke, (joke_w, joke_h)) 
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

def play_game():
    print("Play Game button clicked")

def tutorial():
    print("Tutorial button clicked")

def settings():
    print("Settings button clicked")

loading_screen()
main_menu()
pygame.quit()
sys.exit()
