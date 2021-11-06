import sys
import pygame
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

class Attack:
    def __init__(self, damage, pos, atk_move):
        self.demage = damage
        self.pos = pos
        self.atk_mv_action = atk_move

    def move(self, curr_stage):
        self.atk_mv_action(self, curr_stage)


class Character:
    def __init__(self, path, info):
        self.name = info[0]
        self.image = []
        for img_path in info[1]:
            self.image.append(pygame.image.load(path+img_path))
        self.size = []
        for img in self.image:
            self.size.append(img.get_rect().size)
        self.curr_state = 0
        self.pos = [ 0, 0 ]
        self.move_action = info[2][0]
        self.positioning = info[2][1]
        self.attack = info[2][2]
        self.group = info[3]
        self.move_factor = 5

    def pos_init(self, curr_stage):
        if self.positioning != None:
            self.positioning(self, curr_stage)
        
    def move(self, curr_stage):
        if self.move_action != None:
            self.move_action(self, curr_stage)

    def shoot_atk(self, curr_stage):
        if self.attack != None:
            self.attack(self, curr_stage)

class Stage:
    def __init__(self, game_name, stage_number, path, fps, speed, bg_image, ch_info_list):
        self.bg_image = bg_image
        self.display_size = self.bg_image.get_rect().size
        self.ch_list = []
        for ch_info in ch_info_list:
            self.ch_list.append(Character(path, ch_info))
        self.fps = fps
        self.speed = speed
        self.frame = Stage_frame(game_name+": STAGE "+str(stage_number), path, (self.display_size[0], 10))
        self.event_mouse = []
        self.event_key = []
        self.user_attack = []
        self.monster_attack = []

    def run(self):
        background = pygame.display.set_mode(self.display_size)
        for c in self.ch_list:
            c.pos_init(self)
        
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
                elif event.type == pygame.KEYDOWN:
                    self.event_key.append(event.key)
            if self.frame.pause:
                continue
            
            background.blit(self.bg_image, (0, 0))
            
            for b in self.frame.button:
                b.draw(background) 
            
            for c in self.ch_list:
                c.move(self)
                background.blit(c.image[c.curr_state], c.pos)

            pygame.display.update()
            self.event_mouse.clear()
            self.event_key.clear()
