import pygame
import stage_template
import random

def move_user(ch, game):
    # ch.pos[0] += ch.move_factor
    ch.pos[0] += ch.move_factor_x 
    ch.pos[1] += ch.move_factor_y 

    

    #if ch.curr_state == 0 and ch.pos[0] > game.display_size[0]:
        #ch.pos[0] = -ch.size[ch.curr_state][0]
    #elif ch.curr_state == 1 and ch.pos[0] + ch.size[ch.curr_state][0] < 0:
        #ch.pos[0] = game.display_size[0]
    speed = 5


    for event in game.event_key:
        if event.type == pygame.KEYDOWN:                        
            if event.key == pygame.K_LEFT:
              ch.move_factor_x = -speed         
            
            elif event.key == pygame.K_RIGHT:
              ch.move_factor_x = speed

            elif event.key == pygame.K_UP:
              ch.move_factor_y = -speed

            elif event.key == pygame.K_DOWN:
              ch.move_factor_y = speed
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ch.move_factor_y = 0
            elif event.key == pygame.K_DOWN:
                ch.move_factor_y = 0
            elif event.key == pygame.K_RIGHT:
                ch.move_factor_x = 0
            elif event.key == pygame.K_LEFT:
                ch.move_factor_x = 0
            
def user_start(ch, game):
    ch.pos = [ (game.display_size[0]-ch.size[ch.curr_state][0])/2, game.display_size[1]-ch.size[ch.curr_state][1]-10 ]

# def boss_moving(ch, game):
#     ch.pos[0] += ch.move_factor
#     if ch.pos[0] + ch.size[ch.curr_state][0] > game.display_size[0]:
#         ch.move_factor = -random.randint(0,10)
#     elif ch.pos[0] < 0:
#         ch.move_factor = random.randint(0,10)

def boss_start(ch, game):
    ch.pos = [ (game.display_size[0]-(ch.size[ch.curr_state][0] * 1.3))/2, ch.size[ch.curr_state][1]-220 ]

def boss_resize(ch):
    # image_boss = pygame.image.load("/image/exboss.svg")
    l = len(ch.image)
    for i in range(0, l):
        ch.image[i] = pygame.transform.rotozoom(ch.image[i], 0, 1.3)
        # size variable change
        # ch.size[ch.curr_state][i] *= 1.45 이거 전혀 못하겠습니다..

def arm_move(ch, game):
    ch.change_count += 1
    if ch.change_count == ch.state_change_speed:
        ch.change_count= 0
        if ch.curr_state == 0: ch.change_direc = True
        elif ch.curr_state == ch.state_num-1: ch.change_direc = False
        ch.curr_state += 1 if ch.change_direc else -1

def arm_trans(ch):
    for i in range(0, ch.state_num):
        ch.image[i] = pygame.transform.rotozoom(ch.image[i], 0, 0.5)

def arm1_start(ch, game):
    ch.pos = [ 0, 0 ]
    ch.curr_state = 2

def arm2_start(ch, game):
    ch.pos = [ 600, 0 ]
    ch.curr_state = 2

def stage1(name, path, fps, speed):
    bg_image = pygame.image.load(path + "/image/boss_stage_test.jpg")
    # character info : (name, relative path list, function list, group)
    # # name : character name
    # # relative path list : Characters have various states. Images of all possible conditions.
    # # function list : A function of all actions that can be done as a character, including initialization.
    # #                 [move, positioning, attack, image transform] - if it doesn't exist -> None
    # # group : There are user groups(0) and monster groups(1) in the game.
    ch_info_list = [ ("user", [ "/image/character_r.jpg", "/image/character_l.jpg" ], [ move_user, user_start, None, None ], 0),
                     ("boss", [ "/image/exboss.svg" ], [ None, boss_start, None, boss_resize ], 1),
                     ("boss_arm1", [ "/image/saw2_+2.png", "/image/saw2_+1.png", "/image/saw2_0.png", "/image/saw2_-1.png", "/image/saw2_-2.png" ], [ arm_move, arm1_start, None, arm_trans ], 1), 
                     ("boss_arm2", [ "/image/fist_-1.png", "/image/fist.png", "/image/fist_+1.png", "/image/fist_+2.png", "/image/fist_+3.png" ], [ arm_move, arm2_start, None, arm_trans ], 1) ]

    game = stage_template.Stage(name, 1, path, fps, speed, bg_image, ch_info_list)

    for c in game.ch_list:
        c.img_transform()
    
    game.run()
