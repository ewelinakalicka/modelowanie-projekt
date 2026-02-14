# Modelowanie rozchodzenia się ciepła

Projekt ma na celu zasymulowanie rozkładu temperatur w pokoju z jednym grzejnikiem (różne położenia) oraz rozchodzenia się ciepła pomiędzy trzema pokojami, gdy mamy zagadnienie tzw. pasożytnictwa cieplnego. Kod pozwala wizuwalizować układ pomieszczeń, uruchamiać symulacje oraz wyświetlać podstawowe statystyki. 

## Struktura projektu 

modelowanie-project/
├─ notebooks/ 
│ ├─ problem1.ipynb
│ └─ problem2.ipynb
├─ pipeline/
│ ├─ Boundary.py
│ ├─ MultiRoomSim.py
│ ├─ Parameters.py
│ ├─ Radiator.py
│ ├─ RoomMask.py
│ ├─ Solver.py
│ └─ Visualizations.py
├─ plots/
│ ├─ rozklad_temperatury_problem1.png
│ ├─ podsumowanie.png
│ ├─ scenariusz1.png
│ ├─ scenariusz2.png
│ ├─ scenariusz3.png
│ └─ schemat_pokoj.png
├─ requirements.txt
└─ README.md

## Zawartość poszczególnych elementów repozytorium 

- `notebooks/` – notatniki `.ipynb` z eksperymentami, wizualizacjami i opisami 

- `pipeline/` – kody do symulacji, podzielone na klasy:
  - `Boundary` – definiuje i ustawia warunki brzegowe.
  - `MultiRoomSim` – zarządza symulacją trzech pokoi i trzech scenariuszy grzewczych.
  - `Parameters` – definiuje parametry fizyczne do symulacji.
  - `Radiator` – definiuje charakterystyki i maski grzejnika oraz klasę, do jego kontrolowania.
  - `RoomMask` – zarządza siatką, maską pokoju, w tym okna i grzejników.
  - `Solver` – rozwiązuje równanie ciepła.
  - `Visualizations` – zawiera funkcje do rysowania wykresów: schematów pokoju, heatmap.
  - `main1.py` - uruchamia symulacje dla problemu 1.
  - `main2.py` - uruchamia symulacje dla problemu 2. 

- `plots` - wykresy, schematy, heatmapy

- `requirements.txt` - wymagane paczki do odpalenia kodu
- `.gitignore` - pliki i foldery, które system ma ignorować w repozytorium 

