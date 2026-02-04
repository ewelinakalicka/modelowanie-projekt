import matplotlib.pyplot as plt
from RoomMask import *
from RoomVisualization import *
from Parameters import *
from Boundary import *
from Solver import *

room = Room()
physics = PhysicsParameters()
bc = BoundaryConditions(room.grid, physics, room)

#schemat pokoju:
viz = RoomVisualizer()
radiators = [room.rad_side, room.rad_top, room.rad_bottom]
for i, radiator in enumerate(radiators):
    M = viz.draw_map(room.shape, room.window_mask, radiator, room.wall_mask)
    viz.plot(M)
    #plt.savefig(f"pokoj_{i}.png")
    plt.close()


#symulacja temperatury w pomieszczeniu:
positions = ['side', 'top', 'bottom']
solutions = {}
results = {}

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, position in enumerate(positions):
    print(f"\n=== Symulacja z grzejnikiem: {position} ===")
    solver = Solver(room.grid, room, physics, bc, radiator_position=position)

    solution = solver.solve()
    solutions[position] = solution
    results[position] = {
        'solver': solver,
        'mean_temp_c': np.mean(solver.solution_flat - 273.0),
        'std_temp_c': np.std(solver.solution_flat - 273.0)
    }

    ax = axes[idx]
    #wykres temperatury
    contour = ax.contourf(room.grid.x, room.grid.y, solution,
                          levels=50)

    #colorbar dla każdego subplotu
    plt.colorbar(contour, ax=ax, label='Temperatura [K]')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')

    print(f"Średnia temperatura: {results[position]['mean_temp_c']:.2f}°C")
    print(f"Odchylenie standardowe: {results[position]['std_temp_c']:.2f}°C")
    print(f"Powierzchnia grzejnika: {solver.A_radiator:.4f} m²")

#tytuł:
fig.suptitle('Porównanie rozkładu temperatury dla różnych położeń grzejnika',
             fontsize=14, fontweight='bold')

plt.tight_layout()
#plt.savefig("rozkład temperatury w pomieszczeniu.png")
plt.close()

#podsumowanie:
print("\n" + "=" * 60)
print("PODSUMOWANIE")
print("=" * 60)
for position in positions:
    res = results[position]
    print(f"\n{position.upper():10} | "
          f"Średnia: {res['mean_temp_c']:6.2f}°C | "
          f"Odchylenie: {res['std_temp_c']:5.2f}°C ")

