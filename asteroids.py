from urllib.request import HTTPDigestAuthHandler
from weakref import ref
import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Into the Void")

WHITE = (255, 255, 255)
RED = (255, 0 ,0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)

FALCON_HEIGHT, FALCON_WIDTH = 60, 60
ast_size = 50
juice_size = 25

VEL = 10

FALCON_IMAGE = pygame.image.load(os.path.join('resources', 'mil_falcon.png'))
FALCON = pygame.transform.scale(FALCON_IMAGE, (FALCON_WIDTH, FALCON_HEIGHT) )

FALCON_HIT = pygame.USEREVENT + 1
JUICE_CONSUMED = pygame.USEREVENT + 2

SCORE_FONT = pygame.font.SysFont('comicsans', 20)

def draw_window(asteroids, juices, MILLENIUM_FALCON, HEALTHBAR, SCORE):
    WIN.fill(WHITE)
    WIN.blit(FALCON, (MILLENIUM_FALCON.x, MILLENIUM_FALCON.y) )
    
    for asteroid in asteroids:
        pygame.draw.rect(WIN, BLACK, asteroid)
    
    for juice in juices:
        pygame.draw.rect(WIN, PURPLE, juice)

    pygame.draw.rect(WIN, RED, HEALTHBAR)
    score_text = SCORE_FONT.render("Score: "+str(SCORE),1, RED)
    WIN.blit(score_text, (20, 40))
    pygame.display.update()

def FALCON_movement(keys_pressed, MILLENIUM_FALCON):
    if keys_pressed[pygame.K_LEFT] and MILLENIUM_FALCON.x > 0:
        MILLENIUM_FALCON.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and MILLENIUM_FALCON.x + MILLENIUM_FALCON.width < WIDTH:
        MILLENIUM_FALCON.x += VEL
    #if keys_pressed[pygame.K_UP] and MILLENIUM_FALCON.y > 0:
       # MILLENIUM_FALCON.y -= VEL
    #if keys_pressed[pygame.K_DOWN] and MILLENIUM_FALCON.y + MILLENIUM_FALCON.height < HEIGHT:
       # MILLENIUM_FALCON.y += VEL


def asteroid_movement(asteroids,keys_pressed, ast_X_VEL):
    for i in range(len(asteroids)-1):
        if asteroids[i].y > HEIGHT:
          asteroids[i].x,  asteroids[i].y = random.randint(0,WIDTH-50), -50
          ast_X_VEL[i] = 0    
        asteroids[i].y += random.randint(2,5)

       # if asteroids[i].colliderect(MILLENIUM_FALCON):
           # asteroids[i].x, asteroids[i].y = random.randint(0,WIDTH-juice_size), -juice_size-100
           # ast_X_VEL[i] = 0
            

        if keys_pressed[pygame.K_UP]:
            asteroids[i].y += random.randint(2,3)+1

        if keys_pressed[pygame.K_DOWN]:
            asteroids[i].y += -random.randint(2,3)+1

        asteroids[i].x += ast_X_VEL[i]
        
        
def juice_movement(juices,keys_pressed, juice_X_VEL, MILLENIUM_FALCON, score):
    for i in range(len(juices)-1):
        if juices[i].y > HEIGHT:
            juices[i].x, juices[i].y = random.randint(0,WIDTH-juice_size), -juice_size
            juice_X_VEL[i] = 0
        juices[i].y += random.randint(2,3)

        if juices[i].colliderect(MILLENIUM_FALCON):
            juices[i].x, juices[i].y = random.randint(0,WIDTH-juice_size), -juice_size-100
            juice_X_VEL[i] = 0
            score[0] += 100

        if keys_pressed[pygame.K_UP]:
            juices[i].y += random.randint(2,3)+1
        
        if keys_pressed[pygame.K_DOWN]:
            juices[i].y += -random.randint(2,3)+1

        juices[i].x +=juice_X_VEL[i]

       

def Falcon_collisions(MILLENIUM_FALCON, asteroids, juices, ast_X_VEL, collid_track, HEALTH):
    #for i in range(len(juices)-1):
     #   if MILLENIUM_FALCON.colliderect(juices[i]):
         #   pygame.event.post(pygame.event.Event(JUICE_CONSUMED))
    i = 0
    for asteroid in asteroids:
        if MILLENIUM_FALCON.colliderect(asteroid) and collid_track[i] == False:
            print("HIT")
            HEALTH -= 25
            collid_track[i] = True
        
        if MILLENIUM_FALCON.colliderect(asteroid) == False:
            collid_track[i] = False
        
        i += 1
        return HEALTH

def object_collisions(asteroids, juices,ast_X_VEL , juice_X_VEL, MILLENIUM_FALCON):
    for i in range(len(asteroids)-1):
        for j in range(len(asteroids)-1):
            if i != j:
                if asteroids[i].colliderect(asteroids[j]):
                    if asteroids[i].x < asteroids[j].x:
                        ast_X_VEL[i]=-1
                        ast_X_VEL[j]=1
                    else:
                        ast_X_VEL[i]=1
                        ast_X_VEL[j]=-1
    
    for i in range(len(juices)-1):
        for j in range(len(asteroids)-1):
            if juices[i].colliderect(asteroids[j]):
                if juices[i].x < asteroids[j].x+ast_size/2:
                    juice_X_VEL[i]=-1
                else:
                    juice_X_VEL[i]=1      

def score_implem(score, keys_pressed):
    if keys_pressed[pygame.K_UP]:
            score[0] += 1

    if keys_pressed[pygame.K_DOWN]:
            score[0] -= 1               
    

def main():
    score = [0]
    clock = pygame.time.Clock()
    run =  True
    ast_X_VEL = [0,0,0,0,0,0,0,0]
    juice_X_VEL = [0,0,0,0]
    collid_track=[False, False, False, False, False, False, False, False]
    MILLENIUM_FALCON = pygame.Rect(WIDTH/2-FALCON_WIDTH/2,HEIGHT-100,FALCON_WIDTH,FALCON_HEIGHT)

    HEALTH = 100
    HEALTHBAR = pygame.Rect(20,20,HEALTH,10)
    
    juices = []
    asteroids = []
    for i in range(3) :
       asteroid = pygame.Rect(random.randint(0,WIDTH-ast_size), -ast_size ,ast_size , ast_size)
       asteroids.append(asteroid)

    for i in range(2) :
       juice = pygame.Rect(random.randint(0,WIDTH-juice_size), -juice_size ,juice_size ,juice_size)
       juices.append(juice)
    
    current_ticks = pygame.time.get_ticks()
    while run:
        score[0] += 2
        
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        
        if pygame.time.get_ticks() - current_ticks > 5000 and pygame.time.get_ticks() < 30000:
            asteroid = pygame.Rect(random.randint(0,WIDTH-ast_size), -ast_size ,ast_size , ast_size)
            asteroids.append(asteroid)
            if pygame.time.get_ticks() < 10000:
                juice = pygame.Rect(random.randint(0,WIDTH-juice_size), -juice_size ,juice_size ,juice_size)
                juices.append(juice)
    
            current_ticks = pygame.time.get_ticks()
        
        score_implem(score, keys_pressed)
        asteroid_movement(asteroids, keys_pressed, ast_X_VEL)
        object_collisions(asteroids, juices,ast_X_VEL, juice_X_VEL, MILLENIUM_FALCON)
        juice_movement(juices,keys_pressed,juice_X_VEL ,MILLENIUM_FALCON, score)
        FALCON_movement(keys_pressed, MILLENIUM_FALCON)
        HEALTH = Falcon_collisions(MILLENIUM_FALCON, asteroids, juices, ast_X_VEL, collid_track, HEALTH
        ,)
        #if event.type == FALCON_HIT:
           # HEALTH -= 25
        print(asteroids)
        if HEALTH <= 0:
            run = False
            print(score[0])
        HEALTHBAR = pygame.Rect(20,20,HEALTH,10)
        draw_window(asteroids,juices,MILLENIUM_FALCON, HEALTHBAR, score)


    pygame.quit

if __name__ == "__main__":
    main()