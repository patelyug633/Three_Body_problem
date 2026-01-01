from physics import body
from config import configuration as config

class SimulationError(Exception):
    pass
class Simulation:
    def __init__(self):
        self.elapsed_time = 0.0
        self.cfg = config()
        self.is_cenBody_alone = None # To track if central body is only one in the simulation
        self.bodies = self.cfg.bodies
        
    def getConfig(self):
        return self.cfg


    def run_simulation(self):
        cfg = self.cfg
        F_dt = cfg.F_dt
        while self.elapsed_time >= F_dt:
            cfg.update(self.bodies)
            self.elapsed_time -= F_dt

        # return self.elapsed_time

    def get_elapsed_time(self):
        return self.elapsed_time
    
    def set_elapsed_time(self, time):
        self.elapsed_time = time

    def append_elapsed_time(self, time):
        self.elapsed_time += time

    def draw_bodies(self, screen, bodies):
        for b in bodies:
            b.draw(screen)

    def add_central_body(self, mass=5e24, position=(400, 300), velocity=(0, 0), radius=25, color=(255, 255, 0)):
        central_body = body(mass=mass, position=position, velocity=velocity, radius=radius, color=color)
        self.bodies.append(central_body)
        if self.is_cenBody_alone is None:
            self.is_cenBody_alone = central_body
        else:
            self.is_cenBody_alone = [self.is_cenBody_alone, central_body]
        return central_body

    def add_satellite_body(self, onPos, mass = 10, radius = 5, color = (255,0,0), velocity = None):
        if velocity is None and isinstance(self.is_cenBody_alone, body):
            velocity  = self.cfg.get_PerfectOrbit_velocity(self.is_cenBody_alone.mass, onPos, self.is_cenBody_alone.position)
        if velocity is None:
            velocity = (0,0)
        satellite = body(mass=mass, position=onPos, velocity=velocity, radius=radius, color=color)
        self.bodies.append(satellite)
        return satellite

    def handle_click(self, position):
        x, y = position
        b = body.select_body(self.bodies, (x, y))
        if b is not None:
            print(f"Selected body at position: {b.position} with mass: {b.mass}")
        else:
            self.add_satellite_body((x, y))
    
    def remove_body(self):
        for b in self.bodies:
                    if b.selected:
                        if b is self.is_cenBody_alone:
                            self.is_cenBody_alone = None
                        self.bodies.remove(b)