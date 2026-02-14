import numpy as np
from Parameters import *

class Radiator:
    '''
    Klasa przechowująca podstawowe dane grzejnika: maskę, temperaturę ustawioną na termostacie i
    funkcję, która włącza/wyłącza termostat
    '''
    def __init__(self, mask, setpoint = 295.0):
        self.mask = mask
        self.setpoint = setpoint
        self.radiator_on = True

        p = PhysicsParameters()
        self.power = p.P

    def is_on(self, u):
        if not self.radiator_on:
            return False
        return np.mean(u) < self.setpoint

class RadiatorMask:
    '''
    Klasa tworząca maskę grzejnika
    '''
    def __init__(self, grid, width = 1.0, offset = 2, setpoint = 295.0, position = 'top'):
        self.grid = grid
        self.width = width
        self.offset = offset
        self.setpoint = setpoint
        self.position = position

        p = PhysicsParameters()
        self.power = p.P

        self.mask = self._build_mask()
        self.radiator = Radiator(self.mask, self.setpoint)

    def _build_mask(self):
        g = self.grid
        ox, oy = self.offset * g.hx, self.offset * g.hy

        if self.position in ['top', 'bottom']:
            cx = g.room_width / 2 #środek ściany
            xmin, xmax = cx - self.width / 2, cx + self.width / 2

            if self.position == 'top':
                ymin, ymax = g.room_length - oy - g.hy, g.room_length - oy
            else:
                ymin, ymax = oy, oy + g.hy

        elif self.position in ['left', 'right']:
            cy = g.room_length / 2
            ymin, ymax = cy - self.width / 2, cy + self.width / 2

            if self.position == 'right':
                xmin, xmax = g.room_width - ox - g.hx, g.room_width - ox
            else:
                xmin, xmax = ox, ox + g.hx
        return ((g.X_flat >= xmin) & (g.X_flat <= xmax) &
                (g.Y_flat >= ymin) & (g.Y_flat <= ymax))

class RadiatorController:
    '''
    Klasa kontrolująca grzejnik:
    funkcja, która wyłącza grzejnik,
    funkcja tworząca źródło ciepła
    '''
    def __init__(self, grid, physics):
        self.grid = grid
        self.physics = physics
        self.radiators = []

    def add_radiator(self, radiator):
        self.radiators.append(radiator)

    def enable_radiator(self, idx, state):
        self.radiators[idx].radiator.radiator_on = state

    def source(self, u):
        g = self.grid
        p = self.physics
        f = np.zeros_like(u)

        for radiator in self.radiators:
            mask = radiator.mask
            avg_temp = np.mean(u)
            A_radiator = np.sum(mask) * g.hx * g.hy #powierzchnia grzejnika
            T_local = np.mean(u[mask])
            rho = p.p / (p.r * min(T_local, 343.0))

            if radiator.radiator.is_on(avg_temp) and np.mean(u[mask]) < 343.0:
                S = radiator.power / (rho * A_radiator * p.c)
                f[mask] = S

        return f
