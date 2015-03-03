from os import curdir, pardir
from os.path import join as o_p_join
import Base.Basics as bB # para llamar a las variables
from Base.Basics import *
from Base.Logics import *
from Base.Dibujar_Sprites import *
import pygame, sys, time, random
from pygame.locals import *

# set up pygame
def main():
    pygame.init()
    mainClock = pygame.time.Clock()
    # set up the window
    WINDOWWIDTH = 900
    WINDOWHEIGHT = 600
    windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Juego de prueba alfa 0.1')

    # set up the colors
    # BLACK = (0, 0, 0)
    # set up the block data structure
    playerImage = pygame.image.load(o_p_join(curdir, 'data/img' ,'a_w_stand.png'))
    player = playerImage.get_rect()
    # playerStretchedImage = pygame.transform.scale(playerImage,(40, 40))
    playerStretchedImage = playerImage
    foodImage = pygame.image.load(o_p_join(curdir, 'data/img' ,'diamond.bmp'))
    foods = []
    for i in range(20):
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 20), random.randint(0, WINDOWHEIGHT - 20), playerStretchedImage.get_size()[0], playerStretchedImage.get_size()[1]))
    foodCounter = 0
    NEWFOOD = 40
    playerImage = pygame.image.load(o_p_join(curdir, 'data/img' ,'a_w_stand.png'))
    bombImg = pygame.image.load(o_p_join(curdir, 'data/img' ,'bomb01.bmp'))
    bomb = bombImg.get_rect()
    bomb.move_ip(200,200)
    # set up keyboard variables
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False
    MOVESPEED = 6
    # set up music
    pickUpSound = pygame.mixer.Sound('shot.wav')
    pygame.mixer.music.load(o_p_join(curdir, 'data/sound' ,'gooback.wav'))
    pygame.mixer.music.play(-1, 0.0)
    musicPlaying = True
    # run the game loop
    while True:
        # check for the QUIT event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # change the keyboard variables
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                if event.key == ord('x'):
                    player.top = random.randint(0,WINDOWHEIGHT - player.height)
                    player.left = random.randint(0,WINDOWWIDTH - player.width)
                if event.key == ord('m'):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying
            if event.type == MOUSEBUTTONUP:
                foods.append(pygame.Rect(event.pos[0] - 10, event.pos[1] - 10, 20, 20))
        foodCounter += 1
        if foodCounter >= NEWFOOD:
            # add new food
            foodCounter = 0
            foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - 20), random.randint(0, WINDOWHEIGHT - 20), 20, 20))
        # draw the black background onto the surface
        windowSurface.fill(BLACK)
        # move the player
        if moveDown and player.bottom < WINDOWHEIGHT:
            player.top += MOVESPEED
        if moveUp and player.top > 0:
            player.top -= MOVESPEED
        if moveLeft and player.left > 0:
            player.left -= MOVESPEED
        if moveRight and player.right < WINDOWWIDTH:
            player.right += MOVESPEED
        # draw the block onto the surface
        windowSurface.blit(playerStretchedImage, player)
        # check if the block has intersected with any food squares.
        for food in foods[:]:
            if player.colliderect(food):
                foods.remove(food)
                player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
                playerStretchedImage = pygame.transform.scale(playerImage, (player.width, player.height))
                if musicPlaying:
                    pickUpSound.play()
        # draw the food
        for food in foods:
            windowSurface.blit(foodImage, food[:2])
        # draw the window onto the screen
        windowSurface.blit(bombImg, bomb)
        pygame.display.update()
        mainClock.tick(40)
        
if __name__ == '__main__':
    main()
