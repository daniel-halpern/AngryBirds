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
def calculateBirdPosition(slingshot, bird, game, dt):
    if bird.inSlingshot:
        stretch = calculateDistance(slingshot.pos, bird.pos)
        if calculateDistance(slingshot.pos, bird.pos) > slingshot.maxStretch:
            theta = calculateAngle(slingshot.pos, bird.pos)
            bird.pos = [slingshot.maxStretch * math.cos(theta) + slingshot.pos[0], 
                    slingshot.maxStretch * math.sin(theta) + slingshot.pos[1]]
            stretch = slingshot.maxStretch
        return stretch
    else:
        bird.pos = [bird.pos[0] + (bird.velocity[0] * dt) / game.pixelsPerMeter, 
                    bird.pos[1] - (bird.velocity[1] * dt) / game.pixelsPerMeter,]
        if bird.pos[1] > game.size[1]:
            bird.pos[1] = game.size[1]
            bird.velocity[1] = -bird.velocity[1] * game.energyLostMultiplier
            bird.velocity[0] = bird.velocity[0] * game.energyLostMultiplier

