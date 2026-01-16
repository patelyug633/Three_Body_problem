# graph.py
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, body_name):
        self.body_name = body_name
        self.time = []
        self.velocity = []
        self.acceleration = []
        self.energy = []

    def record(self, t, vel_mag, acc_mag, mass, velocity, U):
        self.time.append(t)
        self.velocity.append(vel_mag)
        self.acceleration.append(acc_mag)
        kinetic = 0.5 * mass * (velocity[0]**2 + velocity[1]**2)
        self.energy.append((kinetic, U, kinetic + U))

    def plot_velocity(self):
        if not self.time:
            print(f"No data for {self.body_name}")
            return
        plt.figure()
        plt.plot(self.time, self.velocity, color='green')
        plt.title(f"{self.body_name} - Velocity")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        plt.grid(True)
        plt.show()

    def plot_acceleration(self):
        if not self.time:
            print(f"No data for {self.body_name}")
            return
        plt.figure()
        plt.plot(self.time, self.acceleration, color='red')
        plt.title(f"{self.body_name} - Acceleration")
        plt.xlabel("Time (s)")
        plt.ylabel("Acceleration (m/s²)")
        plt.grid(True)
        plt.show()

    def plot_energy(self):
        if not self.time:
            print(f"No data for {self.body_name}")
            return
    
        # Unpack energy components
        kinetic = [e[0] for e in self.energy]
        potential = [e[1] for e in self.energy]
        total = [e[2] for e in self.energy]
    
        plt.figure(figsize=(10, 6))
        plt.plot(self.time, kinetic, label="Kinetic Energy", color="green")
        plt.plot(self.time, potential, label="Potential Energy", color="red")
        plt.plot(self.time, total, label="Total Energy", color="blue")
    
        plt.title(f"{self.body_name} - Energy")
        plt.xlabel("Time (s)")
        plt.ylabel("Energy (J)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    