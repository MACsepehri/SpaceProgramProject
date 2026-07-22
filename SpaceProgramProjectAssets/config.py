import pygame

# init
pygame.init()
font = pygame.font.Font("SpaceProgramProjectAssets/file/font/main.ttf", 48)
small_font = pygame.font.Font("SpaceProgramProjectAssets/file/font/main.ttf", 32)

class Button:
    def __init__(self, win, x, y, width, height, font=None, text="", middle=False, text_color="white", button_color="black", hover_color=(21,21,21), image=None, r=5, win_object=None):
        if middle and win_object is not None:
            screen_width = win_object.size[0]
            x = (screen_width - width) // 2
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.win_object = win
        try:
            if font != None: self.font = font
            else: self.font = pygame.font.Font(32)
        except:
            self.font = pygame.font.Font(None, 32)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.clicked = False
        self.visible = True
        self.middle = middle
        if image != "":
            self.image = image
        else:
            self.image = None
        self.border_radius = r

    def draw(self):
        if not self.visible:
            return
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(self.win_object, self.hover_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.win_object, self.button_color, self.rect, border_radius=self.border_radius)

        if self.image is not None:
            text_surface = self.image
        else:
            text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.win_object.blit(text_surface, text_rect)

    def is_clicked(self):
        if not self.visible:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_x, mouse_y) and mouse_click:
            if not self.clicked:
                self.clicked = True
                return True
        else:
            self.clicked = False
        return False
    
    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

def draw_button(btn_list, win):
    for btn in btn_list:
        btn.draw(win)

def button_action(btn_list, action_list):
    i = 0
    for btn in btn_list:
        if btn.is_clicked():
            action_list[i]()
        i += 1