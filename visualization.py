#visualization.py

import pygame
import pygame_gui as pgui
from physics import body
from config import configuration as config
from simulation import Simulation as sim
from UIComponents import UIComponents
from UIHandler import UIEventHandler

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
        self.show_distance = False
        self.dragging_body = None
        self.drag_offset = (0, 0)
        self.show_vector_v = False
        self.show_vector_a = False
        self.show_grid = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.UIBuilder = UIComponents(self)
        self.UIHandler = UIEventHandler(self)  
        self.info_panel = self.UIBuilder.build()

    def vis_loop(self):
        while self.running:
            time_delta = 0
            if not self.pause:
                time_delta = self.clock.tick(60) / 1000.0
                self.simulation.append_elapsed_time(time_delta)  # seconds since last frame
            else:
                time_delta = self.clock.tick(60) / 1000.0

            self.screen.fill((0, 0, 0))
            if self.show_grid:
                self.cfg.draw_grid(self.screen)
            if self.show_distance:
                self.draw_all_distances()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False   
                self.UIHandler.handle(event)
                self.Uim.process_events(event)   
            b = self.simulation.getSelectedbody()
            if b is not None:
                self.UIBuilder.update_selected_body_panel(b)
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

    def mouse_over_ui(self):
        return self.Uim.get_hovering_any_element()
    
    def draw_distance(self, screen, b1, b2):
        x1, y1 = b1.position
        x2, y2 = b2.position

        # Draw line
        pygame.draw.line(screen, (120, 120, 120), (x1, y1), (x2, y2), 1)

        # Distance in sim units
        dx = x2 - x1
        dy = y2 - y1
        sim_dist = (dx**2 + dy**2)**0.5

        # Convert to meters
        dist_m = sim_dist * self.cfg.distance_scale
        text = f"{dist_m:.2e} m"

        # Midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        # Perpendicular offset
        length = max(sim_dist, 1)
        nx = -dy / length
        ny = dx / length

        offset = 18
        label_x = mid_x + nx * offset
        label_y = mid_y + ny * offset

        # Push away from bodies
        label_x += 10 if nx >= 0 else -10
        label_y += 10 if ny >= 0 else -10

        # Render
        font = pygame.font.SysFont("consolas", 14)
        surf = font.render(text, True, (200, 200, 200))
        rect = surf.get_rect(center=(label_x, label_y))

        screen.blit(surf, rect)
    
    def draw_all_distances(self):
        n = len(self.bodies)
        for i in range(n):
            for j in range(i + 1, n):
                self.draw_distance(
                    self.screen,
                    self.bodies[i],
                    self.bodies[j]
                )

    


if __name__ == "__main__":
    viz = Visualization()
    viz.vis_loop()   