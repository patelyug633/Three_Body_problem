import pygame
import pygame_gui as pgui
from physics import body
from config import configuration as config
from simulation import Simulation as sim


class VisualizationError(Exception):
    pass
class Visualization:
    pygame.init()
    def __init__(self):
        self.screen_HW = (960, 720)
        self.screen = pygame.display.set_mode(self.screen_HW)
        self.simulation = sim()
        self.cfg = config()
        self.Uim = pgui.UIManager(self.screen_HW)
        self.bodies = self.cfg.bodies
        self.pause = True
        self.show_vectors = True
        self.running = True
        self.clock = pygame.time.Clock()
    def draw_bodies(self):
        for b in self.bodies:
            b.draw(self.screen)
            if self.show_vectors:
                self.draw_velocity_vector(b,30)
                self.draw_acceleration_vector(b,30)
    def draw_velocity_vector(self, body, maxLen = 50):
        vel_mag = body.get_velocity_magnitude()
        scale = 0
        if vel_mag < 0.0001:
            return
        scale = min(1.0, maxLen / vel_mag)

        end_pos = (body.position[0] + body.velocity[0] * scale,
                   body.position[1] + body.velocity[1] * scale)
        pygame.draw.line(self.screen, (0, 255, 0), (body.position[0], body.position[1]), end_pos, 2)
        
    def draw_acceleration_vector(self, body, maxLen = 100):
        acc_mag = body.get_acceleration_magnitude()
        scale = 0
        if acc_mag < 0.0001:
            return
        scale = min(1.0, maxLen / acc_mag)
        scale = maxLen / acc_mag
        end_pos = (body.position[0] + body.acceleration[0] * scale,
                   body.position[1] + body.acceleration[1] * scale)
        pygame.draw.line(self.screen, (255, 0, 0), (body.position[0], body.position[1]), end_pos, 2)

    def vis_loop(self):
        while self.running:
            time_delta = 0
            if not self.pause:
                time_delta = self.clock.tick(60) / 1000.0
                self.simulation.append_elapsed_time(time_delta)  # seconds since last frame
            else:
                time_delta = self.clock.tick(60) / 1000.0

            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_Mouseclick(event)
                self.handle_Keypress(event)
                self.Uim.process_events(event)
            
            self.Uim.update(time_delta)

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
            b = body.select_body(self.bodies, (x,y))
            if b is not None:
                print(f"Selected body at position: {b.position} with mass: {b.mass}")
            else:
                x_vel, y_vel = self.cfg.get_PerfectOrbit_velocity(5e24, (x,y), (self.screen_HW[0]/2, self.screen_HW[1]/2))
                self.bodies.append(body(10, (x,y), (x_vel,y_vel), 5, (255,0,0), self.bodies))
    
    def handle_Keypress(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for b in self.bodies:
                    if b.selected:
                        self.bodies.remove(b)
            if event.key == pygame.K_a:
                self.bodies.append(body(5e24, (self.screen_HW[0]/2, self.screen_HW[1]/2), (0,0), 25,(0,0,255), self.bodies))
            if event.key == pygame.K_SPACE:
                self.pause = not self.pause
            if event.key == pygame.K_ESCAPE:
                self.running = False
            if event.key == pygame.K_v:
                self.show_vectors = not self.show_vectors

if __name__ == "__main__":
    viz = Visualization()
    viz.vis_loop()   
