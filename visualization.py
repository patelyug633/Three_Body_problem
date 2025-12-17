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
                self.handle_Mouseclick(event)
                self.handle_Keypress(event)

            if self.pause:
                self.draw_bodies()
            else:
                self.simulation.run_simulation(self.bodies)
                self.draw_bodies()

            pygame.display.flip()
        pygame.quit()

    def handle_Mouseclick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            b = body.select_body(self.bodies, (x,y), self.screen)
            if b is not None:
                print(f"Selected body at position: {b.position} with mass: {b.mass}")
            else:
                x_vel, y_vel = self.cfg.get_PerfectOrbit_velocity(5e24, (x,y))
                self.bodies.append(body(10, (x,y), (x_vel,y_vel), 5, (255,0,0), self.bodies))
    
    def handle_Keypress(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for b in self.bodies:
                    if b.selected:
                        self.bodies.remove(b)
            if event.key == pygame.K_a:
                self.bodies.append(body(5e24, (320,240), (0,0), 25,(0,0,255), self.bodies))
            if event.key == pygame.K_SPACE:
                self.pause = not self.pause
            if event.key == pygame.K_ESCAPE:
                self.running = False
               
