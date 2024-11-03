import tkinter as tk
import numpy as np
from tkinter import ttk
from algorithms import *
from tkinter import filedialog
import pandas as pd


# Main application window
root = tk.Tk()
root.title("GUI Skeleton")
root.geometry("900x600")  # Adjust the size as needed

# Variables
kierunek_options = ["Min", "Max"]
criterion_count = 0
data_sets = {} # {criterion_name : list of values}

# Function to add a new criterion
def add_criterion():
    global criterion_count
    criterion_count += 1
    name = f"Kryterium {criterion_count}"
    criteria_tree.insert("", "end", values=(criterion_count, name, kierunek_options[0]))
    renumber_criteria()

# Function to remove selected criterion and re-number "Lp" column
def remove_criterion():
    global data_sets
    selected_item = criteria_tree.selection()
    if selected_item:
        criteria_tree.delete(selected_item)
        renumber_criteria()
    if data_sets != {}:
        update_datasets()

# Function to renumber the Lp column to always be sequential
def renumber_criteria():
    for index, item in enumerate(criteria_tree.get_children(), start=1):
        current_values = criteria_tree.item(item, "values")
        criteria_tree.item(item, values=(index, f"Kryterium {index}", current_values[2]))

# Function to display dropdown over the selected row
def show_kierunek_dropdown(event):
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
    kierunek_dropdown.place_forget()

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
    nazwa_entry.select_range(0, tk.END)

# Function to save the edited "Nazwa" value
def save_nazwa(event):
    selected_item = criteria_tree.selection()
    if selected_item:
        row_id = selected_item[0]
        new_value = nazwa_var.get()
        criteria_tree.set(row_id, column="Nazwa", value=new_value)
    nazwa_entry.place_forget()

# Section 1: Criteria Editor
criteria_frame = ttk.LabelFrame(root, text="Edytor kryteriów")
criteria_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Treeview for criteria with "Lp", "Nazwa" and "Kierunek" columns
columns = ("Lp", "Nazwa", "Kierunek")
criteria_tree = ttk.Treeview(criteria_frame, columns=columns, show="headings")
criteria_tree.heading("Lp", text="Lp")
criteria_tree.heading("Nazwa", text="Nazwa")
criteria_tree.heading("Kierunek", text="Kierunek")
criteria_tree.column("Lp", width=40)
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



def generate_numbers():
    data = []
    type_of_distribution = str(distribution_option.get())
    mean = float(mean_entry.get())
    std = float(std_entry.get())
    number_obj = int(objects_entry.get())
    if type_of_distribution == "normal":
        data = np.random.normal(mean, std, number_obj)
    elif type_of_distribution == "uniform":
        low = mean - (std * np.sqrt(3))
        high = mean + (std * np.sqrt(3))
        data = np.random.uniform(low, high, number_obj)
    elif type_of_distribution == "poisson":
        lam = mean
        data = np.random.poisson(lam, number_obj)
    elif type_of_distribution == "exponential":
        scale = mean
        data = np.random.exponential(scale, number_obj)
    return data

def generate_datasets():
    global data_sets
    data_sets = {}
    for _, item in enumerate(criteria_tree.get_children(), start=1):
        current_values = criteria_tree.item(item, "values")
        data_sets[current_values[1]] = generate_numbers()
    setup_values_tree(data_sets)
    update_combobox()

def update_combobox():
    which_sorted['values'] = list(data_sets.keys())

def sort_datasets():
    global data_sets
    key_to_sort = str(which_sorted.get())
    data_sets[key_to_sort] = sorted(data_sets[key_to_sort])
    setup_values_tree(data_sets)

def update_datasets():
    global data_sets
    keys_to_keep = []
    for _, item in enumerate(criteria_tree.get_children(), start=1):
        current_values = criteria_tree.item(item, "values")
        keys_to_keep.append(current_values[1])
    data_sets = {key: value for key, value in data_sets.items() if key in keys_to_keep}
    setup_values_tree(data_sets)
    update_combobox()

# Section 2: Generation Settings
generation_frame = ttk.LabelFrame(root, text="Generacja")
generation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Options within Generation Frame
distribution_label = ttk.Label(generation_frame, text="Rozkład")
distribution_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
distribution_option = ttk.Combobox(generation_frame, values=["normal", "uniform", "poisson", "exponential"])
distribution_option.grid(row=0, column=1, padx=5, pady=5)

mean_label = ttk.Label(generation_frame, text="Średnia")
mean_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
mean_entry = ttk.Entry(generation_frame)
mean_entry.grid(row=1, column=1, padx=5, pady=5)

std_label = ttk.Label(generation_frame, text="Odchylenie")
std_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
std_entry = ttk.Entry(generation_frame)
std_entry.grid(row=2, column=1, padx=5, pady=5)

objects_label = ttk.Label(generation_frame, text="Liczba obiektów")
objects_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
objects_entry = ttk.Entry(generation_frame)
objects_entry.grid(row=3, column=1, padx=5, pady=5)

# Generate and Sort buttons
generate_button = ttk.Button(generation_frame, text="Generuj", command=generate_datasets)
generate_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

sort_button = ttk.Button(generation_frame, text="Sortuj", command=sort_datasets)
sort_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

which_sorted = ttk.Combobox(generation_frame, values=list(data_sets.keys()))
which_sorted.grid(row=4, column=2, padx=5, pady=5)


# Section 3: Values Editor
values_frame = ttk.LabelFrame(root, text="Edytor wartości")
values_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

# Dynamically adjust columns in values_tree based on keys in the dictionary
def setup_values_tree(datasets):
    # Clear any existing columns
    for column in values_tree["columns"]:
        values_tree.heading(column, text="")

    # Define columns with "lp" as the first column and keys of the dictionary as the rest
    columns = ["lp"] + list(datasets.keys())
    values_tree["columns"] = columns

    # Set up headings for each column
    for col in columns:
        values_tree.heading(col, text=col.capitalize())
        if col == "lp":
            values_tree.column(col, width=10, anchor="center")  # Set smaller width for "lp"
        else:
            values_tree.column(col, width=40)  # Wider width for other columns

    # Add data to the tree
    values_tree.delete(*values_tree.get_children())  # Clear any previous rows
    max_length = max(len(values) for values in datasets.values())  # Determine maximum row count
    for i in range(max_length):
        row = [i + 1]  # Start with lp value
        for key in datasets.keys():
            # Append value if it exists, otherwise append empty string
            row.append(f"{float(datasets[key][i]):.4f}" if i < len(datasets[key]) else "")
        values_tree.insert("", "end", values=row)

# Treeview for values with scrollbars
values_tree = ttk.Treeview(values_frame, show="headings")
values_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Add vertical scrollbar
vertical_scrollbar = ttk.Scrollbar(values_frame, orient="vertical", command=values_tree.yview)
values_tree.configure(yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar.grid(row=0, column=2, sticky="ns")

# Add horizontal scrollbar
horizontal_scrollbar = ttk.Scrollbar(values_frame, orient="horizontal", command=values_tree.xview)
values_tree.configure(xscrollcommand=horizontal_scrollbar.set)
horizontal_scrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")


def load_xls_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx")])
    if file_path:
        data = pd.read_excel(file_path)  # Load the data using pandas

        # Convert the data to dictionary format {column_name: values} for each column
        global data_sets
        data_sets = {col: data[col].tolist() for col in data.columns}

        # Update criteria list in criteria_tree if needed
        for criterion in data.columns:
            criterion_count = len(criteria_tree.get_children()) + 1
            criteria_tree.insert("", "end", values=(criterion_count, criterion, kierunek_options[0]))

        # Display data in values_tree
        setup_values_tree(data_sets)
        update_combobox()

# Nie wiem po co te przyciski tutaj
add_value_button = ttk.Button(values_frame, text="Dodaj", command=load_xls_file)
add_value_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")


def remove_selected_row():
    selected_items = values_tree.selection()  # Get all selected items
    if not selected_items:
        return

    # Gather row indices (lp) of selected items, convert to zero-based indices, and sort in descending order
    row_indices = sorted([int(values_tree.item(item)["values"][0]) - 1 for item in selected_items], reverse=True)

    # Remove each selected row from data_sets for each criterion in descending index order
    for row_index in row_indices:
        for key in data_sets.keys():
            if row_index < data_sets[key].shape[0]:
                data_sets[key] = np.delete(data_sets[key], row_index, axis=0)

    # Remove the selected rows from values_tree
    for item in selected_items:
        values_tree.delete(item)

    # Refresh the Treeview to reassign lp numbers correctly
    setup_values_tree(data_sets)

remove_value_button = ttk.Button(values_frame, text="Usuń", command=remove_selected_row)
remove_value_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")



def render_animation():
    pass

def stop_work():
    pass

def benchmark():
    pass

def solve():
    pass

# Section 4: Actions
actions_frame = ttk.LabelFrame(root, text="Akcje")
actions_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Algorithm selection and buttons
algorithm_label = ttk.Label(actions_frame, text="Algorytm:")
algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
algorithm_option = ttk.Combobox(actions_frame, values=["bez_filtracji", "z_filtracja", "punkt_idealny"])
algorithm_option.grid(row=0, column=1, padx=5, pady=5)

render_button = ttk.Button(actions_frame, text="Renderuj animację", command=render_animation)
render_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

stop_button = ttk.Button(actions_frame, text="Przerwij", command=stop_work)
stop_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

benchmark_button = ttk.Button(actions_frame, text="Benchmark", command=benchmark)
benchmark_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

solve_button = ttk.Button(actions_frame, text="Rozwiąż", command=solve)
solve_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

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
