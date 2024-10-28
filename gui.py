import tkinter as tk
from tkinter import ttk

from algorithms import algorytm_bez_filtracji, algorytm_punkt_idealny, filtracja_zdominowanych

# Main application window
root = tk.Tk()
root.title("GUI Skeleton")
root.geometry("800x500")  # Adjust the size as needed

# Variables
kierunek_options = ["Min", "Max"]
criterion_count = 0

# Function to add a new criterion
def add_criterion():
    global criterion_count
    criterion_count += 1
    name = f"Kryterium {criterion_count}"
    # Insert with a placeholder Lp number, which will be updated in renumber_criteria
    criteria_tree.insert("", "end", values=(criterion_count, name, kierunek_options[0]))
    renumber_criteria()  # Refresh Lp column after adding

# Function to remove selected criterion and re-number "Lp" column
def remove_criterion():
    selected_item = criteria_tree.selection()
    if selected_item:
        criteria_tree.delete(selected_item)
        renumber_criteria()  # Refresh Lp column after removing

# Function to renumber the Lp column to always be sequential
def renumber_criteria():
    for index, item in enumerate(criteria_tree.get_children(), start=1):
        current_values = criteria_tree.item(item, "values")
        # Update Lp column (index), keep existing Nazwa and Kierunek
        criteria_tree.item(item, values=(index, current_values[1], current_values[2]))

# Function to display dropdown over the selected row
def show_kierunek_dropdown(event):
    # Get selected item
    selected_item = criteria_tree.selection()
    if not selected_item:
        return

    # Get the item's bounding box (for positioning the dropdown)
    row_id = selected_item[0]
    x, y, width, height = criteria_tree.bbox(row_id, column="Kierunek")

    # Get the current "Kierunek" value
    current_value = criteria_tree.item(row_id, "values")[2]
    kierunek_var.set(current_value)

    # Position the dropdown
    kierunek_dropdown.place(x=x + criteria_tree.winfo_x(), y=y + criteria_tree.winfo_y() + height)
    kierunek_dropdown.focus()

# Function to save the dropdown selection to the Treeview
def save_kierunek_selection(event):
    selected_item = criteria_tree.selection()
    if selected_item:
        row_id = selected_item[0]
        values = criteria_tree.item(row_id, "values")
        criteria_tree.set(row_id, column="Kierunek", value=kierunek_var.get())
    kierunek_dropdown.place_forget()  # Hide the dropdown after selection

# Function to enable editing of "Nazwa" column
def edit_nazwa(event):
    selected_item = criteria_tree.selection()
    if not selected_item:
        return

    # Get the item's bounding box for positioning the entry widget
    row_id = selected_item[0]
    x, y, width, height = criteria_tree.bbox(row_id, column="Nazwa")

    # Get the current "Nazwa" value
    current_value = criteria_tree.item(row_id, "values")[1]
    nazwa_var.set(current_value)

    # Position the entry widget over the selected cell
    nazwa_entry.place(x=x + criteria_tree.winfo_x(), y=y + criteria_tree.winfo_y() + height)
    nazwa_entry.focus()
    nazwa_entry.select_range(0, tk.END)  # Select text for easy editing

# Function to save the edited "Nazwa" value
def save_nazwa(event):
    selected_item = criteria_tree.selection()
    if selected_item:
        row_id = selected_item[0]
        new_value = nazwa_var.get()
        criteria_tree.set(row_id, column="Nazwa", value=new_value)
    nazwa_entry.place_forget()  # Hide the entry after editing

# Section 1: Criteria Editor
criteria_frame = ttk.LabelFrame(root, text="Edytor kryteriów")
criteria_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Treeview for criteria with "Lp" as the first column
columns = ("Lp", "Nazwa", "Kierunek")
criteria_tree = ttk.Treeview(criteria_frame, columns=columns, show="headings")
criteria_tree.heading("Lp", text="Lp")
criteria_tree.heading("Nazwa", text="Nazwa")
criteria_tree.heading("Kierunek", text="Kierunek")
criteria_tree.column("Lp", width=40)         # Set width for Lp column
criteria_tree.column("Nazwa", width=120)
criteria_tree.column("Kierunek", width=60)
criteria_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Bind double-click on "Kierunek" column to show the dropdown
criteria_tree.bind("<Double-1>", show_kierunek_dropdown)

# Bind double-click on "Nazwa" column to start editing
criteria_tree.bind("<Double-1>", lambda event: edit_nazwa(event) if criteria_tree.identify_column(event.x) == "#2" else show_kierunek_dropdown(event))

# Variable and dropdown for "Kierunek"
kierunek_var = tk.StringVar()
kierunek_dropdown = ttk.Combobox(root, textvariable=kierunek_var, values=kierunek_options, state="readonly")
kierunek_dropdown.bind("<<ComboboxSelected>>", save_kierunek_selection)  # Save selection on dropdown change

# Variable and entry for editing "Nazwa"
nazwa_var = tk.StringVar()
nazwa_entry = ttk.Entry(root, textvariable=nazwa_var)
nazwa_entry.bind("<Return>", save_nazwa)  # Save on Enter key press
nazwa_entry.bind("<FocusOut>", save_nazwa)  # Save on focus out

# Add and Remove buttons for Criteria Editor
add_criteria_button = ttk.Button(criteria_frame, text="Dodaj", command=add_criterion)
add_criteria_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

remove_criteria_button = ttk.Button(criteria_frame, text="Usuń", command=remove_criterion)
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
