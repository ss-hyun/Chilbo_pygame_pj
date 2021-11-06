import pygame
import stage_template
import random

def move_user(ch, game):
    ch.pos[0] += ch.move_factor

    if ch.curr_state == 0 and ch.pos[0] > game.display_size[0]:
        ch.pos[0] = -ch.size[ch.curr_state][0]
    elif ch.curr_state == 1 and ch.pos[0] + ch.size[ch.curr_state][0] < 0:
        ch.pos[0] = game.display_size[0]
    
    for key in game.event_key:
        if key == pygame.K_LEFT:
            ch.move_factor = -ch.move_factor
            ch.curr_state = 1
        elif key == pygame.K_RIGHT:
            ch.move_factor = -ch.move_factor
            ch.curr_state = 0

def user_start(ch, game):
    ch.pos = [ (game.display_size[0]-ch.size[ch.curr_state][0])/2, game.display_size[1]-ch.size[ch.curr_state][1]-10 ]

# def boss_moving(ch, game):
#     ch.pos[0] += ch.move_factor
#     if ch.pos[0] + ch.size[ch.curr_state][0] > game.display_size[0]:
#         ch.move_factor = -random.randint(0,10)
#     elif ch.pos[0] < 0:
#         ch.move_factor = random.randint(0,10)

def boss_start(ch, game):
    ch.pos = [ (game.display_size[0]-ch.size[ch.curr_state][0])/2, ch.size[ch.curr_state][1]-100 ]

def boss_resize(ch):
    image_boss = pygame.image.load("/image/exboss.svg")
    ch.boss_resize = pygame.transform.rotozoom(image_boss, 0, 2)

def stage1(name, path, fps, speed):
    bg_image = pygame.image.load(path + "/image/stage1_background.jpg")
    # character info : (name, relative path list, function list, group)
    # # name : character name
    # # relative path list : Characters have various states. Images of all possible conditions.
    # # function list : A function of all actions that can be done as a character, including initialization.
    # #                 [move, positioning, attack] - if it doesn't exist -> None
    # # group : There are user groups(0) and monster groups(1) in the game.
    ch_info_list = [ ("user", [ "/image/character_r.jpg", "/image/character_l.jpg" ], [ move_user, user_start, None, None ], 0),
                     ("boss", [ "/image/exboss.svg" ], [ None, boss_start, None, boss_resize ], 1) ]
    
    game = stage_template.Stage(name, 1, path, fps, speed, bg_image, ch_info_list)
    
    for c in game.ch_list:
        c.resize()
    
    game.run()
