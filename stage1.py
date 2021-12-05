from typing import Sized
import pygame
from pygame.constants import KEYUP
import stage_template
import random

def move_user(ch, game):
    ch.pos[0] += ch.move_factor_x 
    ch.pos[1] += ch.move_factor_y    

    if ch.pos[1] < 208:
        ch.pos[1] = 208
    if ch.pos[1] > 620:
        ch.pos[1] = 620
    if ch.pos[0] < 8.5:
        ch.pos[0] = 8.5
    if ch.pos[0] > 1130:
        ch.pos[0] = 1130

    speed = 3
    if ch.move_state == True:
        ch.change_count += 1
    
    key_up = False
  
    for event in game.event_key:
        if event.type == pygame.KEYDOWN:            
                                    
            if event.key == pygame.K_LEFT:
                ch.move_state = True
                ch.move_factor_x = -speed            
                ch.curr_state = 6        

            elif event.key == pygame.K_RIGHT:
                ch.move_state = True
                ch.move_factor_x = speed              
                ch.curr_state = 4

            elif event.key == pygame.K_UP:
                ch.move_state = True
                key_up = True
                ch.move_factor_y = -speed              
                ch.curr_state = 10         
                           
            elif event.key == pygame.K_DOWN:
                ch.move_state = True                
                ch.move_factor_y = speed            
                ch.curr_state = 8


        if event.type == pygame.KEYUP:
            ch.move_state = False
            if event.key == pygame.K_UP:               
                ch.move_factor_y = 0
                ch.curr_state = 3

            elif event.key == pygame.K_DOWN:
                ch.move_factor_y = 0
                ch.curr_state = 2


            elif event.key == pygame.K_RIGHT:
                ch.move_factor_x = 0
                ch.curr_state = 0

            elif event.key == pygame.K_LEFT:
                ch.move_factor_x = 0
                ch.curr_state = 1

    if ch.move_state == True:
        if ch.change_count == 10:
            if ch.curr_state % 2 == 0:
               ch.curr_state += 1
            else:
               ch.curr_state -= 1

        if ch.change_count == 20:
            ch.change_count = 0 
    

def user_start(ch, game):
    ch.pos = [ (game.display_size[0]-ch.size[ch.curr_state][0])//2, game.display_size[1]-ch.size[ch.curr_state][1]-10 ]
    if game.stage_number == 1:
        ch.hp = 100 #유저 체력        
    if game.stage_number == 2:
        if ch.hp <= 100 and ch.hp >= 50:
            ch.hp = 100
        elif ch.hp < 50 and ch.hp > 0:
            ch.hp += 50 
        print(ch.hp)
        ch.hp + 50 <= 100
    
def user_resize(ch):
    l = len(ch.image)
    for i in range(0, l):
        ch.image[i] = pygame.transform.rotozoom(ch.image[i], 0, 0.25)
        # size variable change
        ch.size[i] = ch.image[i].get_rect().size

def user_attack(ch, game):
    for event in game.event_key:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:          
            user_attack_pos = ch.pos.copy()
            if ch.curr_state == 0 or ch.curr_state == 4 or ch.curr_state == 5:
                user_attack_pos[0] += 105 
                user_attack_pos[1] += 50
            if ch.curr_state == 1 or ch.curr_state == 6 or ch.curr_state == 7:
                user_attack_pos[1] += 50
            if ch.curr_state == 3 or ch.curr_state == 10 or ch.curr_state == 11:
                user_attack_pos[0] += 108
                user_attack_pos[1] += 50
            if ch.curr_state == 2 or ch.curr_state == 8 or ch.curr_state == 9:
               user_attack_pos[1] += 50                 
            game.user_attack.append(stage_template.Spherical_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], user_attack_pos, user_atk_move))

                                                 
def user_atk_move(atk, game):    
    atk.pos[1] -= 6
    if len(game.monster_list) == 1: game.next_stage = True
    for monster in game.monster_list[:]:
        if monster.name == "laser_waring" or monster.name == "laser_waring1" or monster.name == "laser_field1" or monster.name == "laser_field2":
            break
        if atk.pos[1] <= monster.pos[1] + monster.size[monster.curr_state][1] and monster.pos[0] < atk.pos[0] and atk.pos[0] < monster.pos[0] + monster.size[monster.curr_state][0] :
            if game.stage_number == 1 and monster.name != "boss":      
                monster.hp -= atk.damage
                if monster.hp <= 0:
                    game.monster_list.remove(monster)
            elif game.stage_number == 2 and monster.name == "boss":      
                monster.hp -= atk.damage
                if monster.hp <= 0:
                    game.monster_list.remove(monster)
                    game.next_stage = True
            return False 
    return True 
    
def boss_start(ch, game):    
    ch.pos = [ (game.display_size[0]-ch.size[ch.curr_state][0])//2, ch.size[ch.curr_state][1]-270 ]
    if game.stage_number == 2:
        ch.hp = 120
def boss_resize(ch):
    l = len(ch.image)
    for i in range(0, l):
        ch.image[i] = pygame.transform.rotozoom(ch.image[i], 0, 1.3)
        # size variable change
        ch.size[i] = ch.image[i].get_rect().size


def arm_move_fist_1(ch, game):
    ch.change_count += 1
    if ch.change_count == ch.state_change_speed:
        ch.change_count= 0
        if ch.curr_state == 0: ch.change_direc = True
        elif ch.curr_state == ch.state_num-4: ch.change_direc = False
        elif ch.curr_state == ch.state_num-1: ch.change_direc = False
        ch.curr_state += 1 if ch.change_direc else -1
    
def arm_atk_fist_1(ch, game):
        if ch.curr_state < 3 and random.randrange(1, 200) == 4:
            ch.change_count= 0                
            ch.curr_state = 3
            ch.change_direc = True
            atk = stage_template.Rectangle_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.size[ch.curr_state], 
                                                            ch.pos.copy(), fist_atk_move, ch.atk_list[0][3])
            game.monster_attack.append(atk)
            atk.save_var['ch'] = ch


def arm_move_fist_2(ch, game):
    ch.change_count += 1
    if ch.change_count == ch.state_change_speed:
        ch.change_count= 0
        if ch.curr_state == 0: ch.change_direc = True
        elif ch.curr_state == ch.state_num-4: ch.change_direc = False
        elif ch.curr_state == ch.state_num-1: ch.change_direc = False
        ch.curr_state += 1 if ch.change_direc else -1
    
def arm_atk_fist_2(ch, game):    
    if ch.curr_state < 3 and random.randrange(1, 200) == 4:
        ch.change_count= 0                
        ch.curr_state = 3
        ch.change_direc = True
        atk = stage_template.Rectangle_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.size[ch.curr_state], 
                                                        ch.pos.copy(), fist_atk_move, ch.atk_list[0][3])
        game.monster_attack.append(atk)
        atk.save_var['ch'] = ch

def arm_move_forceps(ch, game):
    ch.change_count += 1
    if ch.change_count == ch.state_change_speed:
        ch.change_count= 0
        if ch.curr_state == 0: ch.change_direc = True
        elif ch.curr_state == ch.state_num-3: ch.change_direc = False
        elif ch.curr_state == ch.state_num-1: ch.change_direc = False
        ch.curr_state += 1 if ch.change_direc else -1
    
    for event in game.event_key:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT:
                ch.change_count= 0                
                ch.curr_state = 3
                ch.change_direc = True
                print("forceps_attack")

def arm_move_saw(ch, game):
    ch.change_count += 1
    if ch.change_count == ch.state_change_speed:
        ch.change_count= 0
        if ch.curr_state == 0: ch.change_direc = True
        elif ch.curr_state == ch.state_num-2: ch.change_direc = False
        elif ch.curr_state == ch.state_num-1: ch.change_direc = False
        ch.curr_state += 1 if ch.change_direc else -1 
    for event in game.event_key:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                ch.change_count= 0                
                ch.curr_state = 5
                ch.change_direc = True
                print("saw_attack")

def arm_trans(ch):
    for i in range(0, ch.state_num):
        ch.image[i] = pygame.transform.rotozoom(ch.image[i], 0, 0.5)
        ch.size[i] = ch.image[i].get_rect().size

def arm1_start(ch, game):
    ch.hp = 30
    ch.pos = [ 300, 0 ]
    ch.curr_state = 1

def arm2_start(ch, game):
    ch.hp = 30
    ch.pos = [ 845, 0 ]
    ch.curr_state = 1

def arm3_start(ch, game):
    ch.hp = 30
    ch.pos = [ 183, 0 ]
    ch.curr_state = 1

def arm4_start(ch, game):
    ch.hp = 30
    ch.pos = [ 973, 0 ]
    ch.curr_state = 1

def arm5_start(ch, game):
    ch.hp = 30
    ch.pos = [ 0, 0 ]
    ch.curr_state = 1

def arm6_start(ch, game):
    ch.hp = 30
    ch.pos = [ 1010, 0 ]
    ch.curr_state = 1

def fist_atk_move(atk, game):
    ch = atk.save_var['ch']
    if ch.curr_state > 2:
        atk.range = ch.size[ch.curr_state]
        for usr in game.user_list[:]:
            if usr.pos[0] > atk.pos[0] + atk.range[0] or usr.pos[0] + usr.size[usr.curr_state][0] < atk.pos[0] \
                    or usr.pos[1] > atk.pos[1] + atk.range[1] or usr.pos[1] + usr.size[usr.curr_state][1] < atk.pos[1]: continue
            usr.hp -= atk.damage
            atk.sound.play()
            if usr.hp <= 0: game.user_list.remove(usr)
            return False
        return True
    return False

def forceps_attack_1(ch, game):
    if random.randrange(1, 175) == 4:
        atk = stage_template.Spherical_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], 
                                                [ ch.pos[0]+75 , ch.pos[1]+180 ], forceps_attack_move_1)
        game.monster_attack.append(atk)
        atk.save_var['d1'] = random.randrange(1, 4) 

def forceps_attack_move_1(atk, game):
    if atk.save_var['d1'] == 1:
        atk.pos[1] += 6
    elif atk.save_var['d1'] == 2:
        atk.pos[0] += 3
        atk.pos[1] += 6
    elif atk.save_var['d1'] == 3:
        atk.pos[0] += 6
        atk.pos[1] += 6
    if atk.pos[0] >= game.display_size[0] or atk.pos[1] >= game.display_size[1]:
        return False
    for user in game.user_list[:]:
        if user.pos[1] < atk.pos[1] and atk.pos[1] <= user.pos[1] + user.size[user.curr_state][1] and user.pos[0] < atk.pos[0] and atk.pos[0] <= user.pos[0] + user.size[user.curr_state][0] :
            if user.name == "user":           
                user.hp -= atk.damage
                if user.hp <= 0: game.user_list.remove(user)
            return False 
    return True

def forceps_attack_2(ch, game):
    if random.randrange(1, 175) == 4:
        atk = stage_template.Spherical_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], [ ch.pos[0]+15, ch.pos[1]+190 ], forceps_attack_move_2)
        game.monster_attack.append(atk)
        atk.save_var['d2'] = random.randrange(1, 4)

def forceps_attack_move_2(atk, game):
    if atk.save_var['d2'] == 1:
        atk.pos[1] += 6
    elif atk.save_var['d2'] == 2:
        atk.pos[0] -= 3
        atk.pos[1] += 6
    else:
        atk.pos[0] -= 6
        atk.pos[1] += 6
    for user in game.user_list[:]:
        if user.pos[1] < atk.pos[1] and atk.pos[1] <= user.pos[1] + user.size[user.curr_state][1] and user.pos[0] < atk.pos[0] and atk.pos[0] <= user.pos[0] + user.size[user.curr_state][0] :
            if user.name == "user":           
                user.hp -= atk.damage
                if user.hp <= 0:
                    game.user_list.remove(user)
            return False 
    if atk.pos[0] <= 0 or atk.pos[1] <= 0:
        return False
    return True

def saw_attack_1(ch, game):
    l = 3
    if random.randrange(1, 200) == 4:
        atk = stage_template.Spherical_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], [ ch.pos[0]+175 , ch.pos[1]+250 ], saw_attack_move_1)
        game.monster_attack.append(atk)
        atk.remove_count == 3
        atk.save_var['Ss1'] = random.randrange(1, 4)
        atk.save_var['Sscount1'] = l

def saw_attack_move_1(atk, game):
    if atk.remove_count == 3:
        if atk.save_var['Ss1'] == 1:
            atk.pos[0] += 4
            atk.pos[1] += 4
        elif atk.save_var['Ss1'] == 2:
            atk.pos[0] += 4
            atk.pos[1] += 2
        elif atk.save_var['Ss1'] == 3:
            atk.pos[0] += 6
            atk.pos[1] += 2
    elif atk.remove_count == 2:
        if atk.save_var['Ss1'] == 1:
            atk.pos[0] -= 4
            atk.pos[1] -= 4
        elif atk.save_var['Ss1'] == 2:
            atk.pos[0] -= 4
            atk.pos[1] -= 2
        elif atk.save_var['Ss1'] == 3:
            atk.pos[0] -= 6
            atk.pos[1] -= 2
    if atk.pos[0] <= 150 or atk.pos[1] <= 150:
        atk.remove_count = 3
        return False
    if atk.pos[0] >= game.display_size[0] - 70 or atk.pos[1] >= game.display_size[1] - 70:
        atk.remove_count = 2
    for user in game.user_list[:]:
        if user.pos[1] < atk.pos[1] + 37 and atk.pos[1] + 37 <= user.pos[1] + user.size[user.curr_state][1] and user.pos[0] < atk.pos[0] + 37 and atk.pos[0] + 37 <= user.pos[0] + user.size[user.curr_state][0] :
            if user.name == "user" and atk.remove_count == 2:
                atk.save_var['Sscount1'] -= 1
                if atk.save_var['Sscount1'] == 0:
                    return False
                atk.remove_count = 3
                user.hp -= atk.damage
                if user.hp <= 0:
                    game.user_list.remove(user)
            elif user.name == "user" and atk.remove_count == 3:    
                atk.save_var['Sscount1'] -= 1
                if atk.save_var['Sscount1'] == 0:
                    return False
                atk.remove_count = 2
                user.hp -= atk.damage
                if user.hp <= 0:
                    game.user_list.remove(user)
            return True
    return True

def saw_attack_2(ch, game):
    l = 10
    if random.randrange(1, 200) == 4:
        atk = stage_template.Spherical_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], [ ch.pos[0]+15 , ch.pos[1]+250 ], saw_attack_move_2)
        game.monster_attack.append(atk)
        print(ch.pos[0]+10 , ch.pos[1]+250 )
        atk.remove_count = 3
        atk.save_var['Ss2'] = random.randrange(1, 4)
        atk.save_var['Sscount2'] = l

def saw_attack_move_2(atk, game):
    if atk.remove_count == 3:
        if atk.save_var['Ss2'] == 1:
            atk.pos[0] -= 4
            atk.pos[1] += 4
        elif atk.save_var['Ss2'] == 2:
            atk.pos[0] -= 4
            atk.pos[1] += 2
        elif atk.save_var['Ss2'] == 3:
            atk.pos[0] -= 6
            atk.pos[1] += 2
    elif atk.remove_count == 2:
        if atk.save_var['Ss2'] == 1:
            atk.pos[0] += 4
            atk.pos[1] -= 4
        elif atk.save_var['Ss2'] == 2:
            atk.pos[0] += 4
            atk.pos[1] -= 2
        elif atk.save_var['Ss2'] == 3:
            atk.pos[0] += 6
            atk.pos[1] -= 2
    if atk.pos[0] >= 1025 or atk.pos[1] <= 250:
        atk.remove_count = 3
        return False
    if atk.pos[0] <= 0 or atk.pos[1] >= game.display_size[1] - 70:
        atk.remove_count = 2
    for user in game.user_list[:]:
        if user.pos[1] < atk.pos[1] + 37 and atk.pos[1] + 37 <= user.pos[1] + user.size[user.curr_state][1] and user.pos[0] < atk.pos[0] + 37 and atk.pos[0] + 37 <= user.pos[0] + user.size[user.curr_state][0] :
            if user.name == "user" and atk.remove_count == 2:
                atk.save_var['Sscount2'] -= 1
                if atk.save_var['Sscount2'] == 0:
                    return False
                atk.remove_count = 3
                user.hp -= atk.damage
                if user.hp <= 0:
                    game.user_list.remove(user)
            elif user.name == "user" and atk.remove_count == 3:    
                atk.save_var['Sscount2'] -= 1
                if atk.save_var['Sscount2'] == 0:
                    return False
                atk.remove_count = 2
                user.hp -= atk.damage
                if user.hp <= 0:
                    game.user_list.remove(user)
            return True
    return True



def laser_field1_start(ch, game):
    ch.pos = [ 0, game.display_size[1] - ch.size[ch.curr_state][1]]
    atk = stage_template.Rectangle_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], ch.pos.copy(), laser_field1_attack_attack)
    game.monster_attack.append(atk)
    atk.save_var['ch'] = ch

def laser_field1_attack_attack(atk, game):
    ch = atk.save_var['ch']
    atk.range = ch.size[ch.curr_state]
    for user in game.user_list[:]:
        if user.pos[0] > atk.pos[0] + atk.range[0]: continue
        user.hp -= atk.damage
        print(user.hp)
        if user.hp <= 0: game.user_list.remove(user)
        return True                  
    return True

def laser_field2_start(ch, game):
    ch.pos = [ game.display_size[0] - ch.size[ch.curr_state][0], game.display_size[1] - ch.size[ch.curr_state][1] ]
    atk = stage_template.Rectangle_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], ch.pos.copy(), laser_field2_attack_attack)
    game.monster_attack.append(atk)
    atk.save_var['ch'] = ch

def laser_field2_attack_attack(atk, game):
    ch = atk.save_var['ch']
    atk.range = ch.size[ch.curr_state]
    for user in game.user_list[:]:
        if user.pos[0] + user.size[user.curr_state][0] < atk.pos[0]: continue
        user.hp -= atk.damage
        print(user.hp)
        if user.hp <= 0: game.user_list.remove(user)
        return True                  
    return True

def laser_attack_attack(atk, game): 
    for event in game.event_key:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
            atk.pos[1] = 300

def stage1(name, path, fps, speed):
    bg_image = pygame.image.load(path + "/image/boss_stage_test.jpg")

    # attack info : ( image path, damage, range, sound )
    user_atk_info = [ [ "/image/bullet.png", 1, 9, None ] ] 
    fist_atk_info = [ [ None, 5, None, "/sound/punch.wav" ] ]
    forceps_atk_info = [ [ "/image/gugu.png", 5, 10, None ] ]
    saw_atk_info = [ [ "/image/sawsaw.png", 10, 20, None  ] ]


    # character info : (name, relative path list, function list, attack info list, group)
    # # name : character name
    # # relative path list : Characters have various states. Images of all possible conditions.
    # # function list : A function of all actions that can be done as a character, including initialization.
    # #                 [move, positioning, attack, image transform] - if it doesn't exist -> None
    # # group : There are user groups(0) and monster groups(1) in the game.
    ch_info_list = [ ("user", [ "/image/오른1.png", "/image/왼1.png", "/image/앞1.png", "/image/뒤1.png" ,"/image/오른2.png", "/image/오른3.png", "/image/왼2.png","/image/왼3.png","/image/앞2.png", "/image/앞3.png", "/image/뒤2.png","/image/뒤3.png"], [ move_user, user_start, user_attack, user_resize ], user_atk_info, 0),
                     ("boss", [ "/image/exboss1.png" ], [ None, boss_start, None, boss_resize ], None, 1),                    

                     ("boss_arm1", [ "/image/fist.png", "/image/fist_+1.png", "/image/fist_+2.png", "/image/fist_attack.png", "/image/fist_attack_+1.png", "/image/fist_attack_+2.png"  ], [ arm_move_fist_1, arm2_start, arm_atk_fist_1, arm_trans ], fist_atk_info, 1),
                     ("boss_arm2", [ "/image/r_fist.png", "/image/r_fist_+1.png", "/image/r_fist_+2.png", "/image/r_fist_attack.png", "/image/r_fist_attack_+1.png", "/image/r_fist_attack_+2.png" ], [ arm_move_fist_2, arm1_start, arm_atk_fist_2, arm_trans ], fist_atk_info, 1),
                     ("boss_arm3", [ "/image/forceps_A.png", "/image/forceps_B.png", "/image/forceps_B.png", "/image/forceps_A.png", "/image/forceps_A.png" ], [ arm_move_forceps, arm4_start, forceps_attack_2, arm_trans ], forceps_atk_info, 1),
                     ("boss_arm4", [ "/image/r_forceps_A.png", "/image/r_forceps_B.png", "/image/r_forceps_B.png", "/image/r_forceps_1_attack_A.png", "/image/r_forceps_1_attack_B.png" ], [ arm_move_forceps, arm3_start, forceps_attack_1, arm_trans ], forceps_atk_info, 1),
                     ("boss_arm5", [ "/image/sawB.png", "/image/sawB_+1.png", "/image/sawB_+2.png", "/image/sawB_+1.png","/image/sawB.png", "/image/sawB.png" ], [ arm_move_saw, arm5_start, saw_attack_1, arm_trans ], saw_atk_info, 1),
                     ("boss_arm6", [ "/image/r_sawB.png", "/image/r_sawB_+1.png", "/image/r_sawB_+2.png", "/image/r_sawB_+1.png", "/image/r_sawB.png", "/image/r_sawB.png" ], [ arm_move_saw, arm6_start, saw_attack_2, arm_trans ], saw_atk_info, 1),
                    ]

    
    stage1_1 = stage_template.Stage(name, 1, path, fps, speed, bg_image, ch_info_list)
    have_next = stage1_1.run()
        
    bg_image = pygame.image.load(path + "/image/boss_stage_test.jpg")

    def laser_waring_start(ch, game):
        ch.pos = [ 500, 300 ]

    def laser_waring_move(ch, game):
        i = random.randrange(200, 900)
        ch.change_count += 1
        ch.state_change_speed = 160
        if ch.change_count == 160:
            ch.change_count = 0
        elif ch.change_count == 1:
            ch.pos[0] = i
        elif ch.change_count == 121:
            ch.pos[0] = 1500

    def laser_attack(ch, game):
        if ch.change_count == 120:
            atk = stage_template.Rectangle_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], ch.pos.copy(), laser_attack_move)
            game.monster_attack.append(atk)
            atk.save_var['ch'] = ch

    def laser_attack_move(atk, game):
        ch = atk.save_var['ch']
        if ch.change_count >= 120 and ch.change_count <= 140:
            atk.range = ch.size[ch.curr_state]
            for user in game.user_list[:]:
                if user.pos[0] > atk.pos[0] + atk.range[0] or user.pos[0] + user.size[user.curr_state][0] < atk.pos[0] or user.pos[1] > atk.pos[1] + atk.range[1] or user.pos[1] + user.size[user.curr_state][1] < atk.pos[1]: continue
                user.hp -= atk.damage
                print(user.hp)
                if user.hp <= 0: game.user_list.remove(user)
        if ch.change_count == 1:
            return False
        return True

    def laser_waring_start1(ch, game):
        ch.pos = [ 0, 300 ]

    def laser_waring_move1(ch, game):
        i = random.randrange(300, 600)
        ch.change_count += 1
        ch.state_change_speed = 160
        if ch.change_count == 160:
            ch.change_count = 0
        elif ch.change_count == 1:
            ch.pos[1] = i
        elif ch.change_count == 121:
            ch.pos[1] = 1500

    def laser_attack1(ch, game):
        if ch.change_count == 120:
            atk = stage_template.Rectangle_Attack(ch.atk_list[0][0], ch.atk_list[0][1], ch.atk_list[0][2], ch.pos.copy(), laser_attack_move1)
            game.monster_attack.append(atk)
            atk.save_var['ch'] = ch

    def laser_attack_move1(atk, game):
        ch = atk.save_var['ch']
        if ch.change_count >= 120 and ch.change_count <= 140:
            atk.range = ch.size[ch.curr_state]
            for user in game.user_list[:]:
                if user.pos[0] > atk.pos[0] + atk.range[0] or user.pos[0] + user.size[user.curr_state][0] < atk.pos[0] or user.pos[1] > atk.pos[1] + atk.range[1] or user.pos[1] + user.size[user.curr_state][1] < atk.pos[1]: continue
                user.hp -= atk.damage
                print(user.hp)
                if user.hp <= 0: game.user_list.remove(user)
        if ch.change_count == 1:
            return False
        return True


    # attack info : ( image path, damage, range, sound )
    laser_atk_info = [ [ "/image/laser_attack.png", 2 , 10, None ] ]
    laser1_atk_info = [ [ "/image/laser_attack1.png", 2 , 10, None ] ]
    laser_field_atk_info = [ [ None, 5, None, None ] ]

    ch_info_list = ["user", "boss", 
                     ("laser_field1", [ "/image/laser_field.png" ], [ None, laser_field1_start, None, None ], laser_field_atk_info, 1),
                     ("laser_field2", [ "/image/laser_field.png" ], [ None, laser_field2_start, None, None ], laser_field_atk_info, 1),
                     ("laser_waring", ["/image/waring.png"], [laser_waring_move, laser_waring_start, laser_attack, None], laser_atk_info, 1),
                     ("laser_waring1", ["/image/waring3.png"], [laser_waring_move1, laser_waring_start1, laser_attack1, None], laser1_atk_info, 1)]

    if have_next:
        stage1_2 = stage_template.Stage(name, 2, path, fps, speed, bg_image, ch_info_list, stage1_1)
        have_next = stage1_2.run()


    if not stage1_1.user_list :
        bg_image = pygame.image.load(path + "/image/game_over.jpg")
        game_over = stage_template.Stage(name, 0, path, fps, speed, bg_image, [])
        game_over.run()
        return

    bg_image = pygame.image.load(path + "/image/ending.jpg")

    if have_next:
        clear = stage_template.Stage(name, 0, path, fps, speed, bg_image, []).run()
        clear.run()

