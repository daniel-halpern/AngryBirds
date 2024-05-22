import pygame
from bird import *
from slingshot import *
from player import *
from game import *
from helpers import *
import time

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1400, 1000))
clock = pygame.time.Clock()
running = True

# Game setup
slingshot = Slingshot([200,600])
bird = Bird(slingshot.pos, 10)
game = Game()

while running:
    dt = clock.tick(60)
    # Events
    # Closes on red x pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouseButtonsPressed = pygame.mouse.get_pressed()
    # Calculates where the bird should be drawn
    # In this case, the player is pulling back the slingshot
    if mouseButtonsPressed[0] and bird.inSlingshot:
        mousePos = pygame.mouse.get_pos()
        bird.pos = mousePos
        slingshot.stretch = calculateBirdPosition(slingshot, bird, game, dt)
    # In this case, the player just let go the slingshot
    elif bird.inSlingshot and abs(slingshot.stretch) > 0:
        bird.inSlingshot = False
        bird.startTime = time.time()
        bird.calculateVelocity(slingshot.springPotentialEnergy(), 
                               calculateAngle(slingshot.pos, bird.pos))
    # In this case, the bird already has some initial velocity
    elif bird.velocity != [0, 0]: # Bird is launched
        bird.recalculateVelocity()
        calculateBirdPosition(slingshot, bird, game, dt)


    # Drawing
    screen.fill("aqua")
    pygame.draw.circle(screen, "blue", slingshot.pos, 50) # The slingshot size
    pygame.draw.circle(screen, "red", bird.pos, 25) # The bird
    pygame.display.flip()

pygame.quit()