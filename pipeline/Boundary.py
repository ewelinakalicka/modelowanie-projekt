import numpy as np

def D1_forward(n):
    return np.eye(n, k=1) - np.eye(n)

def D1_backward(n):
    return -np.eye(n, k=-1) + np.eye(n)

def D2(n):
    return np.eye(n, k=-1) - 2 * np.eye(n) + np.eye(n, k=1)

class BoundaryConditions:
    def __init__(self, grid, physics, room):
        self.grid = grid
        self.physics = physics
        self.room = room

        self._build_derivative_matrices()
        self._build_boundary_operators()

    def _build_derivative_matrices(self):
        Nx, Ny = self.grid.Nx, self.grid.Ny
        self.id_x = np.eye(Nx)
        self.id_y = np.eye(Ny)
        self.id = np.eye(Nx*Ny)

        self.D1_forward_x = D1_forward(Nx)
        self.D1_backward_x = D1_backward(Nx)
        self.D1_forward_y = D1_forward(Ny)
        self.D1_backward_y = D1_backward(Ny)

        self.D2_x = D2(Nx)
        self.D2_y = D2(Ny)

    def _build_boundary_operators(self):
        hx, hy = self.grid.hx, self.grid.hy

        self.Bx_forward = -np.kron(self.id_y, self.D1_forward_x) / hx + self.id * self.physics.beta_wall
        self.Bx_backward = np.kron(self.id_y, self.D1_backward_x) / hx + self.id * self.physics.beta_wall
        self.By_forward = -np.kron(self.D1_forward_y, self.id_x) / hy + self.id * self.physics.beta_wall
        self.By_backward = np.kron(self.D1_backward_y, self.id_x) / hy + self.id * self.physics.beta_wall
        self.By_backward_window = np.kron(self.D1_backward_y, self.id_x) / hy + self.id * self.physics.beta_window

    def laplacian(self):
        hx, hy = self.grid.hx, self.grid.hy

        return (np.kron(self.id_y, self.D2_x) / (hx ** 2) + np.kron(self.D2_y, self.id_x) / (hy ** 2))