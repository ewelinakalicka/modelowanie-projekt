import numpy as np
import scipy.sparse.linalg as spla
import tqdm

class Solver:
    '''
    Klasa do rozwiązywania równania ciepła
    '''
    def __init__(self, grid, room, physics, bc, controller, t_end=3600*6):
        self.grid = grid
        self.room = room
        self.physics = physics
        self.bc = bc
        self.controller = controller

        self.t_end = t_end
        self.ht = 1
        self.t = np.arange(0, self.t_end, self.ht)

        self._build_matrix()

    def _build_matrix(self):
        alpha = self.physics.alpha
        lap = self.bc.lap

        self.A = self.bc.id - alpha * self.ht * lap
        self.A = self.bc.apply(self.A, self.room)

    def solve(self):
        g = self.grid
        p = self.physics

        u = np.ones(g.size) * p.T_initial
        for time in tqdm.tqdm(self.t):
            source = self.controller.source(u)

            rhs = u + self.ht * source
            rhs = self.bc.apply_rhs(rhs, self.room, self.physics.T_out)

            u = spla.spsolve(self.A, rhs)

        self.solution_2d = u.reshape(g.Ny, g.Nx)
        return self.solution_2d

    def step(self, u, neighbour_temps, T_out):
        source = self.controller.source(u)
        rhs = u + self.ht * source
        rhs = self.bc.apply_rhs(rhs, self.room, T_out, neighbour_temps)
        return spla.spsolve(self.A, rhs)