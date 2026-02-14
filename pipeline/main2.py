from MultiRoomSim import *
from Visualizations import *

viz = Visualizer()

print("Symulacja 1/3: Wszyscy grzeją...")
sim_all = MultiRoomSimulation()
sim_all.set_scenario(True, True, True)
sim_all.run()

print("Symulacja 2/3: Środkowy nie grzeje...")
sim_par = MultiRoomSimulation()
sim_par.set_scenario(True, False, True)
sim_par.run()

print("Symulacja 3/3: Tylko środkowy grzeje...")
sim_mid = MultiRoomSimulation()
sim_mid.set_scenario(False, True, False)
sim_mid.run()

sims = [sim_all, sim_par, sim_mid]
titles = [
    "Wszyscy grzeją",
    "Środkowy nie grzeje",
    "Tylko środkowy grzeje"
]

# Heatmapy
viz.plot_three_room_heatmaps(sims, titles)

# Statystyki
for sim, title in zip(sims, titles):
    viz.print_statistics(sim, title)


# ==== PODSUMOWANIE PASOŻYTNICTWA CIEPLNEGO ====
fig, axes = plt.subplots(1, 2, figsize=(12,5))

#średnie temperatury
avg_temps = []
for sim in sims:
    L_mean = np.mean(sim.temp_history['L'])
    M_mean = np.mean(sim.temp_history['M'])
    R_mean = np.mean(sim.temp_history['R'])
    avg_temps.append([L_mean, M_mean, R_mean])

avg_temps = np.array(avg_temps)
width = 0.2
x = np.arange(len(titles))

axes[0].bar(x - width, avg_temps[:,0], width, label="lewy")
axes[0].bar(x, avg_temps[:,1], width, label="środkowy")
axes[0].bar(x + width, avg_temps[:,2], width, label="prawy")

axes[0].set_xticks(x)
axes[0].set_xticklabels(titles, rotation=20)
axes[0].set_ylabel("Średnia temperatura")
axes[0].set_title("Temperatury w pokojach")
axes[0].legend()

# zużycie energii w każdym ze scenariuszy
rooms = ['L', 'M', 'R']
labels = ['lewy', 'środkowy', 'prawy']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

x = np.arange(len(sims))  #pozycje scenariuszy
width = 0.25  #szerokość pojedynczego słupka

for i, room in enumerate(rooms):
    room_energies = [sim.energy[room] for sim in sims]

    offset = (i - 1) * width
    rects = axes[1].bar(x + offset, room_energies, width, label=labels[i], color=colors[i])

    #etykiety tekstowe nad słupkami
    for rect in rects:
        height = rect.get_height()
        axes[1].annotate(f'{int(height)}',
                         xy=(rect.get_x() + rect.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8)

axes[1].set_ylabel('Zużyta energia')
axes[1].set_title('Zużycie energii w podziale na pokoje')
axes[1].set_xticks(x)
axes[1].set_xticklabels(titles, rotation=20)
axes[1].legend()

fig.suptitle("Analiza pasożytnictwa cieplnego", fontsize=16)
plt.tight_layout()
plt.show()