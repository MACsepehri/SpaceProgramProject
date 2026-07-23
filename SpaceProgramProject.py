import pygame
import sys
from SpaceProgramProjectAssets import config

# init
pygame.init()
display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
win = pygame.display.set_mode((width, height))
status = "menu"

# set rocket positions
def set_rocket_middle():
    # 1
    with open("SpaceProgramProjectAssets/rocket/1.robj", "w") as file:
        file.write(f"NoseObject({int(width / 2 - 64)}, 200)\nFuelTank_1({int(width / 2 - 64)}, 308)\nEngine_1({int(width / 2 - 64)}, 405)")

# actions
def start():
    global status

    status = "ingame"

def rocket_object_1():
    global status

    status = "rocket_1"

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
        config.button_action(btn, [rocket_object_1, lambda: ..., lambda: ...])

def draw_rocket_object_1():
    global status
    global rocket_type

    if status == "rocket_1":
        rocket_1.render()
        rocket_type = 1

def render_rotation():
    global status
    global rocket_type

    if status == "rocket_1" and rocket_type == 1:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            rocket_1.rotate(-2)
        if keys[pygame.K_d]:
            rocket_1.rotate(2)

# update
def update():
    draw_menu()
    draw_ingame_button()
    render_rotation()

    # render rocket objects
    draw_rocket_object_1()

# objects
rocket_1 = config.RocketObjectLoader("SpaceProgramProjectAssets/rocket/1.robj", win)

rocket_type = 0

# run
def main():
    set_rocket_middle()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        win.fill("skyblue")
        update()
        pygame.display.update()

if __name__ == "__main__":
    main()