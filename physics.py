# physics.py
import numpy as np
import pygame
from config import configuration as config

class body:
    cfg = None
    def __init__(self, mass, position, velocity, radius, color, name, others=None):
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.radius = radius
        self.color = color
        self.selected = False
        self.dragging = False
        self.trail = []
        self.new_trail_point = (self.position[0], self.position[1])
        self.acceleration = np.array([0.0, 0.0], dtype='float64')
        if others is not None:
            ax, ay = self.getAcceleration(others)
            self.acceleration = np.array([ax, ay], dtype='float64')
        if body.cfg is None:
            body.cfg = config()
    
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
        dx = (other.position[0] - self.position[0]) * body.cfg.distance_scale
        dy = (other.position[1] - self.position[1]) * body.cfg.distance_scale
        distance = np.sqrt(dx**2 + dy**2)
        if distance == 0:
            return 0,0
        force = body.cfg.G * other.mass * self.mass / distance**2
        fx = force * dx / distance
        fy = force * dy / distance
        return fx, fy
    def update_position(self, dt):
        scaled_dt = dt * body.cfg.time_scale
        self.position[0] += (self.velocity[0] * scaled_dt + 
                             (0.5 * self.acceleration[0] * (scaled_dt**2))) / body.cfg.distance_scale
        self.position[1] += (self.velocity[1] * scaled_dt + 
                             (0.5 * self.acceleration[1] * (scaled_dt**2))) / body.cfg.distance_scale
        self.new_trail_point = (self.position[0], self.position[1])
    
    def update_velocity(self, new_acceleration, dt):
        scaled_dt = dt * (body.cfg.time_scale)
        self.velocity[0] += 0.5 * (self.acceleration[0] + new_acceleration[0]) * scaled_dt
        self.velocity[1] += 0.5 * (self.acceleration[1] + new_acceleration[1]) * scaled_dt
        self.acceleration = new_acceleration
        self.trail.append(self.new_trail_point)
        if len(self.trail) > 500:
            self.trail.pop(0)
        
    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, (255,0,0), (self.position[0], self.position[1]), self.radius+2, 2)
            pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.radius)
        else:
            pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.radius)
        self.draw_trail(screen)
    
    def draw_trail(self, screen):
        if len(self.trail) > 2:
            pygame.draw.lines(screen, self.color, False, self.trail, 1)
    def get_velocity_magnitude(self):
        return np.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
    def get_acceleration_magnitude(self):
        return np.sqrt(self.acceleration[0]**2 + self.acceleration[1]**2)
    
    def set_color(self, color_name):
        colormap = {"WHITE" : (255, 255, 255),
        "RED": (255, 0, 0),
        "GREEN" :(0, 255, 0),
        "BLUE" : (0, 0, 255),
        "YELLOW" : (255, 255, 0)}

        if isinstance(color_name, str) and color_name.upper() in colormap:
            self.color = colormap[color_name.upper()]
        elif isinstance(color_name, tuple) and len(color_name) == 3:
            self.color = color_name
    
    def get_color(self):
        reverseColormap = {(255, 255, 255): "WHITE",
        (255, 0, 0): "RED",
        (0, 255, 0): "GREEN",   
        (0, 0, 255): "BLUE",
        (255, 255, 0): "YELLOW"}

        if self.color in reverseColormap:
            return reverseColormap[self.color]
        else:
            return str(self.color)
        
    def get_potential_energy(self, bodies):
        U = 0 
        for body1 in bodies:
            if body1 != self:
                dx = (self.position[0] - body1.position[0]) * body.cfg.distance_scale
                dy = (self.position[1] - body1.position[1]) * body.cfg.distance_scale
                distance = np.sqrt(dx**2 + dy**2)
                if distance != 0:
                    U -= body.cfg.G * self.mass * body1.mass / distance
        return U
    
    def kinetic_energy(self):
        return 0.5 * self.mass * (self.velocity[0]**2 + self.velocity[1]**2)

    @staticmethod
    def select_body(bodies, position):
        for b in bodies:
            dx = b.position[0] - position[0]
            dy = b.position[1] - position[1]
            distance = np.sqrt(dx**2 + dy**2)
            if distance <= b.radius:
                for other_b in bodies:
                    other_b.selected = False
                b.selected = not b.selected
                return b
    
    @staticmethod
    def unselect_body(bodies):
        for b in bodies:
            if b.selected:
                b.selected = False

        