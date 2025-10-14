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

# retro font
font = pygame.font.Font('font.otf', 40)
header_font = pygame.font.Font('font.otf', 100)

#background
loading_background = pygame.image.load('loading.png')
loading_background = pygame.transform.scale(loading_background, (screen_width, screen_height))
menu_background = pygame.image.load('menu.png')
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

#loading joke bank
startup_jokes1 = [
    "Six?",
    "Y'know what else is massive?",
    "*UFO zooms past*"
]

startup_jokes2 = [
    "Seven!",
    "Low taper fade.",
    "Oh my god, did you see that!"
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
        loading_joke = font.render(selected_joke, True, YELLOW)

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

def main_menu():
    menu_running = True
    while menu_running:
        screen.blit(menu_background, (0, 0))

        menu_text = header_font.render("Main Menu", True, YELLOW)
        play_text = font.render("Play", True, YELLOW)
        tutorial_text = font.render("Tutorial", True, YELLOW)
        menu_joke = font.render(selected_joke2, True, YELLOW)

        title_w = screen_width // 2 - menu_text.get_width() // 2
        title_h = screen_height // 4 - menu_text.get_height() // 2
        play_w = screen_width // 2 - play_text.get_width() // 2
        play_h = (screen_height * 2) // 4 - play_text.get_height() // 2
        tut_w = screen_width // 2 - tutorial_text.get_width() // 2
        tut_h = (screen_height * 2.5) // 4 - tutorial_text.get_height() // 2
        joke_w = screen_width // 2 - menu_joke.get_width() // 2
        joke_h = (screen_height * 7) // 8 - menu_joke.get_height() // 2

        screen.blit(menu_text, (title_w, title_h))
        screen.blit(play_text, (play_w, play_h))
        screen.blit(tutorial_text, (tut_w, tut_h)) 
        screen.blit(menu_joke, (joke_w, joke_h)) 
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

        
loading_screen()
main_menu()
pygame.quit()
sys.exit()