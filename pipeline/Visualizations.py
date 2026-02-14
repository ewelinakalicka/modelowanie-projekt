import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class Visualizer:
    """
    Klasa, która tworzy wizualizacje:
    schematy pokojów, heatmapy rozchodzącego się ciepła
    """
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

    def plot(self, maps, titles=None, suptitle="Schemat pokojów",
             legend_pos=(1.0, 0.85)):
        '''
        Rysuje schemat pokoju z różnymi położeniami grzejnika
        :param maps:
        :param titles:
        :param suptitle:
        :param legend_pos:
        :return:
        '''
        n = len(maps)
        fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))

        if n == 1:
            axes = [axes]

        for i, ax in enumerate(axes):
            ax.imshow(maps[i], cmap=self.cmap, origin='lower')
            ax.set_xticks([])
            ax.set_yticks([])

            if titles:
                ax.set_title(titles[i])

        for name, col in self.legend_items:
            axes[-1].plot([], [], 's', color=col, label=name)

        axes[-1].legend(loc="upper right", bbox_to_anchor=legend_pos)

        fig.suptitle(suptitle, fontsize=14)
        plt.tight_layout()

        plt.show()


    def plot_three_room_heatmaps(self, sims, titles):
        """
        Rysuje heatmapy rozchodzenia się ciepła między trzema pokojami (3 scenariusze)
        """
        for sim, title in zip(sims, titles):
            fig, ax = plt.subplots(figsize=(12,4), constrained_layout=True)
            L, M, R = sim.get_2d_results_celsius()
            combined = np.hstack((L, M, R))

            im = ax.imshow(combined, origin='lower')

            ax.axvline(x=L.shape[1] - 0.5, color='white', linestyle='--')
            ax.axvline(x=L.shape[1] + M.shape[1] - 0.5, color='white', linestyle='--')

            ax.set_title(title)
            ax.axis('off')

            cbar = fig.colorbar(im, ax=ax, shrink=0.9)
            cbar.set_label("Temperatura [°C]")
            plt.show()

    def print_statistics(self, sim, title):
        '''
        Wyświetla statystyki dla każdego scenariusza
        '''
        L, M, R = sim.get_2d_results_celsius()
        rooms = [('Lewy', L, 'L'), ('Środkowy', M, 'M'), ('Prawy', R, 'R')]

        print("\n" + "=" * 70)
        print(f"STATYSTYKI: {title}")
        print(f"{'Pokój':<12} | {'Średnia':<8} | {'Max':<8} | {'Min':<8} | {'Std':<8} | {'Energia [kJ]':<12}")
        print("-" * 70)

        for name, data, key in rooms:
            avg_t = np.mean(data)
            max_t = np.max(data)
            min_t = np.min(data)
            std_t = np.std(data)
            energy_kj = sim.energy[key]

            print(f"{name:<12} | {avg_t:>7.2f}°C | {max_t:>7.2f}°C | "
                  f"{min_t:>7.2f}°C | {std_t:>7.2f} | {energy_kj:>10.2f}")
