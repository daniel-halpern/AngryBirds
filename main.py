import pygame
from bird import *
from slingshot import *
from player import *
from game import *
from helpers import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 400))
running = True

# Game setup
slingshot = Slingshot([200,200])
bird = Bird(slingshot.pos)
game = Game()
while running:
    # Events
    # Closes on red x pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouseButtonsPressed = pygame.mouse.get_pressed()
    # Calculate where the bird should be drawn if in slingshot
    if mouseButtonsPressed[0] and bird.inSlingshot:
        mousePos = pygame.mouse.get_pos()
        bird.pos = calculateBirdPosition(game, slingshot, mousePos)

    # Drawing
    screen.fill("aqua")
    pygame.draw.circle(screen, "blue", slingshot.pos, 100) # The slingshot size
    pygame.draw.circle(screen, "red", bird.pos, 40) # The bird
    pygame.display.flip()

pygame.quit()