import pygame
import sys
from SpaceProgramProjectAssets import config

# init
pygame.init()
display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60
status = "menu"
ingame = False
engine_is_on = False
space_pressed = False
max_height = 300
rocket_1_y = 0
fly = False
fuel = 100
rocket_height = 0

# set rocket positions
def set_rocket_middle():
    # 1
    with open("SpaceProgramProjectAssets/rocket/1.robj", "w") as file:
        file.write(f"NoseObject({int(width / 2 - 64)}, {height - 262})\nFuelTank_1({int(width / 2 - 64)}, {height - 154})\nEngine_1({int(width / 2 - 64)}, {height - 57})")

# actions
def start():
    global status
    status = "ingame"

def rocket_object_1():
    global status
    global ingame
    ingame = True
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
            rocket_1.rotate(-0.3)
        if keys[pygame.K_d]:
            rocket_1.rotate(0.3)

def help_text():
    global ingame

    if ingame:
        config.draw_text("Rotate with A - D\nTurn on/off engine with Space", True, width - 350, height - 100, win, config.small_font)

def change_engine_state():
    global engine_is_on
    engine_is_on = not engine_is_on

# update
def update():
    global ingame
    global engine_is_on
    global space_pressed
    global max_height
    global rocket_1_y
    global rocket_1s
    global rocket_1
    global fly
    global fuel
    global rocket_height

    # handle key 
    keys = pygame.key.get_pressed()
    if ingame:
        if keys[pygame.K_SPACE] and not space_pressed:
            change_engine_state()
            space_pressed = True
            fly = True

        elif not keys[pygame.K_SPACE]:
            space_pressed = False

    if ingame:
        config.draw_launch_pad(width, height, win)
        # draw fuel
        config.draw_text(f"Fuel: {int(fuel)}\nHeight: {config.show_height_type(int(rocket_height)[0])} {config.show_height_type(int(rocket_height)[1])}", "black", 10, height - 100, win, config.font)

    if ingame and fly:
        fuel -= 0.01
        rocket_height += 0.02

    if int(rocket_1_y) != int(max_height) and fly:
        with open("SpaceProgramProjectAssets/rocket/1.robj", "r") as file:
            data = file.readlines()
        
        y_coords = []
        for content in data:
            y_coords.append(int(float(content.split("(")[1].replace(")", "").split(",")[1].replace("\n", ""))))
        
        speed = 2
        new_y_coords = [y - speed for y in y_coords]
        
        with open("SpaceProgramProjectAssets/rocket/1.robj", "w") as file:
            file.write(f"NoseObject({int(width / 2 - 64)}, {new_y_coords[0]})\n")
            file.write(f"FuelTank_1({int(width / 2 - 64)}, {new_y_coords[1]})\n")
            file.write(f"Engine_1({int(width / 2 - 64)}, {new_y_coords[2]})")
        
        rocket_1 = config.RocketObjectLoader("SpaceProgramProjectAssets/rocket/1.robj", win)
        rocket_1.render()
        
        rocket_1_y = abs(new_y_coords[0])

    # functions
    draw_menu()
    draw_ingame_button()
    help_text()

    # render rocket objects
    draw_rocket_object_1()
    if engine_is_on:
        render_rotation()

rocket_type = 0

# objects
set_rocket_middle()
rocket_1 = config.RocketObjectLoader("SpaceProgramProjectAssets/rocket/1.robj", win)

# run
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        win.fill("skyblue")
        update()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()