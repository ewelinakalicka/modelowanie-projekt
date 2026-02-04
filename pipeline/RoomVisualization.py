import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class RoomVisualizer:
    def __init__(self):
        self.cmap = ListedColormap([
            "#d9d9d9",
            "#1f77b4",
            "#d62728",
            "#000000"
        ])

        self.legend_items = [
            ("Pokój", "#d9d9d9"),
            ("Ściany", "#000000"),
            ("Okno", "#1f77b4"),
            ("Grzejnik", "#d62728")
        ]

    def draw_map(self, room_shape, window, radiator, walls):
        M = np.zeros(room_shape, dtype=int)
        M[window.reshape(room_shape)] = 1
        M[radiator.reshape(room_shape)] = 2
        M[walls.reshape(room_shape)] = 3

        return M

    def plot(self, M, title="Schemat pokoju", legend_pos=(1.0, 0.85)):
        plt.figure(figsize=(6, 4))
        plt.imshow(M, cmap=self.cmap, origin="lower")

        # „zwykła” legenda
        for name, col in self.legend_items:
            plt.plot([], [], 's', color=col, label=name)

        plt.legend(loc="upper right", bbox_to_anchor=legend_pos)
        plt.xticks([])
        plt.yticks([])
        plt.title(title)
        plt.tight_layout()