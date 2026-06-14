"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
from random import randint
from pygame import mixer
from operator import itemgetter

def display_score():
    global lives, invincibility_timer
    current_time = (pygame.time.get_ticks() - start_time)//1000 
    score_surf = game_font.render(f"Score: {current_time}", False, "Black") 
    score_rect = score_surf.get_rect(center = (400,50))
    #screen.blit(score_surf, score_rect)
    menu_surf = small_font.render("Escape (E)", False, "Black")
    menu_rect = menu_surf.get_rect(center = (710, 25))
    screen.blit(menu_surf, menu_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
    screen.blit(score_surf, score_rect)
    return current_time 

def obstacle_movement(obstacle_list):
    global is_playing, lives, invincibility_timer, game_state
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= int(5+ (pygame.time.get_ticks() - start_time)//10000)
            if obstacle_rect.bottom == 210:
                screen.blit(shark_surf, obstacle_rect)
            else:
                screen.blit(seaweed_surf, obstacle_rect)
            
            if fish_rect.inflate(-110, -110).colliderect(obstacle_rect.inflate(-80, -80)):
                if invincibility_timer ==0:
                    lives -= 1
                    invincibility_timer = 40
                if lives <= 0:
                    is_playing = False
                    game_state = "game_over"
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return[]

def fish_animation():
    global fish_surf, fish_index
    fish_index += 0.1
    if fish_index >= len(fish_move): fish_index = 0
    fish_surf = fish_move[int(fish_index)]

def shark_animation():
    global shark_surf, shark_index
    shark_index += 0.1
    if shark_index >= len(shark_move): shark_index = 0
    shark_surf = shark_move[int(shark_index)]

def collectible_animation():
    global collectible_surf, collectible_index
    collectible_index += 0.1
    if collectible_index >= len(collectible_move): collectible_index = 0
    collectible_surf = collectible_move[int(collectible_index)]

#REVIEW WHAT THIS DOES AGAIN
def check_difficulty():
    global score
    global shark_move
    
def display_lives():
    life_surf = pygame.image.load("graphics/heart/heart.png").convert_alpha()
    for i in range(lives):
        life_rect = life_surf.get_rect(topleft = (615 + i*40, 20))
        screen.blit(life_surf, life_rect)

def collectible_movement(collectible_list):
    global lives
    if collectible_list:
    #only runs code is at least 1 collectible on screen
        for collectible_rect in collectible_list:
            collectible_rect.x -= int(5 + (pygame.time.get_ticks() - start_time) // 10000)
            screen.blit(collectible_surf, collectible_rect)
#deletes collectibles that have been touched or gone off screen(x axis), so it doesn't get checked for collisions again
            if fish_rect.inflate(-110, -110).colliderect(collectible_rect.inflate(-20, -20)):
                if lives< 3:
                    lives += 1
                collectible_list.remove(collectible_rect)
        collectible_list = [collectible for collectible in collectible_list if collectible.x > -100]
        return collectible_list
    else:
        return []


# Initialize Pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
start_time = 0
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)
collectible_timer = pygame.USEREVENT + 2
pygame.time.set_timer(collectible_timer, 10000)
#appears every 10 seconds instead of 1.2
score = 0

# Game state variables
is_playing = False  # Whether in game or in menu
game_state = "menu"
GROUND_Y = 300  # The Y-coordinate of the ground level
PLAYER_FLOOR = 340
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps, negative moves up
fish_gravity_speed = 0  # The current speed at which the player falls
lives = 3
invincibility_timer = 0
can_double_jump = False
#HOW TO CHANGE FONT SO IT IS NOT IN SYSFONT?
game_font = pygame.font.SysFont("bahnschrift", 50)
small_font = pygame.font.SysFont("bahnschrift", 30)




# backgrounds
SKY_SURF = pygame.image.load("graphics/ocean_top.png").convert()
SKY_SURF = pygame.transform.scale(SKY_SURF, (800, 400))
MENU_SURF = pygame.image.load("graphics/menu_pic.png").convert()
MENU_SURF = pygame.transform.scale(MENU_SURF, (800, 400))
baby_shark = pygame.mixer.Sound("graphics/shark/baby_shark.mp3")
#baby_shark.play( loops = -1 )
jump_sound = pygame.mixer.Sound("graphics/bubbles/bubbles.mp3")
score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))


# sprites
fish_move_1 = pygame.image.load("graphics/fish/fish.png").convert_alpha()
fish_move_2 = pygame.image.load("graphics/fish/fish_move_2.png").convert_alpha()
fish_move = [fish_move_1, fish_move_2]
fish_index = 0
fish_surf = fish_move[fish_index]
fish_rect = fish_surf.get_rect(bottomleft=(25, PLAYER_FLOOR))
seaweed_surf = pygame.image.load("graphics/seaweed/seaweed.png").convert_alpha()
seaweed_surf = pygame.transform.scale(seaweed_surf, (130, 130))
shark_move_1 = pygame.image.load("graphics/shark/shark.png").convert_alpha()
shark_move_2 = pygame.image.load("graphics/shark/shark_move_2.png").convert_alpha()
shark_move = [shark_move_1, shark_move_2]
shark_index = 0
shark_surf = shark_move[shark_index]
bubbles_surf = pygame.image.load("graphics/bubbles/bubbles.png").convert_alpha()
obstacle_rect_list = []
collectible_rect_list = []
fish_stand = pygame.image.load("graphics/fish/fish.png").convert_alpha()
fish_stand = pygame.transform.rotozoom(fish_stand, 0, 2)
fish_stand_rect = fish_stand.get_rect(center = (400,200))
game_name = game_font.render('Ocean Escape', False, ("black"))
game_name_rect = game_name.get_rect(center = (400,75))
game_over_message = game_font.render('Game Over', False, "Black")
game_over_message_rect = game_over_message.get_rect(center = (400,250))
menu_message = small_font.render("Press space to start", False, "black")
menu_message_rect = menu_message.get_rect(center = (400, 140))
collectible_move_1 = pygame.image.load("graphics/lifesaver/lifesaver_move_1.png").convert_alpha()
collectible_move_1 = pygame.transform.scale(collectible_move_1, (90, 90))
collectible_move_2 = pygame.image.load("graphics/lifesaver/lifesaver_move_2.png").convert_alpha()
collectible_move_2 = pygame.transform.scale(collectible_move_2, (90, 90))
collectible_move = [collectible_move_1, collectible_move_2]
collectible_index = 0
collectible_surf = collectible_move[collectible_index]



while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if fish_rect.bottom >= PLAYER_FLOOR:
                    fish_gravity_speed = JUMP_GRAVITY_START_SPEED
                    can_double_jump = True
                    jump_sound.play()
                elif can_double_jump:
                    fish_gravity_speed = JUMP_GRAVITY_START_SPEED
                    can_double_jump = False
                    jump_sound.play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                is_playing = False
                game_state = "escaped"
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                previous_state = game_state
                is_playing = True
                game_state = "playing"
                baby_shark.stop()
                baby_shark.play(loops=-1) 
                if previous_state != "escaped":
                    start_time = pygame.time.get_ticks()
                    baby_shark.stop()
                    baby_shark.play(loops=-1)
                    screen.fill((94,129,162))
                    obstacle_rect_list = []
                    collectible_rect_list = []
                    fish_gravity_speed = 0
                    fish_rect.bottom = PLAYER_FLOOR
                    lives = 3
                    invincibility_timer = 0
        if event.type == obstacle_timer and is_playing:
            if randint(0,2):
                obstacle_rect_list.append(seaweed_surf.get_rect(bottomright = (randint(900,1100),PLAYER_FLOOR)))
            else:
                obstacle_rect_list.append(shark_surf.get_rect(bottomright = (randint(900,1100),210)))
        if event.type == collectible_timer and is_playing:
            #if randint(0,2):
            collectible_rect_list.append(collectible_surf.get_rect(bottomright = (randint(900,1100), PLAYER_FLOOR)))
            
    if is_playing: 
        screen.fill("blue")  # Wipe the screen
        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        pygame.draw.rect(screen, (194, 178, 128), (0, GROUND_Y, 800, 400))
        score = display_score()
        # Adjust player's vertical location then blit it
        fish_gravity_speed += 1
        fish_rect.y += fish_gravity_speed
        if fish_rect.bottom > PLAYER_FLOOR: fish_rect.bottom = PLAYER_FLOOR
        if invincibility_timer > 0:
            invincibility_timer-= 1
        fish_animation()
        shark_animation()
        collectible_animation()
        screen.blit(fish_surf, fish_rect)
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        collectible_rect_list = collectible_movement(collectible_rect_list)
        display_lives()

    # When game is over, display game over message
    elif game_state == "menu":
        screen.blit(MENU_SURF, (0, 0))
        screen.blit(fish_stand, fish_stand_rect)
        screen.blit(game_name, game_name_rect)
        baby_shark.stop()

    elif game_state == "escaped":
        screen.blit(MENU_SURF, (0, 0))
        screen.blit(fish_stand, fish_stand_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(menu_message, menu_message_rect)
        score_message = game_font.render(f'Score: {score}', False, "black")
        score_message_rect = score_message.get_rect(center = (400,350))
        screen.blit(score_message, score_message_rect)
        baby_shark.stop()

    elif game_state == "game_over":
        screen.blit(MENU_SURF, (0, 0))
        screen.blit(game_name, game_name_rect)
        screen.blit(game_over_message, game_over_message_rect)
        screen.blit(menu_message, menu_message_rect)
        score_message = game_font.render(f'Score: {score}', False, "black")
        score_message_rect = score_message.get_rect(center = (400,350))
        screen.blit(score_message, score_message_rect)
        baby_shark.stop()

        #if score == 0:
            #screen.blit(game_message, game_message_rect)
            #pygame.mixer.pause()
        #else:
            #screen.blit(score_message, score_message_rect)
            #baby_shark.stop()
            

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
