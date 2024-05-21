import math

# Simple distance calculation function
def calculateDistance(pos1, pos2):
    deltaX = pos1[0] - pos2[0]
    deltaY = pos1[1] - pos2[1]
    return math.sqrt(deltaX ** 2 + deltaY ** 2)

# Calculates the angle of pos2 around pos1 in radians
def calculateAngle(pos1, pos2):
    deltaX = pos2[0] - pos1[0]
    deltaY = pos2[1] - pos1[1]
    return math.atan2(deltaY, deltaX)

# Calculates bird position *in slingshot*
def calculateBirdPosition(game, slingshot, mousePos):
    birdPos = mousePos
    if calculateDistance(slingshot.pos, birdPos) > game.maxStretch:
        theta = calculateAngle(slingshot.pos, birdPos)
        birdPos = [game.maxStretch * math.cos(theta) + slingshot.pos[0], 
                   game.maxStretch * math.sin(theta) + slingshot.pos[1]]
    return birdPos
