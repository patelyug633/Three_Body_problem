import pygame
# from simulation import run_simulation
from physics import body
from config import configuration as config
from simulation import Simulation as sim


def draw_bodies(screen, bodies):
    for b in bodies:
        b.draw(screen)

def vis_loop():
    screen = pygame.display.set_mode((640, 480), )
    running = True
    clock = pygame.time.Clock()
    bodies = []
    simulation = sim()
    pause = True
    while running:
        if not pause:
            simulation.append_elapsed_time(clock.tick(60) / 1000)  # seconds since last frame
        else:
            clock.tick(60)

        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x_vel, y_vel = config().get_PerfectOrbit_velocity(5e24, (x,y))
                bodies.append(body(10, (x,y), (x_vel,y_vel), 5, (255,0,0), bodies))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    bodies.append(body(5e24, (320,240), (0,0), 25,(0,0,255), bodies))
                if event.key == pygame.K_SPACE:
                    pause = not pause

        if pause:
            draw_bodies(screen, bodies)
        else:
            simulation.run_simulation(bodies)
            draw_bodies(screen, bodies)

        pygame.display.flip()
    pygame.quit()
