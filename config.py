import pygame 
import sys
import numpy as np

G = 6.67430e-11         # Real gravitational constant
distance_scale = 1e6   # 1 pixel = 1,000,000 meters
time_scale = 60*60*24  # 1 frame = 1 day
F_dt = 1/60 # 1 frame = 1 second

