import numpy as np
import tqdm

class Solver:
    def __init__(self, grid, room, physics, bc, radiator_position = 'top'):
        self.grid = grid
        self.room = room
        self.physics = physics
        self.bc = bc

        self.ht = 1.0
        self.t = np.arange(0, 3600, self.ht)  # godzina symulacji

        self.radiator_position = radiator_position #położenie grzejnika: top/bottom/side

        self._build_system_matrix()
        self._build_source()

    def get_radiator_mask(self):
        if self.radiator_position == 'top':
            return self.room.rad_top
        elif self.radiator_position == 'side':
            return self.room.rad_side
        elif self.radiator_position == 'bottom':
            return self.room.rad_bottom

    def _build_system_matrix(self):
        alpha = self.physics.alpha
        lap = self.bc.laplacian()

        self.A = self.bc.id - alpha * self.ht * lap
        g = self.grid
        r = self.room

        # Warunki brzegowe:
        # lewa ściana:
        self.A[g.ind_edge_left, :] = self.bc.Bx_forward[g.ind_edge_left, :]
        # górna ściana:
        self.A[g.ind_edge_top, :] = self.bc.By_backward[g.ind_edge_top, :]
        # prawa ściana:
        self.A[g.ind_edge_right, :] = self.bc.Bx_backward[g.ind_edge_right, :]
        # dolna ściana:
        self.A[g.ind_edge_bottom, :] = self.bc.By_forward[g.ind_edge_bottom, :]
        # okno:
        self.A[r.window_mask, :] = self.bc.By_backward_window[r.window_mask, :]

    def _build_source(self):
        g = self.grid
        p = self.physics

        self.f = np.zeros(g.size)
        radiator_mask = self.get_radiator_mask()
        #powierzchnia grzejnika:
        self.A_radiator = np.sum(radiator_mask) * g.hx * g.hy

        #źródło ciepła na grzejniku:
        self.f[radiator_mask] = p.P * p.r / (p.p * self.A_radiator * p.c)

    def solve(self):
        g = self.grid
        p = self.physics
        r = self.room

        u0 = np.ones(g.size) * p.T_initial
        u_current = np.zeros(len(u0))
        radiator_mask = self.get_radiator_mask()
        boundary = (
            g.ind_edge_left | g.ind_edge_top | g.ind_edge_right | g.ind_edge_bottom
        ) & ~r.window_mask
        window = r.window_mask

        for time in tqdm.tqdm(self.t):
            if time == self.t[0]:
                u_current = u0.copy()
            else:
                f_eff = self.f * u_current * (np.mean(u_current) < p.T_target) * np.mean(u_current[radiator_mask] < 350)
                rhs = u_current + self.ht * f_eff
                rhs[boundary] = p.beta_wall * p.T_out
                rhs[window] = p.beta_window * p.T_out
                u_current = np.linalg.solve(self.A, rhs)

        self.solution_flat = u_current
        self.solution_2d = u_current.reshape(g.Nx, g.Ny)

        u_current = u_current - 273.0
        self.mean_temp = np.mean(u_current)
        self.std = np.std(u_current)

        return self.solution_2d

