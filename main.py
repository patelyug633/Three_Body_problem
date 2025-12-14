from visualization import vis_loop


vis_loop() 





# pygame.init()
# G = 6.67430e-11         # Real gravitational constant
# distance_scale = 1e6   # 1 pixel = 1,000,000 meters
# time_scale = 60*60*24  # 1 frame = 1 day
# F_dt = 1/60 # 1 frame = 1 second

# class body:
#     def __init__(self, mass, position, velocity, radius, color, others=None):
#         self.mass = mass
#         self.position = np.array(position, dtype='float64')
#         self.velocity = np.array(velocity, dtype='float64')
#         self.radius = radius
#         self.color = color
#         self.trail = []
#         self.new_trail_point = (self.position[0], self.position[1])
#         self.acceleration = np.array([0.0, 0.0], dtype='float64')
#         if others is not None:
#             ax, ay = self.getAcceleration(others)
#             self.acceleration = np.array([ax, ay], dtype='float64')
    
#     def getAcceleration(self, others):
#         fx, fy = 0,0
#         for other in others:
#             if other != self:
#                 fxi, fyi = self.force(other)
#                 fx += fxi
#                 fy += fyi
#         ax = fx / self.mass
#         ay = fy / self.mass
#         return ax, ay
    
#     def force(self,other):
#         dx = (other.position[0] - self.position[0]) * distance_scale
#         dy = (other.position[1] - self.position[1]) * distance_scale
#         distance = np.sqrt(dx**2 + dy**2)
#         if distance == 0:
#             return 0,0
#         force = G * other.mass * self.mass / distance**2
#         fx = force * dx / distance
#         fy = force * dy / distance
#         return fx, fy
#     def update_position(self, dt):
#         scaled_dt = dt * time_scale
#         self.position[0] += (self.velocity[0] * scaled_dt + 
#                              (0.5 * self.acceleration[0] * (scaled_dt**2))) / distance_scale
#         self.position[1] += (self.velocity[1] * scaled_dt + 
#                              (0.5 * self.acceleration[1] * (scaled_dt**2))) / distance_scale
#         self.new_trail_point = (self.position[0], self.position[1])
    
#     def update_velocity(self, new_acceleration, dt):
#         scaled_dt = dt * time_scale
#         self.velocity[0] += 0.5 * (self.acceleration[0] + new_acceleration[0]) * scaled_dt
#         self.velocity[1] += 0.5 * (self.acceleration[1] + new_acceleration[1]) * scaled_dt
#         self.acceleration = new_acceleration
#         self.trail.append(self.new_trail_point)
#         if len(self.trail) > 500:
#             self.trail.pop(0)
        
#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.radius)
#         self.draw_trail(screen)
    
#     def draw_trail(self, screen):
#         if len(self.trail) > 2:
#             pygame.draw.lines(screen, self.color, False, self.trail, 1)

# def update(dt, others):
#         for b in others:
#             b.update_position(dt)
#         new_accelerations = []
#         for b in others:
#             ax, ay = b.getAcceleration(others)
#             new_accelerations.append(np.array([ax, ay], dtype='float64'))
#         for b, new_acc in zip(others, new_accelerations):
#             b.update_velocity(new_acc, dt)

# def run_simulation(elapsed_time):
#     while elapsed_time >= F_dt:
#         update(F_dt, bodies)
#         elapsed_time -= F_dt
    
#     return elapsed_time

# def draw_bodies():
#     for b in bodies:
#         b.draw(screen)

# screen = pygame.display.set_mode((640, 480), )
# running = True
# clock = pygame.time.Clock()
# bodies = []
# elapsed_time = 0
# pause = True

# while running:
#     if not pause:
#         elapsed_time += clock.tick(60) / 1000  # seconds since last frame
#     else:
#         clock.tick(60)

#     screen.fill((0, 0, 0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = event.pos
#             bodies.append(body(10, (x,y), (550,550), 5, (255,0,0), bodies))
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_a:
#                 bodies.append(body(5e24, (320,240), (0,0), 25,(0,0,255), bodies))
#             if event.key == pygame.K_SPACE:
#                 pause = not pause
    
#     if pause:
#         draw_bodies()
#     else:
#         elapsed_time = run_simulation(elapsed_time)
#         draw_bodies()
#     pygame.display.flip()

# pygame.quit()