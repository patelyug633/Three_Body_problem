import pygame 
import sys
import numpy as np

class Body:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.vx = 0
        self.vy = 0

    def update(self, fx, fy, dt):
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 50)

    def getposition(self):
        return self.x, self.y

G = 0.1     # Modified Gravitational constant for simulation purposes
bodies = [] # List to hold all celestial bodies in the simulation
screen = pygame.display.set_mode((1600, 1200))  # Screen dimensions
