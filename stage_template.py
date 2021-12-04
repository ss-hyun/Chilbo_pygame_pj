import sys
import pygame
from pygame.constants import K_TAB
import button

class Stage_frame:
    def __init__(self, name, path, button_pos):
        self.name = name
        self.running = True
        self.pause = False
        start_bt_img = pygame.image.load(path + "/image/button_start.jpg")
        pause_bt_img = pygame.image.load(path + "/image/button_pause.jpg")
        close_bt_img = pygame.image.load(path + "/image/button_close.jpg")
        close_bt_pos = (button_pos[0]-60, button_pos[1])
        pause_bt_pos = (close_bt_pos[0]-60, button_pos[1])
        start_bt_pos = (pause_bt_pos[0]-60, button_pos[1])
        self.button = [ button.Button(start_bt_img, start_bt_img, start_bt_pos, self.stage_start),
                        button.Button(pause_bt_img, pause_bt_img, pause_bt_pos, self.stage_pause),
                        button.Button(close_bt_img, close_bt_img, close_bt_pos, self.stage_exit)]

    def stage_start(self):
        self.pause = False

    def stage_pause(self):
        self.pause = True

    def stage_exit(self):
        self.running = False

# 구 형태의 공격
class Spherical_Attack:
    def __init__(self, image, damage, range, pos, atk_move):
        self.image = image
        self.damage = damage
        self.atk_range = range
        self.pos = pos
        self.atk_mv_action = atk_move
        self.remove_count = 3
        # List of variables you want to save here
        # "variable name" : value
        self.save_var = {}

    # If you want to keep the attack, return True and if you want to remove it, return False.
    def move(self, curr_stage):
        if self.atk_mv_action != None:
            return self.atk_mv_action(self, curr_stage)

# 사각형 형태의 공격
class Rectangle_Attack:
    def __init__(self, image, damage, range, pos, atk_move, sound = None):
        self.image = image
        self.damage = damage
        self.atk_range = range
        self.pos = pos
        self.atk_mv_action = atk_move
        self.sound = sound
        self.remove_count = 3
        # List of variables you want to save here
        # "variable name" : value
        self.save_var = {}

    # If you want to keep the attack, return True and if you want to remove it, return False.
    def move(self, curr_stage):
        if self.atk_mv_action != None:
            return self.atk_mv_action(self, curr_stage)


class Character:
    def __init__(self, path, info):
        self.name = info[0] 
        # image list : user - [ right image, left image ]
        self.state_num = 0
        self.image = []
        for img_path in info[1]:  
            self.image.append(pygame.image.load(path+img_path))   
            self.state_num += 1        
        # image size list : user - [ right image size, left image size ]
        self.size = []
        for img in self.image:
            self.size.append(img.get_rect().size)
        # image init setting
        self.curr_state = 0
        self.change_count = 0
        self.state_change_speed = 20
        self.change_direc = True # True : list index up, False : list index down
        self.move_state = False        
        # image position
        self.pos = [ 0, 0 ]
        self.move_action = info[2][0] 
        self.positioning = info[2][1]
        self.attack = info[2][2]
        self.img_control = info[2][3]
        # atk_list[i][0] : image surface, [1] : damage
        self.atk_list = []
        if info[3]:
            for atk in info[3]: self.atk_list.append((pygame.image.load(path+atk[0]) if atk[0] else None, atk[1], atk[2], pygame.mixer.Sound(path+atk[3]) if atk[3] else None))
        if self.atk_list and self.atk_list[0][3]: self.atk_list[0][3].set_volume(0.02)
        # group : 1 - monster, 0 - user
        self.group = info[4]
        self.move_factor_x = 0
        self.move_factor_y = 0
        self.hp = 0
        self.laser_status = False
        self.save_var = {}

    def pos_init(self, curr_stage):
        if self.positioning != None:
            self.positioning(self, curr_stage)
        
    def move(self, curr_stage):
        if self.move_action != None:
            self.move_action(self, curr_stage)

    def shoot_atk(self, curr_stage):
        if self.attack != None:
            self.attack(self, curr_stage)

    def img_transform(self):
        if self.img_control != None:
            self.img_control(self)


class Stage:
    def __init__(self, game_name, stage_number, path, fps, speed, bg_image, ch_info_list, before_stage = None):
        self.bg_image = bg_image
        self.display_size = self.bg_image.get_rect().size
        self.user_list = []
        for ch_info in ch_info_list:
            if isinstance(ch_info, str):
                for c in before_stage.user_list:
                    if c.name == ch_info: self.user_list.append(c)
            else:
                if ch_info[4] != 0: continue
                c = Character(path, ch_info)
                self.user_list.append(c)
                c.img_transform()
        self.monster_list = []
        for ch_info in ch_info_list:
            if isinstance(ch_info, str):
                for c in before_stage.monster_list:
                    if c.name == ch_info: self.monster_list.append(c)
            else:
                if ch_info[4] != 1: continue
                c = Character(path, ch_info)
                self.monster_list.append(c)
                c.img_transform()
        self.fps = fps
        self.speed = speed
        self.stage_number = stage_number
        self.frame = Stage_frame(game_name+": STAGE "+ str(stage_number), path, (self.display_size[0], 10))
        self.event_mouse = []
        self.event_key = []
        self.user_attack = []
        self.monster_attack = []

    def run(self):
        background = pygame.display.set_mode(self.display_size)
        for c in self.user_list:
            c.pos_init(self)
        for c in self.monster_list:
            c.pos_init(self)
        
        next_stage = False
        

        while self.frame.running:
            pygame.display.set_caption(self.frame.name)
            self.fps.tick(self.speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.event_mouse.append(pygame.mouse.get_pos())
                    for b in self.frame.button:
                        b.click()                
                elif len(self.monster_list) == 1:
                    self.frame.running = False
                    next_stage = True
                    break
                self.event_key.append(event)
            if self.frame.pause:
                continue
            
            background.blit(self.bg_image, (0, 0))
            
            for c in self.user_list:
                background.blit(c.image[c.curr_state], c.pos)
                c.move(self)
                if c.attack: c.attack(c, self)

            for c in self.monster_list:
                background.blit(c.image[c.curr_state], c.pos)
                c.move(self)
                if c.attack: c.attack(c, self)

            for a in self.user_attack[:]:
                if a.image: background.blit(a.image, a.pos)
                if not a.move(self): 
                    self.user_attack.remove(a)
                
            for a in self.monster_attack[:]:
                if a.image: background.blit(a.image, a.pos)
                if not a.move(self):
                    self.monster_attack.remove(a)

            for b in self.frame.button:
                b.draw(background) 

            pygame.display.update()
            self.event_mouse.clear()
            self.event_key.clear()
            
        return next_stage
