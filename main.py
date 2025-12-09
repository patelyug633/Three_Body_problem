import pygame
import sys
import numpy as np

G = 0.1     #Modified gravitational constant
Screen_width, Screen_height = 640, 480
bodies = []
mass_increment = 100
velocity_increment = 10
class Body:
    def __init__(self, mass, position, momentum, radius, color):
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.momentum = np.array(momentum, dtype='float64')
        self.radius = radius
        self.color = color
    
    def force(self, other):
        Gforce = (G * self.mass * other.mass) // ((self.position[0] - other.position[0])**2) + ((self.position[1] - other.position[1])**2)
        o_x, o_y = other.getPosition()
        theta = np.arctan(o_y/o_x)
        force_y = Gforce*np.sin(theta)
        force_x = Gforce*np.cos(theta)
        return force_x, force_y

    def update(self, others, dt):
        fx, fy = 0, 0
        for other in others:
            if other != self:
                fx_other, fy_other = self.force(other)
                fx += fx_other
                fy += fy_other
        ax = fx/self.mass
        ay = fy/self.mass
        self.momentum[0] += ax * dt
        self.momentum[1] += ay * dt
        self.position[0] += self.momentum[0] / self.mass * dt
        self.position[1] += self.momentum[1] / self.mass * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.getPosition(), 50)

    def getPosition(self):
        return self.position[0], self.position[1]
    
    def traceOrbit(self):
        print("tracing orbit")
    
    def getMassLable(self):
        return f'Mass: {self.mass}'

def scree_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            buttonclicked = ButtonControl(x, y, 50)
            if not buttonclicked:
                bodies.append(Body(1000, (x, y), (0, 0), 10, (255, 255, 255)))

            
    return True

def ButtonControl(x, y, radius):
    obj_x, obj_y = Screen_width // 6, Screen_height - 100
    distance_mass = np.sqrt((x - obj_x)**2 + (y - obj_y)**2)
    if distance_mass <= radius:
        print("Mass button clicked")
        return True
    obj_x, obj_y = Screen_width // 3, Screen_height - 100
    distance_mass = np.sqrt((x - obj_x)**2 + (y - obj_y)**2)
    if distance_mass <= radius:
        print("Velocity button clicked")
        return True
    obj_x, obj_y = Screen_width // 2, Screen_height - 100
    distance_mass = np.sqrt((x - obj_x)**2 + (y - obj_y)**2)
    if distance_mass <= radius:
        print("Angle button clicked")
        return True
    return False

def draw_buttons(screen):
    pygame.draw.circle(screen, (0, 255, 0), (Screen_width // 6, Screen_height - 100),50)
    pygame.draw.circle(screen, (0, 255, 255), (Screen_width // 3, Screen_height - 100),50)
    pygame.draw.circle(screen, (255, 255, 0), (Screen_width // 2, Screen_height - 100),50)
    text_surface = base_font.render(user_mass, True, (0, 0, 0))
    screen.blit(text_surface, (Screen_width // 6 - 20, Screen_height - 100))
    text_surface = base_font.render(user_velocity, True, (0, 0, 0))
    screen.blit(text_surface, (Screen_width // 3 - 21, Screen_height - 100))
    text_surface = base_font.render(user_velocity, True, (0, 0, 0))
    screen.blit(text_surface, (Screen_width // 2 - 21, Screen_height - 100))
    
pygame.init()
screen = pygame.display.set_mode((Screen_width, Screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 24)
running = True
user_mass = 'mass'
user_velocity = 'velocity'

while running:
    dt = clock.tick(60) / 1000.0
    running  = scree_loop()
    draw_buttons(screen)
    for body in bodies:
        body.update(bodies, dt)
        body.draw(screen)
    pygame.display.flip()
    clock.tick(60)