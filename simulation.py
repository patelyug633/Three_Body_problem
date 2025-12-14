from physics import body
from config import F_dt
from config import update

def run_simulation(elapsed_time, bodies):
    while elapsed_time >= F_dt:
        update(F_dt, bodies)
        elapsed_time -= F_dt
    
    return elapsed_time
