import pygame
# from simulation import run_simulation
from physics import body
from config import configuration as config
from simulation import Simulation as sim

class VisualizationError(Exception):
    pass
class Visualization:
    pygame.init()
    def __init__(self):
        self.screen_HW = (640, 480)
        self.screen = pygame.display.set_mode(self.screen_HW)
        self.simulation = sim()
        self.cfg = config()
        self.bodies = self.cfg.bodies
        self.pause = True
        self.running = True
        self.clock = pygame.time.Clock()
    def draw_bodies(self):
        for b in self.bodies:
            b.draw(self.screen)
    def vis_loop(self):
        while self.running:
            if not self.pause:
                self.simulation.append_elapsed_time(self.clock.tick(60) / 1000)  # seconds since last frame
            else:
                self.clock.tick(60)

            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x_vel, y_vel = self.cfg.get_PerfectOrbit_velocity(5e24, (x,y))
                    self.bodies.append(body(10, (x,y), (x_vel,y_vel), 5, (255,0,0), self.bodies))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.bodies.append(body(5e24, (320,240), (0,0), 25,(0,0,255), self.bodies))
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause

            if self.pause:
                self.draw_bodies()
            else:
                self.simulation.run_simulation(self.bodies)
                self.draw_bodies()

            pygame.display.flip()
        def handel_key(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.bodies.append(body(5e24, (320,240), (0,0), 25,(0,0,255), self.bodies))
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()
        def handel_mouse(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.pause:
                    body().isbody(self.bodies, (x,y))
                x_vel, y_vel = self.cfg.get_PerfectOrbit_velocity(5e24, (x,y))
                self.bodies.append(body(10, (x,y), (x_vel,y_vel), 5, (255,0,0), self.bodies))
            
    # def draw_bodies(screen, bodies):
#     for b in bodies:
#         b.draw(screen)

# def vis_loop():
#     screen = pygame.display.set_mode((640, 480), )
#     running = True
#     clock = pygame.time.Clock()
#     bodies = []
#     simulation = sim()
#     pause = True
#     while running:
#         if not pause:
#             simulation.append_elapsed_time(clock.tick(60) / 1000)  # seconds since last frame
#         else:
#             clock.tick(60)

#         screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 x, y = event.pos
#                 x_vel, y_vel = config().get_PerfectOrbit_velocity(5e24, (x,y))
#                 bodies.append(body(10, (x,y), (x_vel,y_vel), 5, (255,0,0), bodies))
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_a:
#                     bodies.append(body(5e24, (320,240), (0,0), 25,(0,0,255), bodies))
#                 if event.key == pygame.K_SPACE:
#                     pause = not pause

#         if pause:
#             draw_bodies(screen, bodies)
#         else:
#             simulation.run_simulation(bodies)
#             draw_bodies(screen, bodies)

#         pygame.display.flip()
#     pygame.quit()
