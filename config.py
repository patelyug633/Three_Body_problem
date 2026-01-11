import numpy as np

class configuration:
    def __init__(self):
        self.G = 6.67430e-11         # Real gravitational constant
        self.distance_scale = 1e6   # 1 pixel = 1,000,000 meters
        self.time_scale = 60*60*24  # 1 frame = 1 day
        self.F_dt = 1/60 # 1 frame = 1 second
        self.bodies = []
    def get_PerfectOrbit_velocity(self, mass_central, current_pos, central_pos=(320,240)):
        x, y = current_pos
        central_x, central_y = central_pos
        Pvelocity = np.sqrt(((self.G)*(mass_central))/(np.sqrt((x-central_x)**2 + (y-central_y)**2)*self.distance_scale))
        x_vel = Pvelocity * abs((x-central_x))/(np.sqrt((x-central_x)**2 + (y-central_y)**2))
        y_vel = Pvelocity * abs((y-central_y))/(np.sqrt((x-central_x)**2 + (y-central_y)**2))
        if x < central_x and y < central_y:
            return y_vel, -x_vel
        elif x < central_x and y > central_y:
            return -y_vel, -x_vel
        elif x > central_x and y > central_y:
            return -y_vel, x_vel
        else:
            return y_vel, x_vel
        
    def update_VV(self, others):
        dt = self.F_dt * self.time_scale

        # 1. Update positions
        for b in others:
            b.position += (
                b.velocity * dt +
                0.5 * b.acceleration * dt * dt
            ) / self.distance_scale

            if not b.dragging:
                b.new_trail_point = tuple(b.position)

        # 2. Compute new accelerations
        new_accs = []
        for b in others:
            ax, ay = b.getAcceleration(others)
            new_accs.append(np.array([ax, ay], dtype='float64'))

        # 3. Update velocities
        for b, new_acc in zip(others, new_accs):
            b.velocity += 0.5 * (b.acceleration + new_acc) * dt
            b.acceleration = new_acc

            if not b.dragging:
                b.trail.append(b.new_trail_point)
            if len(b.trail) > 500:
                b.trail.pop(0)

                # b.update_velocity(new_acc, dt)