#visualization.py

import pygame
import pygame_gui as pgui
from physics import body
from config import configuration as config
from simulation import Simulation as sim
from UIcomponents.UIComponents import UIComponents
from UIcomponents.UIHandler import UIEventHandler


class VisualizationError(Exception):
    pass
class Visualization:
    pygame.init()
    def __init__(self):
        self.screen_HW = (1320, 720)
        self.screen = pygame.display.set_mode(self.screen_HW)
        self.simulation = sim(self)
        self.cfg = self.simulation.cfg
        self.Uim = pgui.UIManager(self.screen_HW, 'theme.json')
        self.bodies = self.simulation.bodies
        self.pause = True
        self.input_mode = None
        self.dragging_body = None
        self.drag_offset = (0, 0)
        self.show_vector_v = False
        self.show_vector_a = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.UIBuilder = UIComponents(self.Uim, self.screen_HW)
        self.info_panel = self.UIBuilder.build()
        self.UI_handler = UIEventHandler(self)       

    # Keep it !
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
                self.UI_handler.handle(event)      
                self.handle_Mouseclick(event)
                self.Uim.process_events(event)   
            
            self.Uim.update(time_delta)

            if self.pause:
                self.draw_bodies()
                self.draw_target_cursor()
            else:
                self.simulation.run_simulation()
                self.draw_bodies()
                self.draw_target_cursor()

                
            self.Uim.draw_ui(self.screen)

            pygame.display.flip()
        pygame.quit()
            
    # Keep basic, move the rest to simulation.py 
    def handle_Mouseclick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < 300:
                if self.input_mode is not None:
                    self.input_mode = None
                    self.info_panel.elements["add_sat"].unselect()
                    self.info_panel.elements["add_cen"].unselect()
                return
            self.input_mode = self.simulation.handle_click((x, y), self.input_mode)
    
    # Keep it !
    def draw_bodies(self):
        for b in self.bodies:
            b.draw(self.screen)
            if self.show_vector_v:
                self.draw_velocity_vector(b,30)
            if self.show_vector_a:
                self.draw_acceleration_vector(b,30)
    # Keep it !
    def draw_velocity_vector(self, body, maxLen = 50):
        vel_mag = body.get_velocity_magnitude()
        scale = 0
        if vel_mag < 0.0001:
            return
        scale = min(1.0, maxLen / vel_mag)

        end_pos = (body.position[0] + body.velocity[0] * scale,
                   body.position[1] + body.velocity[1] * scale)
        pygame.draw.line(self.screen, (0, 255, 0), (body.position[0], body.position[1]), end_pos, 2)

    #Keep it !
    def draw_acceleration_vector(self, body, maxLen = 100):
        acc_mag = body.get_acceleration_magnitude()
        scale = 0
        if acc_mag < 0.0001:
            return
        scale = maxLen / acc_mag
        end_pos = (body.position[0] + body.acceleration[0] * scale,
                   body.position[1] + body.acceleration[1] * scale)
        pygame.draw.line(self.screen, (255, 0, 0), (body.position[0], body.position[1]), end_pos, 2)
    
    def draw_target_cursor(self):
        if self.input_mode is None:
            return
        x, y = pygame.mouse.get_pos()
        if x < 300:
            return

        color = (0, 255, 0) if self.input_mode == "ADD_SATELLITE" else (255, 255, 0)

        pygame.draw.circle(self.screen, color, (x, y), 15, 2)
        pygame.draw.circle(self.screen, color, (x, y), 4, 2)
        pygame.draw.line(self.screen, color, (x - 20, y), (x + 20, y), 1)
        pygame.draw.line(self.screen, color, (x, y - 20), (x, y + 20), 1)

            

if __name__ == "__main__":
    viz = Visualization()
    viz.vis_loop()   
