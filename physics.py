import numpy as np
import pygame
from config import G, distance_scale, time_scale


class body:
    def __init__(self, mass, position, velocity, radius, color, others=None):
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.radius = radius
        self.color = color
        self.trail = []
        self.new_trail_point = (self.position[0], self.position[1])
        self.acceleration = np.array([0.0, 0.0], dtype='float64')
        if others is not None:
            ax, ay = self.getAcceleration(others)
            self.acceleration = np.array([ax, ay], dtype='float64')
    
    def getAcceleration(self, others):
        fx, fy = 0,0
        for other in others:
            if other != self:
                fxi, fyi = self.force(other)
                fx += fxi
                fy += fyi
        ax = fx / self.mass
        ay = fy / self.mass
        return ax, ay
    
    def force(self,other):
        dx = (other.position[0] - self.position[0]) * distance_scale
        dy = (other.position[1] - self.position[1]) * distance_scale
        distance = np.sqrt(dx**2 + dy**2)
        if distance == 0:
            return 0,0
        force = G * other.mass * self.mass / distance**2
        fx = force * dx / distance
        fy = force * dy / distance
        return fx, fy
    def update_position(self, dt):
        scaled_dt = dt * time_scale
        self.position[0] += (self.velocity[0] * scaled_dt + 
                             (0.5 * self.acceleration[0] * (scaled_dt**2))) / distance_scale
        self.position[1] += (self.velocity[1] * scaled_dt + 
                             (0.5 * self.acceleration[1] * (scaled_dt**2))) / distance_scale
        self.new_trail_point = (self.position[0], self.position[1])
    
    def update_velocity(self, new_acceleration, dt):
        scaled_dt = dt * time_scale
        self.velocity[0] += 0.5 * (self.acceleration[0] + new_acceleration[0]) * scaled_dt
        self.velocity[1] += 0.5 * (self.acceleration[1] + new_acceleration[1]) * scaled_dt
        self.acceleration = new_acceleration
        self.trail.append(self.new_trail_point)
        if len(self.trail) > 500:
            self.trail.pop(0)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.radius)
        self.draw_trail(screen)
    
    def draw_trail(self, screen):
        if len(self.trail) > 2:
            pygame.draw.lines(screen, self.color, False, self.trail, 1)

