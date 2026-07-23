import pygame
import math

# init
pygame.init()
font = pygame.font.Font("SpaceProgramProjectAssets/file/font/main.ttf", 48)
small_font = pygame.font.Font("SpaceProgramProjectAssets/file/font/main.ttf", 32)

class Button:
    def __init__(self, win, x, y, width, height, font=None, text="", middle=False, text_color="white", button_color="black", hover_color=(21,21,21), image=None, r=5, win_object=None):
        self.win_object = win_object if win_object is not None else win
        
        if middle and self.win_object is not None:
            screen_width = self.win_object.get_width() if hasattr(self.win_object, 'get_width') else self.win_object.size[0]
            x = (screen_width - width) // 2
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        try:
            if font is not None: 
                self.font = font
            else: 
                self.font = pygame.font.Font(None, 32)
        except:
            self.font = pygame.font.Font(None, 32)
            
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.clicked = False
        self.visible = True
        self.middle = middle
        self.image = image if image != "" else None
        self.border_radius = r

    def draw(self):
        if not self.visible:
            return
        
        if self.middle and self.win_object is not None:
            screen_width = self.win_object.get_width() if hasattr(self.win_object, 'get_width') else self.win_object.size[0]
            self.rect.x = (screen_width - self.width) // 2
        
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
            return False
        
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
        
    def set_middle(self):
        if self.win_object is not None:
            screen_width = self.win_object.get_width() if hasattr(self.win_object, 'get_width') else self.win_object.size[0]
            self.rect.x = (screen_width - self.width) // 2

def draw_text(text, color, x, y, win, font):
    win.blit(font.render(text, True, color), (x, y))

def draw_button(btn_list):
    for btn in btn_list:
        btn.draw()

def button_action(btn_list, action_list):
    i = 0
    for btn in btn_list:
        if btn.is_clicked():
            action_list[i]()
        i += 1

class RocketObjectLoader:
    def __init__(self, file: str, win):
        self.content = open(file, "r").readlines()
        self.win = win
        self.angle = 0
        self.parts = []
        self.load_parts()
        
    def load_parts(self):
        for content in self.content:
            if not content.strip() or "(" not in content:
                continue
                
            try:
                coords = content.split("(")[1].replace(")", "").split(",")
                x = int(coords[0].strip())
                y = int(coords[1].strip())
            except (IndexError, ValueError) as e:
                print(f"Error parsing line: {content.strip()} - {e}")
                continue
            
            if self.isNose(content):
                part_type = "nose"
                image_path = "SpaceProgramProjectAssets/assets/nose/nose.png"
            elif self.isFireEngine(content):
                part_type = "fire_engine"
                image_path = "SpaceProgramProjectAssets/assets/fire/fire_engine.png"
            elif self.isFuelTank1(content):
                part_type = "fuel_tank"
                image_path = "SpaceProgramProjectAssets/assets/fuel_tank/fuel_tank_1.png"
            elif self.isEngine_1(content):
                part_type = "engine"
                image_path = "SpaceProgramProjectAssets/assets/engine/engine1.png"
            else:
                print(f"Unknown part type: {content.strip()}")
                continue
                
            try:
                image = pygame.image.load(image_path).convert_alpha()
            except pygame.error as e:
                print(f"Failed to load image: {image_path} - {e}")
                continue
            
            print(f"Loaded {part_type} at ({x}, {y})")
            
            self.parts.append({
                'type': part_type,
                'x': x,
                'y': y,
                'image': image,
                'original_x': x,
                'original_y': y
            })
        
        print(f"Total parts loaded: {len(self.parts)}")
    
    def isNose(self, string):
        return string.strip().startswith("NoseObject(")
    
    def isFuelTank1(self, string):
        return string.strip().startswith("FuelTank_1(")
    
    def isEngine_1(self, string):
        return string.strip().startswith("Engine_1(")

    def isFireEngine(self, string):
        return string.strip().startswith("FireEngine(")
    
    def rotate(self, angle_change):
        self.angle += angle_change
        self.angle %= 360
    
    def get_rotated_position(self, original_x, original_y, center_x, center_y):
        dx = original_x - center_x
        dy = original_y - center_y
        
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        new_dx = dx * cos_a - dy * sin_a
        new_dy = dx * sin_a + dy * cos_a
        
        new_x = center_x + new_dx
        new_y = center_y + new_dy
        
        return int(new_x), int(new_y)
    
    def render(self):
        if not self.parts:
            print("No parts to render")
            return
            
        center_x = sum(p['x'] for p in self.parts) // len(self.parts)
        center_y = sum(p['y'] for p in self.parts) // len(self.parts)
        
        render_order = {
            'nose': 0,
            'fuel_tank': 1,
            'engine': 2,
            'fire_engine': 3
        }
        sorted_parts = sorted(self.parts, key=lambda p: render_order.get(p['type'], 0))
        
        for part in sorted_parts:
            pos_x, pos_y = self.get_rotated_position(
                part['original_x'], 
                part['original_y'],
                center_x,
                center_y
            )
            
            rotated_image = pygame.transform.rotate(part['image'], -self.angle)
            rect = rotated_image.get_rect(center=(pos_x, pos_y))
            self.win.blit(rotated_image, rect)
    
    def handle_input(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if keys[pygame.K_a]:
                self.rotate(-2)
            if keys[pygame.K_d]:
                self.rotate(2)
            return True
        return False
    
    def toggle_fire(self, show_fire=True):
        for part in self.parts:
            if part['type'] == 'fire_engine':
                if show_fire:
                    try:
                        part['image'] = pygame.image.load(
                            "SpaceProgramProjectAssets/assets/fire/fire_engine.png"
                        ).convert_alpha()
                    except pygame.error:
                        pass
                else:
                    part['image'] = pygame.Surface((1, 1), pygame.SRCALPHA)
                break

def hide_button(btn_list):
    for btn in btn_list:
        btn.hide()

def draw_launch_pad(width, height, win):
    pad = pygame.image.load("SpaceProgramProjectAssets/assets/launch_pad/launchpad.png")
    x = width / 2 - 113
    y = height - 49
    win.blit(pad, (x, y))

def show_height_type(h):
    if h >= 1000:
        m = []
        res = ""
        for data in str(h / 1000):
            m.append(data)
        for i in range(3):
            res += m[i]
        return m, "km"
    else:
        return h, "m"