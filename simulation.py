from physics import body
from config import configuration as config

class SimulationError(Exception):
    pass
class Simulation:
    def __init__(self):
        self.elapsed_time = 0.0
        self.cfg = config()

    def run_simulation(self, bodies):
        cfg = self.cfg
        F_dt = cfg.F_dt
        while self.elapsed_time >= F_dt:
            cfg.update(bodies)
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