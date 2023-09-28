import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Simple Recipe Organizer")


# Function to open the "Add Recipe" window
def open_add_recipe_window():
    add_recipe_window = tk.Toplevel(root)
    add_recipe_window.title("Add Recipe")

    # Add widgets and functionality for adding a recipe here


# Function to open the "View Recipes" window
def open_view_recipes_window():
    view_recipes_window = tk.Toplevel(root)
    view_recipes_window.title("View Recipes")

    # Add widgets and functionality for viewing recipes here


# Function to open the "Search Recipes" window
def open_search_recipes_window():
    search_recipes_window = tk.Toplevel(root)
    search_recipes_window.title("Search Recipes")

    # Add widgets and functionality for searching recipes here


# Button to open the "Add Recipe" window
add_recipe_button = tk.Button(root, text="Add Recipe", command=open_add_recipe_window)
add_recipe_button.pack()

# Button to open the "View Recipes" window
view_recipes_button = tk.Button(root, text="View Recipes", command=open_view_recipes_window)
view_recipes_button.pack()

# Button to open the "Search Recipes" window
search_recipes_button = tk.Button(root, text="Search Recipes", command=open_search_recipes_window)
search_recipes_button.pack()

# Exit button to close the application
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack()

# Start the main application loop
root.mainloop()
