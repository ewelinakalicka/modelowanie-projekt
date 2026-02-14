from Radiator import *
from Parameters import *

#siatka:
class Grid:
    '''
    Klasa tworząca siatkę (dyskretyzacja przestrzeni) i przechowująca indeksy brzegowe
    '''
    def __init__(self, w=2.0, l=2.0, Nx=20, Ny=20):
        self.room_width = w
        self.room_length = l
        self.Nx, self.Ny = Nx, Ny

        self.x = np.linspace(0, w, Nx)
        self.y = np.linspace(0, l, Ny)

        self.hx = self.x[1] - self.x[0]
        self.hy = self.y[1] - self.y[0]

        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.X_flat = self.X.flatten()
        self.Y_flat = self.Y.flatten()

        self.size = Nx * Ny
        self.shape = (Ny, Nx)

        # indeksy brzegów:
        self.ind_edge_left = self.X_flat == self.x[0]
        self.ind_edge_right = self.X_flat == self.x[-1]
        self.ind_edge_bottom = self.Y_flat == self.y[0]
        self.ind_edge_top = self.Y_flat == self.y[-1]

class Window:
    '''
    Klasa tworząca maskę okna
    '''
    def __init__(self, grid, width = 1.5):
        center = grid.room_width / 2
        xmin = center - width / 2
        xmax = center + width / 2

        self.mask = (grid.X_flat >= xmin) & (grid.X_flat <= xmax) & \
                    (grid.Y_flat == grid.room_length)

class Room:
    '''
    Klasa przechowująca parametry pokoju: maski ścian, okna, grzejnika oraz siatkę
    '''
    def __init__(self, radiator_position = 'top'):
        self.grid = Grid()
        g = self.grid
        p = PhysicsParameters()
        self.window = Window(g)
        self.wall_mask = (g.ind_edge_left | g.ind_edge_right |
                           g.ind_edge_top | g.ind_edge_bottom) & ~self.window.mask

        self.controller = RadiatorController(g, p)
        self.radiator_mask = RadiatorMask(g, position = radiator_position)
        self.controller.add_radiator(self.radiator_mask)
