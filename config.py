import pygame 
import sys
import numpy as np

G = 6.67430e-11         # Real gravitational constant
distance_scale = 1e6   # 1 pixel = 1,000,000 meters
time_scale = 60*60*24  # 1 frame = 1 day
F_dt = 1/60 # 1 frame = 1 second

def get_PerfectOrbit_velocity(mass_central, current_pos, central_pos=(320,240)):
    x, y = current_pos
    central_x, central_y = central_pos
    Pvelocity = np.sqrt((G*mass_central)/(abs((central_x-x))*distance_scale))
    x_vel = Pvelocity * abs((x-central_x))/(np.sqrt((x-central_x)**2 + (y-central_y)**2))
    y_vel = Pvelocity * abs((y-central_y))/(np.sqrt((x-central_x)**2 + (y-central_y)**2))
    return y_vel, x_vel

def update(dt, others):
        for b in others:
            b.update_position(dt)
        new_accelerations = []
        for b in others:
            ax, ay = b.getAcceleration(others)
            new_accelerations.append(np.array([ax, ay], dtype='float64'))
        for b, new_acc in zip(others, new_accelerations):
            b.update_velocity(new_acc, dt)
