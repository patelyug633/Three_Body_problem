# simulation.py
from physics import body
from config import configuration as config
from graph import Graph

class SimulationError(Exception):
    pass
class Simulation:
    def __init__(self, viz):
        self.elapsed_time = 0.0
        self.cfg = config()
        self.centralBodies = [] # To track if central body is only one in the simulation
        self.bodies = self.cfg.bodies
        self.viz = viz
        self.selected_body = None
        self.graph_logs = {}
        self.logged_bodies = set()
        
    def getConfig(self):
        return self.cfg


    def run_simulation(self):
        cfg = self.cfg
        F_dt = cfg.F_dt
        while self.elapsed_time >= F_dt:
            cfg.update_VV(self.bodies)
            self.cfg.sim_time += F_dt
            self.log_graph_data()
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
        central_body = body(mass=mass, position=position, velocity=velocity, radius=radius, color=color, name= f"Body_{len(self.bodies)+1}")
        self.bodies.append(central_body)
        self.centralBodies.append(central_body)
        return central_body

    def add_satellite_body(self, onPos, mass = 10, radius = 5, color = (255,0,0), velocity = (0,0)):
        # if velocity is None and len(self.centralBodies) == 1:
        #     velocity  = self.cfg.get_PerfectOrbit_velocity(self.centralBodies[0].mass, onPos, self.centralBodies[0].position)
        if velocity is None:
            velocity = (0,0)
        satellite = body(mass=mass, position=onPos, velocity=velocity, radius=radius, color=color, name= f"Body_{len(self.bodies)+1}")
        self.bodies.append(satellite)
        return satellite

    def handle_click(self, position, mode):
        x, y = position
        b = body.select_body(self.bodies, (x, y)) if mode is None else None
        if b is not None:
            self.viz.UIBuilder.selected_body_panel(b)
            print(f"Selected body at position: {b.position} with mass: {b.mass}")
            self.selected_body = b
        else:
            if mode == "Add_satelite":
                self.add_satellite_body((x, y))
                mode = None
                self.viz.info_panel.elements["add_sat"].unselect()
            elif mode == "Add_Central":
                self.add_central_body(mass = 5e24, 
                    position =(x, y),
                    velocity = (0,0),
                    radius = 25,
                    color = (0,0,255))
                mode = None
                self.viz.info_panel.elements["add_cen"].unselect()
            else:
                self.unselectBodies()
                self.viz.UIBuilder.selected_body_panel_kill()
        return mode
    
    def remove_body(self):
        for b in self.bodies[:]:
            if b.selected:
                if b in self.centralBodies:
                    self.centralBodies.remove(b)
                self.bodies.remove(b)
    
    def remov_every_body(self):
        self.centralBodies.clear()
        self.bodies.clear()

    def selectBody(self, pos):
        b = body.select_body(self.bodies, pos)
        self.selected_body = b
        return b
    
    def getSelectedbody(self):
        return self.selected_body
    
    def unselectBodies(self):
        body.unselect_body(self.bodies)
        self.selected_body = None

    def getPOrbit(self):
        if len(self.centralBodies) == 1:
            velocity  = self.cfg.get_PerfectOrbit_velocity(self.centralBodies[0].mass, self.selected_body.position, self.centralBodies[0].position)
            return velocity
    
    def start_logging(self, body):
        if body not in self.graph_logs:
            self.graph_logs[body] = Graph(body.name)
        self.logged_bodies.add(body)
    
    def stop_logging(self, body):
        self.logged_bodies.discard(body)


    def log_graph_data(self):
        for body in self.logged_bodies:
            graph = self.graph_logs[body]

            vel = body.velocity
            acc = body.acceleration

            vel_mag = (vel[0]**2 + vel[1]**2) ** 0.5
            acc_mag = (acc[0]**2 + acc[1]**2) ** 0.5

            U = body.get_potential_energy(self.bodies)

            graph.record(
                (self.cfg.sim_time*self.cfg.time_scale),
                vel_mag,
                acc_mag,
                body.mass,
                vel,
                U
            )
