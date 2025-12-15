import pygame
import sys
import time
import random
import textwrap

pygame.init()

#music
pygame.mixer.music.load('bg music.mp3')
pygame.mixer.music.set_volume(0.5)  # range is 0.0 to 1.0
pygame.mixer.music.play(-1)
clap = pygame.mixer.Sound('cheer and clap.mp3')
boo = pygame.mixer.Sound('boo.mp3')
laugh = pygame.mixer.Sound('laugh.mp3')
heavy_laugh = pygame.mixer.Sound('extreme laughter.mp3')
disappointed = pygame.mixer.Sound('disappointed.mp3')
fail = pygame.mixer.Sound('fail trumpet.mp3')

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
even_smaller_font = pygame.font.Font('font.otf', 20)

#background
loading_background = pygame.image.load('loading.png')
loading_background = pygame.transform.scale(loading_background, (screen_width, screen_height))
menu_background = pygame.image.load('menu.png')
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))
game_bg = pygame.image.load('game bg.png')
game_bg = pygame.transform.scale(game_bg, (screen_width, screen_height))

#other global images
back_img = pygame.image.load('back button.png')
back_img = pygame.transform.scale(back_img, (50, 50))

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

#opening jokes
opening_lines = [
    "So… I walked in here and immediately regretted it.",
    "Hey, how are ya?",
    "Good evening everyone… or at least the three people pretending to listen.",
    "They told me to 'act natural', so here I am. Awkward as heck.",
    "I promised myself I would NOT cry on stage today… no guarantees.",
    "Thanks for being here. My mum said nobody would come.",
    "I love the energy in here… it's hiding, but I can feel it."
]

joke_categories = {
    "dad": [
        "I’m afraid for the calendar. Its days are numbered.",
        "Why don’t eggs tell jokes? They’d crack each other up.",
        "I only know 25 letters of the alphabet. I don’t know Y.",
        "Why did the scarecrow win an award? Because he was outstanding in his field."
    ],

    "sarcastic": [
        "Oh great. Another meeting that could’ve been an email.",
        "I love deadlines. I love the whooshing sound they make as they fly by.",
        "Yeah, because that went *exactly* as planned.",
        "I’m not lazy. I’m on energy-saving mode."
    ],

    "hilarious": [
        "I tried exercising but I kept losing my balance—turns out the treadmill was off.",
        "My phone battery lasts longer than my motivation.",
        "I told my computer I needed a break and it froze.",
        "I started a diet, but I keep losing my snacks."
    ]
}

jokes = [
    "Did you hear they arrested the devil? Yeah, they got him on possession.",
    "What did one DNA say to the other DNA? “Do these genes make me look fat?”",
    "It’s okay if you don’t like me. Not everyone has good taste.",
    "My IQ test results came back. They were negative.",
    "What do you get when you cross a polar bear with a seal? A polar bear.",
    "Why can’t you trust an atom? Because they make up literally everything.",
    "At least your mum thinks you're pretty.",
    "Why was six afraid of seven? Because seven eight nine.",
    "What do you call a hippie’s wife? Mississippi.",
    "What’s the difference between an outlaw and an in-law? Outlaws are wanted.",
    "According to my neighbour's diary, i have boundary issues??",
    "Scientists have recently discovered a food that greatly reduces sex drive. It’s called wedding cake.",
    "Before you marry a person, you should first make them use a computer with a slow Internet connection to see who they really are."
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

#timer
timer = 10
timer_running = False
timer_update = pygame.time.get_ticks()

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

#starts the timer each new round
def start_timer():
    global timer, timer_running, timer_update
    timer = 10
    timer_running = True
    timer_update = pygame.time.get_ticks()

    #timer countdown or exit round
def update_timer():
    global timer, timer_running, timer_update
        
    if not timer_running:
        return #exits function if timer is not running
        
    current_time = pygame.time.get_ticks()
    
    #check if 1 second has passed then update timer
    if current_time - timer_update >= 1000:
        timer -= 1
        timer_update = current_time
        
    #exit if timer is zero
    if timer <= 0:
        timer == 0
        disappointed.play()
        timer_running = False
    

def play_game():
    global timer_running
    gameplay_running = True

    #player sprite set up
    player_img = pygame.image.load('player.png')
    player_sprite = pygame.transform.scale(player_img, (200, 250))
    player_x = screen_width // 2 - 110 #sets the postion of the player on the screen
    player_y = screen_height // 3 - 25

    #mic set up
    mic_img = pygame.image.load('mic.png')
    mic_sprite = pygame.transform.scale(mic_img, (320, 300))
    mic_x = screen_width // 2 - 140
    mic_y = screen_height // 3 - 50

    #pause button set up
    pause_img = pygame.image.load('pause unclicked.png')
    pause_sprite = pygame.transform.scale(pause_img, (50, 50))
    pause_rect = pause_img.get_rect(topleft=(20, 20))
    #pause_w = 20
    #pause_h = 20

    #score display and setup
    totalscore = 0

    #boost bar and setup
    boostlevel = 0
    max_boost = 100

    #some variables
    joke_clicked = False
    using_openings = True

    #opening joke selection
    def gen_jokes():
        if using_openings:
            joke = random.sample(opening_lines, 4)
        else:
            joke = random.sample(jokes, 4)
        return joke

    start_timer()
    joke = gen_jokes()

    while gameplay_running:
        screen.blit(game_bg, (0, 0))
        screen.blit(pause_sprite, (pause_rect))
        screen.blit(player_sprite, (player_x, player_y))
        screen.blit(mic_sprite, (mic_x, mic_y))

        #score display
        score_text = smaller_font.render(f"Score: {totalscore}", True, YELLOW)
        score_x = screen_width // 2 - score_text.get_width() // 2
        score_y = 20
        screen.blit(score_text, (score_x, score_y))

        #bar display
        bar_width = 200
        bar_height = 20
        bar_x = screen_width // 2  - bar_width // 2
        bar_y = 65

        pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, bar_width, bar_height), 3)
        boostbar = (boostlevel / max_boost) * bar_width
        pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, boostbar, bar_height))

        def draw_timer():
            timer_text = smaller_font.render(str(timer), True, YELLOW)
            timer_x = screen_width - timer_text.get_width() - 20
            timer_y = 20
            screen.blit(timer_text, (timer_x, timer_y))

        update_timer()
        draw_timer()

        # joke boxe dimensions
        box_margin = 20
        box_width = (screen_width - (3 * box_margin)) // 2
        box_height = 60

        # top row y
        top_y = 400
        # bottom row y
        bottom_y = top_y + box_height + box_margin

        # box positions
        box_positions = [
            (box_margin, top_y),                     # box1
            (box_margin * 2 + box_width, top_y),     # box2
            (box_margin, bottom_y),                  # box3
            (box_margin * 2 + box_width, bottom_y)   # box4
        ]       

        # Draw all 4 boxes
        for i, (x, y) in enumerate(box_positions):
            pygame.draw.rect(screen, YELLOW, (x, y, box_width, box_height), 3)
            
            #wrap jokes
            wrapped = textwrap.wrap(joke[i], width = 40) 

           # pick right padding based on if wrapped or not
            if len(wrapped) > 1:
                text_y = y + 5       
            else:
                 text_y = y + 10     
            for line in wrapped:
                # render joke text inside
                joke_text = even_smaller_font.render(line, True, YELLOW)
                # center text inside each box
                text_x = x + (box_width - joke_text.get_width()) // 2
                screen.blit(joke_text, (text_x, text_y))
                text_y += joke_text.get_height() + 1.5

        #mouse button click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        if click and not joke_clicked:  
            for i, (x, y) in enumerate(box_positions):
                box_rect = pygame.Rect(x, y, box_width, box_height)

                if box_rect.collidepoint(mouse):
                    joke_clicked = True
                    selected_index = i
                    joke_selected = joke[selected_index]

                    print("You selected:", joke_selected)

                    # play clap sound for opening jokes
                    clap.play()
                
                    if using_openings:
                        using_openings = False
                        joke = gen_jokes()
                        joke_clicked = False
                        start_timer()

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameplay_running = False




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
        back_rect = back_img.get_rect(topleft=(20, 20))

        title_w = screen_width // 2 - settings_text.get_width() // 2
        title_h = 60
        back_w = 20
        back_h = 20

        screen.blit(settings_text, (title_w, title_h))
        screen.blit(back_img, (back_w, back_h))

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
                if back_rect.collidepoint(event.pos):
                    settings_running = False  # go back

                elif bg_rect.collidepoint(event.pos):
                    dragging = 'bg'
                elif event_rect.collidepoint(event.pos):
                    dragging = 'event'
                elif audience_rect.collidepoint(event.pos):
                    dragging = 'audience'
                elif master_rect.collidepoint(event.pos):
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
