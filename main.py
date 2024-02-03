import pygame
import sys
import random 

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('The Game')
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/joystix/joystix_monospace.otf', 20)
title_font = pygame.font.Font('fonts/joystix/joystix_monospace.otf', 50)
start_time = 0
high_score = 0
bonus_score = 0

# Surfaces
background_surf = pygame.image.load('images/Background1.png').convert()

ground_height = 300
ground_surf = pygame.image.load('images/ground.png').convert()

## Power Ups
coin_surf = pygame.image.load('images/coin.png').convert_alpha()
coin_rect = coin_surf.get_rect(midbottom = (400, 200))

## PLAYER
player_surf = pygame.image.load('images/StickMan.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (100,300))

# ENEMIES
square_surf = pygame.image.load('images/EnemySquare.png').convert_alpha()
square_rect = square_surf.get_rect(midbottom = (850,300))
square_speed = 4

square2_surf = pygame.image.load('images/EnemySquare2.png').convert_alpha()
square2_rect = square_surf.get_rect(midbottom = (850,300))
square2_speed = 7

ufo_surf = pygame.image.load('images/pink_ufo.png').convert_alpha()
ufo_rect = ufo_surf.get_rect(midbottom = (-150,150))
ufo_speed = 5.5

# Player Movement
player_gravity = 0
player_accel = 1
player_speed = 0
move_left = False
move_right = False

# Game Modes
game_active = False
current_level = 1
title_surf = title_font.render('The Game',False,(64,64,64))
title_rect = title_surf.get_rect(center = (400,50))

start_surf = game_font.render('Press Space to Start',False,(64,64,64))
start_rect = title_surf.get_rect(center = (400,150))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == ground_height:
                player_gravity = -20
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_DOWN:
                player_gravity = 50
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
                player_speed = 0
            if event.key == pygame.K_LEFT:
                move_left = False
                player_speed = 0
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                start_time = pygame.time.get_ticks()
                current_level = 1
                bonus_score = 0
                
            
    screen.blit(background_surf,(0,0))
    screen.blit(ground_surf,(0,300))
    
    if game_active:
    # Player movement
        level_surf = game_font.render(f'Level {current_level}',False,(64,64,64))
        level_rect = level_surf.get_rect(center = (400,20))
        screen.blit(level_surf,level_rect)
        screen.blit(coin_surf,coin_rect)
        if move_left:
            if player_speed > -15:
                player_speed -= player_accel
            player_rect.x += player_speed
        if move_right:
            if player_speed < 15:
                player_speed += player_accel
            player_rect.x += player_speed
        
        if player_rect.right < 0: player_rect.left = 800
        if player_rect.left > 800: player_rect.right = 0
        
        # Gravity 
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= ground_height: player_rect.bottom = ground_height
            
        screen.blit(player_surf,player_rect)
        
        # Display Score
        score = (pygame.time.get_ticks() - start_time)//500 + bonus_score
        score_surf = game_font.render(f'Score: {score}',False,(64,64,64))
        score_rect = score_surf.get_rect(center = (400,50))
        screen.blit(score_surf,score_rect)
        if score > high_score: high_score = score
            
        
        if current_level > 0:
            screen.blit(square_surf,square_rect)
            square_rect.x -= square_speed
            if square_rect.x < -50:
                prob = random.random()
                if prob < .5:
                    square_rect.x = 850
                else:
                    square_speed *= -1
            if square_rect.x > 850: 
                prob = random.random()
                if prob < .5:
                    square_rect.x = -50
                else:
                    square_speed *= -1
        if current_level == 2 or current_level == 4:
            screen.blit(square2_surf,square2_rect)
            square2_rect.x -= square2_speed
            if square2_rect.x < -50:
                prob = random.random()
                if prob < .5:
                    square2_rect.x = 850
                else:
                    square2_speed *= -1
            if square2_rect.x > 850: 
                prob = random.random()
                if prob < .5:
                    square2_rect.x = -50
                else:
                    square2_speed *= -1
        if current_level > 2:
            screen.blit(ufo_surf,ufo_rect)
            ufo_rect.x -= ufo_speed
            if ufo_rect.x < -150:
                prob = random.random()
                if prob < .5:
                    ufo_rect.x = 900
                else:
                    square2_speed *= -1
            if ufo_rect.x > 900: 
                prob = random.random()
                if prob < .5:
                    ufo_rect.x = -150
                else:
                    ufo_speed *= -1

        if player_rect.colliderect(square_rect) or player_rect.colliderect(square2_rect) or player_rect.colliderect(ufo_rect):
            game_active = False
            player_rect.x = 50
            square_rect.x = 700
            square_speed = 4
            square2_rect.x = 850
            square2_speed = 7
            ufo_rect.x = 900
            ufo_speed = 5.5
            
        if player_rect.colliderect(coin_rect):
            bonus_score += 3 
            randx = random.uniform(50, 750) // 1
            randy = random.uniform(100, 250) // 1
            coin_rect.x , coin_rect.y = randx, randy
        
        if score >= 50 and score < 100:
            current_level = 2
        elif score >= 100 and score < 150:
            current_level = 3
            square2_rect.x = 900
        elif score >= 150:
            current_level = 4
    else:
        HS_surf = game_font.render(f'High Score: {high_score}',False,(64,64,64))
        HS_rect = HS_surf.get_rect(center = (400,170))
        screen.blit(title_surf,title_rect)
        screen.blit(start_surf,start_rect)
        screen.blit(HS_surf,HS_rect)
    
    
    
    pygame.display.update()
    clock.tick(60)