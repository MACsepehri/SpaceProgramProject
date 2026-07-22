import pygame
import sys
from SpaceProgramProjectAssets import config

# init
pygame.init()
display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
win = pygame.display.set_mode((width, height))
status = "menu"

# actions
def start():
    global status

    status = "ingame"


# draw button
def draw_menu():
    global status

    if status == "menu":
        btn = [
            config.Button(win, 0, 250, 200, 90, config.font, "Start", middle=True),
            config.Button(win, 0, 350, 200, 90, config.font, "Setting", middle=True),
            config.Button(win, 0, 450, 200, 90, config.font, "Exit", middle=True)
        ]
        config.draw_button(btn)
        config.button_action(btn, [start, lambda: ..., sys.exit])

def draw_ingame_button():
    global status

    if status == "ingame":
        btn = [
            config.Button(win, 30, 250, 200, 90, config.font, "Rocket 1"),
            config.Button(win, 30, 350, 200, 90, config.font, "Rocket 2"),
            config.Button(win, 30, 450, 200, 90, config.font, "Rocket 3")
        ]
        config.draw_button(btn)
        config.button_action(btn, [lambda: ..., lambda: ..., lambda: ...])

# update
def update():
    draw_menu()
    draw_ingame_button()

# run
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        win.fill("skyblue")
        update()
        pygame.display.update()

if __name__ == "__main__":
    main()