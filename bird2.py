import math
import pygame
import pymunk
import pymunk.pygame_util

class Bird:
    def __init__(self, pos):
        self.in_slingshot = True
        self.mass = 10
        self.radius = 25
        # moment_for_circle args: mass, inner_radius, outer_radius, offset
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.radius, (0,0))
        self.body = pymunk.Body(self.mass, self.inertia)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius, (0,0))
        self.shape.elasticity = .8
        self.shape.friction = .8
        # Load the bird image
        self.image = pygame.image.load('assets/Red.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.shape.collision_type = 1

    def calculate_velocity(self, energy, theta):
        velocity = math.sqrt(2 * energy)
        vx = -velocity * math.cos(theta)
        vy = -velocity * math.sin(theta)
        self.body.velocity = pymunk.Vec2d(vx, vy)
