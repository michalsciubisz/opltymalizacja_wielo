import tkinter as tk
from tkinter import ttk

# Main application window
root = tk.Tk()
root.title("GUI Skeleton")
root.geometry("800x500")  # Adjust the size as needed

# Section 1: Criteria Editor
criteria_frame = ttk.LabelFrame(root, text="Edytor kryteriów")
criteria_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Treeview for criteria
criteria_tree = ttk.Treeview(criteria_frame, columns=("Nazwa", "Kierunek"), show="headings")
criteria_tree.heading("Nazwa", text="Nazwa")
criteria_tree.heading("Kierunek", text="Kierunek")
criteria_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Add and Remove buttons for Criteria Editor
add_criteria_button = ttk.Button(criteria_frame, text="Dodaj")
add_criteria_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

remove_criteria_button = ttk.Button(criteria_frame, text="Usuń")
remove_criteria_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Section 2: Generation Settings
generation_frame = ttk.LabelFrame(root, text="Generacja")
generation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Options within Generation Frame
distribution_label = ttk.Label(generation_frame, text="Rozkład")
distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
distribution_option = ttk.Combobox(generation_frame, values=["Ekspotencjalny", "Normalny", "Uniform"])
distribution_option.grid(row=0, column=1, padx=5, pady=5)

mean_label = ttk.Label(generation_frame, text="Średnia")
mean_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
mean_entry = ttk.Entry(generation_frame)
mean_entry.grid(row=1, column=1, padx=5, pady=5)

objects_label = ttk.Label(generation_frame, text="Liczba obiektów")
objects_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
objects_entry = ttk.Entry(generation_frame)
objects_entry.grid(row=2, column=1, padx=5, pady=5)

# Generate and Sort buttons
generate_button = ttk.Button(generation_frame, text="Generuj")
generate_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

sort_button = ttk.Button(generation_frame, text="Sortuj")
sort_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# Section 3: Values Editor
values_frame = ttk.LabelFrame(root, text="Edytor wartości")
values_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

# Treeview for values
values_tree = ttk.Treeview(values_frame, columns=("Kryterium 1", "Kryterium 2", "Kryterium 3",
                                                  "Kryterium 4", "Kryterium 5", "Kryterium 6",
                                                  "Kryterium 7", "Kryterium 8"), show="headings")
for i in range(1, 9):
    values_tree.heading(f"Kryterium {i}", text=f"Kryterium {i}")
values_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Add and Remove buttons for Values Editor
add_value_button = ttk.Button(values_frame, text="Dodaj")
add_value_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

remove_value_button = ttk.Button(values_frame, text="Usuń")
remove_value_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Section 4: Actions
actions_frame = ttk.LabelFrame(root, text="Akcje")
actions_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Algorithm selection and buttons
algorithm_label = ttk.Label(actions_frame, text="Algorytm:")
algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
algorithm_option = ttk.Combobox(actions_frame, values=["Naiwny", "Zaawansowany"])
algorithm_option.grid(row=0, column=1, padx=5, pady=5)

render_button = ttk.Button(actions_frame, text="Renderuj animację")
render_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

stop_button = ttk.Button(actions_frame, text="Przerwij")
stop_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

benchmark_button = ttk.Button(actions_frame, text="Benchmark")
benchmark_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

solve_button = ttk.Button(actions_frame, text="Rozwiąż")
solve_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Adjust grid weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(1, weight=3)

criteria_frame.grid_rowconfigure(0, weight=1)
criteria_frame.grid_columnconfigure(0, weight=1)
values_frame.grid_rowconfigure(0, weight=1)
values_frame.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
