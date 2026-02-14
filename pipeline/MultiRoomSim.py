from RoomMask import *
from Boundary import *
from Solver import *


class MultiRoomSimulation:
    '''
    Klasa do symulacji problemu pasożytnictwa dla trzech pokoi
    '''
    def __init__(self, t_end=3600*6):
        self.t_end = t_end
        self.ht = 1.0
        self.time_steps = np.arange(0, t_end, self.ht)

        self.physics = PhysicsParameters()

        self.room_L = Room(radiator_position = 'left')  #pokój po lewej
        self.room_M = Room()                            #pokój po środku
        self.room_R = Room(radiator_position = 'right') #pokój po prawej

        self.bc_L = BoundaryConditions(self.room_L.grid, self.physics)
        self.bc_M = BoundaryConditions(self.room_M.grid, self.physics)
        self.bc_R = BoundaryConditions(self.room_R.grid, self.physics)

        self.solver_L = Solver(self.room_L.grid, self.room_L, self.physics, self.bc_L, self.room_L.controller, t_end)
        self.solver_M = Solver(self.room_M.grid, self.room_M, self.physics, self.bc_M, self.room_M.controller, t_end)
        self.solver_R = Solver(self.room_R.grid, self.room_R, self.physics, self.bc_R, self.room_R.controller, t_end)

        # Warunki początkowe
        self.u_L = np.ones(self.room_L.grid.size) * self.physics.T_initial
        self.u_M = np.ones(self.room_M.grid.size) * self.physics.T_initial
        self.u_R = np.ones(self.room_R.grid.size) * self.physics.T_initial

        # Metryki: Zużycie energii (W * s = J) i historia średniej temperatury
        self.energy = {'L': 0.0, 'M': 0.0, 'R': 0.0}
        self.power = self.physics.P
        self.power_settings = {'L': self.physics.P, 'M': self.physics.P, 'R': self.physics.P}
        self.temp_history = {'L': [], 'M': [], 'R': []}

    def set_scenario(self, L_on, M_on, R_on):
        self.room_L.controller.enable_radiator(0, L_on)
        self.room_M.controller.enable_radiator(0, M_on)
        self.room_R.controller.enable_radiator(0, R_on)

    def run(self):
        for _ in tqdm.tqdm(self.time_steps, desc="Symulacja"):
            # temperatury sąsiednich pokoi
            bnd_L_right = self.u_L[self.room_L.grid.ind_edge_right]
            bnd_M_left = self.u_M[self.room_M.grid.ind_edge_left]
            bnd_M_right = self.u_M[self.room_M.grid.ind_edge_right]
            bnd_R_left = self.u_R[self.room_R.grid.ind_edge_left]

            self.u_L = self.solver_L.step(self.u_L, {'right': bnd_M_left}, self.physics.T_out)
            self.u_M = self.solver_M.step(self.u_M, {'left': bnd_L_right, 'right': bnd_R_left}, self.physics.T_out)
            self.u_R = self.solver_R.step(self.u_R, {'left': bnd_M_right}, self.physics.T_out)

            # historia temperatur
            self.temp_history['L'].append(np.mean(self.u_L) - 273.15)
            self.temp_history['M'].append(np.mean(self.u_M) - 273.15)
            self.temp_history['R'].append(np.mean(self.u_R) - 273.15)

            source_L = self.room_L.controller.source(self.u_L)
            source_M = self.room_M.controller.source(self.u_M)
            source_R = self.room_R.controller.source(self.u_R)

            hx, hy = self.room_L.grid.hx, self.room_L.grid.hy

            #zużycie energii:
            self.energy['L'] += np.sum(source_L) * hx * hy * self.ht
            self.energy['M'] += np.sum(source_M) * hx * hy * self.ht
            self.energy['R'] += np.sum(source_R) * hx * hy * self.ht


    def get_2d_results_celsius(self):
        Nx, Ny = self.room_L.grid.Nx, self.room_L.grid.Ny
        return (self.u_L.reshape((Ny, Nx)) - 273.0,
                self.u_M.reshape((Ny, Nx)) - 273.0,
                self.u_R.reshape((Ny, Nx)) - 273.0)
