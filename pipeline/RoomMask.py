import numpy as np

class Grid:
    def __init__(self, room_width = 3.0, room_length = 3.0, Nx = 20, Ny = 20):
        self.room_width = room_width
        self.room_length = room_length
        self.Nx = Nx
        self.Ny = Ny

        self.shape = (self.Nx, self.Ny)
        self.size = self.Nx * self.Ny

        self.x = np.linspace(0, room_width, Nx)
        self.y = np.linspace(0, room_length, Ny)
        self.hx = self.x[1] - self.x[0]
        self.hy = self.y[1] - self.y[0]

        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.X_flat = self.X.flatten()
        self.Y_flat = self.Y.flatten()

        #indeksy brzegów:
        self.ind_edge_left = self.X_flat == self.x[0]
        self.ind_edge_right = self.X_flat == self.x[-1]
        self.ind_edge_bottom = self.Y_flat == self.y[0]
        self.ind_edge_top = self.Y_flat == self.y[-1]


class Window:
    def __init__(self, grid, width):
        self.grid = grid
        self.width = width
        self.center = grid.room_width / 2
        self.x_min = self.center - width / 2
        self.x_max = self.center + width / 2

    def mask(self):
        return (self.grid.Y_flat == self.grid.room_length) & \
               (self.grid.X_flat >= self.x_min) & (self.grid.X_flat <= self.x_max)

class Radiator:
    def __init__(self, grid, width, offset = 2):
        self.grid = grid
        self.width = width
        self.offset = offset

    def top(self):
        offset_y = self.offset * self.grid.hy
        center_x = self.grid.room_width / 2
        xmin = center_x - self.width / 2
        xmax = center_x + self.width / 2

        return (self.grid.Y_flat <= self.grid.room_length - offset_y) & \
               (self.grid.Y_flat > self.grid.room_length - offset_y - 2 * self.grid.hy) & \
               (self.grid.X_flat >= xmin) & (self.grid.X_flat <= xmax)

    def bottom(self):
        offset_y = self.offset * self.grid.hy
        center_x = self.grid.room_width / 2
        xmin = center_x - self.width / 2
        xmax = center_x + self.width / 2

        return (self.grid.Y_flat >= offset_y) & \
            (self.grid.Y_flat < offset_y + 2 * self.grid.hy) & \
            (self.grid.X_flat >= xmin) & (self.grid.X_flat <= xmax)

    def side(self):
        offset_x = self.offset * self.grid.hx
        center_y = self.grid.room_length / 2
        ymin = center_y - self.width / 2
        ymax = center_y + self.width / 2

        return (self.grid.X_flat >= offset_x) & \
            (self.grid.X_flat < offset_x + 2 * self.grid.hx) & \
            (self.grid.Y_flat >= ymin) & (self.grid.Y_flat <= ymax)

class Walls:
    def __init__(self, grid):
        self.grid = grid

    def mask(self, window_mask=None):
        walls = (self.grid.X_flat == 0) | (self.grid.X_flat == self.grid.room_width) | \
                (self.grid.Y_flat == 0) | (self.grid.Y_flat == self.grid.room_length)
        if window_mask is not None:
            walls = walls & ~window_mask

        return walls

class Room:
    def __init__(self, room_width=3.0, room_length=3.0, Nx=20, Ny=20,
                 window_width=1.5, radiator_width=1.0, radiator_offset=2):
        self.grid = Grid(room_width, room_length, Nx, Ny)
        self.shape = self.grid.shape
        self.window = Window(self.grid, window_width)
        self.radiator = Radiator(self.grid, radiator_width, radiator_offset)
        self.walls = Walls(self.grid)

        # maski
        self.window_mask = self.window.mask()
        self.rad_top = self.radiator.top()
        self.rad_bottom = self.radiator.bottom()
        self.rad_side = self.radiator.side()
        self.wall_mask = self.walls.mask(self.window_mask)