import scipy.sparse as sp

#operatory różnicowe:
def D1_forward_sparse(n):
    return sp.eye(n, k=1, format='csr') - sp.eye(n, format='csr')

def D1_backward_sparse(n):
    return -sp.eye(n, k=-1, format='csr') + sp.eye(n, format='csr')

def D2_sparse(n):
    return sp.eye(n, k=-1, format='csr') - 2*sp.eye(n, format='csr') + sp.eye(n, k=1, format='csr')

class BoundaryConditions:
    '''
    Klasa budująca operatory do obliczenia warunków brzegowych
    '''
    def __init__(self, grid, physics):
        self.grid = grid
        self.physics = physics

        self._build_operators()

    def _build_operators(self):
        g = self.grid
        Nx, Ny = g.Nx, g.Ny
        hx, hy = g.hx, g.hy

        id_x = sp.eye(Nx, format='csr')
        id_y = sp.eye(Ny, format='csr')
        self.id = sp.eye(Nx * Ny, format='csr')

        self.Bx_forward = -sp.kron(id_y, D1_forward_sparse(Nx)) / hx + self.id * self.physics.beta_wall
        self.Bx_backward = sp.kron(id_y, D1_backward_sparse(Nx)) / hx + self.id * self.physics.beta_wall
        self.By_forward = -sp.kron(D1_forward_sparse(Ny), id_x) / hy + self.id * self.physics.beta_wall
        self.By_backward = sp.kron(D1_backward_sparse(Ny), id_x) / hy + self.id * self.physics.beta_wall
        self.By_backward_window = sp.kron(D1_backward_sparse(Ny), id_x) / hy + self.id * self.physics.beta_window

        self.lap = sp.kron(id_y, D2_sparse(Nx)) / (hx ** 2) + sp.kron(D2_sparse(Ny), id_x) / (hy ** 2)

    def apply(self, A, room):
        '''
        Funkcja nakładająca warunki brzegowe na macierz A
        '''
        g = self.grid
        A = A.tolil()
        # Warunki brzegowe:
        # lewa ściana:
        A[g.ind_edge_left, :] = self.Bx_forward[g.ind_edge_left, :]
        # górna ściana:
        A[g.ind_edge_top, :] = self.By_backward[g.ind_edge_top, :]
        # prawa ściana:
        A[g.ind_edge_right, :] = self.Bx_backward[g.ind_edge_right, :]
        # dolna ściana:
        A[g.ind_edge_bottom, :] = self.By_forward[g.ind_edge_bottom, :]
        # okno:
        A[room.window.mask, :] = self.By_backward_window[room.window.mask, :]

        return A.tocsr()

    def apply_rhs(self, rhs, room, T_out, neighbour_temps=None):
        g = self.grid
        p = self.physics
        rhs = rhs.copy()

        def wall(mask, T, beta):
            rhs[mask] = beta * T

        for side in ['left', 'right', 'top', 'bottom']:
            if neighbour_temps and side in neighbour_temps:
                wall(getattr(g, f"ind_edge_{side}"), neighbour_temps[side], p.beta_wall)
            else:
                wall(getattr(g, f"ind_edge_{side}"), T_out, p.beta_wall)

        wall(room.window.mask, T_out, p.beta_window)

        return rhs
