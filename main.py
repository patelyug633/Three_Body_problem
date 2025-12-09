import pygame
import sys
import numpy as np

# --- Simulation constants ---
G = 6.67430e-11        # Real gravitational constant
distance_scale = 1e6   # 1 pixel = 1,000,000 meters
time_scale = 60*30  # 1 frame = 1 day

Screen_width, Screen_height = 640, 480

# --- Body class ---
class Body:
    def __init__(self, mass, position, velocity, radius, color):
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.radius = radius
        self.color = color
    
    def force(self, other):
        # Compute vector from self to other in meters
        dx = (other.position[0] - self.position[0]) * distance_scale
        dy = (other.position[1] - self.position[1]) * distance_scale
        distance = np.sqrt(dx**2 + dy**2)
        if distance == 0:
            return 0, 0
        force_magnitude = G * self.mass * other.mass / distance**2
        fx = force_magnitude * dx / distance
        fy = force_magnitude * dy / distance
        return fx, fy

    def update(self, others, dt):
        fx_total, fy_total = 0, 0
        for other in others:
            if other != self:
                fx, fy = self.force(other)
                fx_total += fx
                fy_total += fy
        # Acceleration in m/s^2
        ax = fx_total / self.mass
        ay = fy_total / self.mass
        # Update velocity (m/s)
        self.velocity[0] += ax * dt * time_scale
        self.velocity[1] += ay * dt * time_scale
        # Update position (pixels)
        self.position[0] += self.velocity[0] * dt * time_scale / distance_scale
        self.position[1] += self.velocity[1] * dt * time_scale / distance_scale

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.getPosition(), self.radius)

    def getPosition(self):
        return int(self.position[0]), int(self.position[1])

def event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        # Add body with mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Give random initial velocity for visible motion
            vx = 550 #np.random.uniform(-500, 500)  # m/s
            vy = 550 #np.random.uniform(-500, 500)  # m/s
            bodies.append(Body(
                mass=10e22,  # smaller mass for visible motion
                position=(x, y),
                velocity=(vx, vy),
                radius=5,
                color=(255, 0, 0)
            ))
        # Add large central body with key 'a'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                bodies.append(Body(
                    mass=5.972e24,  # Earth-mass
                    position=(Screen_width//2, Screen_height//2),
                    velocity=(0, 0),
                    radius=15,
                    color=(0, 0, 255)
                ))
    return True
# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("Three Body Problem Simulation")
clock = pygame.time.Clock()

bodies = []
running = True

# --- Main loop ---
while running:
    screen.fill((0, 0, 0))  # Clear screen
    running = event_loop()
    
    # Update and draw bodies
    for body in bodies:
        body.update(bodies, dt=1)
        body.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
