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
def force(body1, body2):
    dx = body2.x - body1.x
    dy = body2.y - body1.y
    distance = (dx**2 + dy**2) ** 0.5
    if distance == 0:
        return 0, 0
    F = G * body1.mass * body2.mass / distance**2
    theta = np.arctan2(dy, dx)
    Fx = F * np.cos(theta)
    Fy = F * np.sin(theta)
    return Fx, Fy

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Three Body Problem Simulation")
clock = pygame.time.Clock()
G = 0.1  # Gravitational constant
bodies = []


running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            mass = 100000 + np.random.randint(900000)
            color = (np.random.randint(256), 255, 255)
            bodies.append(Body(x, y, mass, color))
    
    for body in bodies:
        fx_total, fy_total = np.random.randint(100), np.random.randint(20)
        for other_body in bodies:
            if body != other_body:
                fx, fy = force(body, other_body)
                fx_total += fx
                fy_total += fy
        body.update(fx_total, fy_total, 0.1)
        print(body.getposition())
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()


