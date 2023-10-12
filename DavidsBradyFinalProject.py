import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json

# Create the main application window
root = tk.Tk()
root.title("Simple Recipe Organizer")

# Lists to store user-defined categories and saved recipes
user_defined_categories = []
saved_recipes = []

# Function to save recipes and categories to a JSON file


def save_data():
    data = {"categories": user_defined_categories, "recipes": saved_recipes}
    with open("recipe_data.json", "w") as f:
        json.dump(data, f)

# Function to load recipes and categories from a JSON file


def load_data():
    try:
        with open("recipe_data.json", "r") as f:
            data = json.load(f)
            user_defined_categories.extend(data["categories"])
            saved_recipes.extend(data["recipes"])
    except FileNotFoundError:
        # The file doesn't exist on the first run
        pass

# Function to save a recipe


def save_recipe(name, categories, ingredients, instructions, notes):
    recipe = {
        "name": name,
        "categories": categories,
        "ingredients": ingredients,
        "instructions": instructions,
        "notes": notes,
    }
    saved_recipes.append(recipe)

# Load data at the start of the program


load_data()

# Function to open the "Add Recipe" window


def open_add_recipe_window():
    add_recipe_window = tk.Toplevel(root)
    add_recipe_window.title("Add Recipe")

    # Labels for input fields
    label_name = tk.Label(add_recipe_window, text="Recipe Name:")
    label_name.pack()
    entry_name = tk.Entry(add_recipe_window)
    entry_name.pack()

    # Create a combobox for selecting or creating recipe categories
    label_category = tk.Label(add_recipe_window, text="Categories:")
    label_category.pack()

    category_vars = []
    category_comboboxes = []

    # Frame to hold category input fields
    category_frame = tk.Frame(add_recipe_window)
    category_frame.pack()

    def add_category():
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(category_frame, textvariable=category_var, values=user_defined_categories)
        category_combobox.grid(row=len(category_comboboxes), column=0)
        category_comboboxes.append(category_combobox)
        category_vars.append(category_var)

    # Add a button to add a new category input field
    add_category_button = tk.Button(add_recipe_window, text="Add Category", command=add_category)
    add_category_button.pack()

    # Labels for ingredients, instructions, and notes
    label_ingredients = tk.Label(add_recipe_window, text="Ingredients:")
    label_ingredients.pack()
    entry_ingredients = tk.Entry(add_recipe_window)
    entry_ingredients.pack()

    label_instructions = tk.Label(add_recipe_window, text="Instructions:")
    label_instructions.pack()
    entry_instructions = tk.Entry(add_recipe_window)
    entry_instructions.pack()

    label_notes = tk.Label(add_recipe_window, text="Notes:")
    label_notes.pack()
    entry_notes = tk.Entry(add_recipe_window)
    entry_notes.pack()

    # Function to add the recipe
    def save_added_recipe():
        recipe_name = entry_name.get()
        recipe_categories = [category_var.get() for category_var in category_vars if category_var.get()]
        recipe_ingredients = entry_ingredients.get()
        recipe_instructions = entry_instructions.get()
        recipe_notes = entry_notes.get()

        # Validate the input
        if not recipe_name or not recipe_ingredients or not recipe_instructions:
            messagebox.showerror("Error", "Please fill in all required fields.")
        else:
            # Check if any of the selected categories are not in user_defined_categories
            for category in recipe_categories:
                if category and category not in user_defined_categories:
                    user_defined_categories.append(category)

            # Save the recipe
            save_recipe(recipe_name, recipe_categories, recipe_ingredients, recipe_instructions, recipe_notes)
            messagebox.showinfo("Success", "Recipe added successfully!")
            add_recipe_window.destroy()
            # Save data after adding a recipe
            save_data()

    # Button to save the recipe
    save_button = tk.Button(add_recipe_window, text="Save Recipe", command=save_added_recipe)
    save_button.pack()


# Function to open the "View Recipes" window


def open_view_recipes_window():
    view_recipes_window = tk.Toplevel(root)
    view_recipes_window.title("View Recipes")

    # Create a listbox to display the list of saved recipes
    recipe_listbox = tk.Listbox(view_recipes_window, selectmode=tk.SINGLE)
    recipe_listbox.pack()

    # Function to update the listbox with saved recipes
    def update_recipe_list():
        recipe_listbox.delete(0, tk.END)
        for recipe in saved_recipes:
            recipe_listbox.insert(tk.END, recipe["name"])

    # Button to refresh the recipe list
    refresh_button = tk.Button(view_recipes_window, text="Refresh List", command=update_recipe_list)
    refresh_button.pack()

    # Function to view the details of the selected recipe
    def view_recipe_details():
        selected_index = recipe_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_recipe = saved_recipes[index]

            # Create a new window to display recipe details
            recipe_details_window = tk.Toplevel(view_recipes_window)
            recipe_details_window.title(selected_recipe["name"])

            # Display recipe details
            categories = selected_recipe.get('categories', [])
            ingredients = selected_recipe.get('ingredients', '')
            instructions = selected_recipe.get('instructions', '')
            notes = selected_recipe.get('notes', '')

            details_text = (
                f"Categories: {', '.join(categories)}\n"
                f"Ingredients: {ingredients}\n"
                f"Instructions: {instructions}\n"
                f"Notes: {notes}"
            )
            recipe_label = tk.Label(recipe_details_window, text=details_text)
            recipe_label.pack()

    # Button to view recipe details
    view_details_button = tk.Button(view_recipes_window, text="View Details", command=view_recipe_details)
    view_details_button.pack()

    # Initial update of the recipe list
    update_recipe_list()

    # Button to delete the selected recipe
    def delete_recipe():
        selected_index = recipe_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del saved_recipes[index]
            update_recipe_list()
            save_data()

    delete_button = tk.Button(view_recipes_window, text="Delete Recipe", command=delete_recipe)
    delete_button.pack()

    # Button to edit the selected recipe
    def edit_recipe():
        selected_index = recipe_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_recipe = saved_recipes[index]

            open_edit_recipe_window(selected_recipe)

    edit_button = tk.Button(view_recipes_window, text="Edit Recipe", command=edit_recipe)
    edit_button.pack()

    # Initial update of the recipe list
    update_recipe_list()

    # Function to open the "Edit Recipe" window
    def open_edit_recipe_window(selected_recipe):
        def add_category():
            # Function to add a new category to the category list
            new_category = category_var.get()
            if new_category and new_category not in user_defined_categories:
                user_defined_categories.append(new_category)
                category_combobox['values'] = user_defined_categories
            category_var.set("")  # Clear the input field

        edit_recipe_window = tk.Toplevel(root)
        edit_recipe_window.title("Edit Recipe")

        # Labels for input fields
        label_name = tk.Label(edit_recipe_window, text="Recipe Name:")
        label_name.pack()
        entry_name = tk.Entry(edit_recipe_window)
        entry_name.insert(0, selected_recipe["name"])  # Pre-populate with the recipe name
        entry_name.pack()

        # Create a combobox for selecting or creating recipe categories
        label_category = tk.Label(edit_recipe_window, text="Categories:")
        label_category.pack()

        category_vars = []
        category_comboboxes = []

        # Frame to hold category input fields
        category_frame = tk.Frame(edit_recipe_window)
        category_frame.pack()

        for category in selected_recipe["categories"]:
            category_var = tk.StringVar()
            category_combobox = ttk.Combobox(category_frame, textvariable=category_var, values=user_defined_categories)
            category_combobox.set(category)  # Pre-populate with the recipe's categories
            category_combobox.grid(row=len(category_vars), column=0)
            category_vars.append(category_var)
            category_comboboxes.append(category_combobox)

        # Add a button to add a new category input field
        add_category_button = tk.Button(category_frame, text="Add Category", command=add_category)
        add_category_button.grid(row=0, column=1)

        label_ingredients = tk.Label(edit_recipe_window, text="Ingredients:")
        label_ingredients.pack()
        entry_ingredients = tk.Entry(edit_recipe_window)
        entry_ingredients.insert(0, selected_recipe["ingredients"])  # Pre-populate with ingredients
        entry_ingredients.pack()

        label_instructions = tk.Label(edit_recipe_window, text="Instructions:")
        label_instructions.pack()
        entry_instructions = tk.Entry(edit_recipe_window)
        entry_instructions.insert(0, selected_recipe["instructions"])  # Pre-populate with instructions
        entry_instructions.pack()

        label_notes = tk.Label(edit_recipe_window, text="Notes:")
        label_notes.pack()
        entry_notes = tk.Entry(edit_recipe_window)
        entry_notes.insert(0, selected_recipe["notes"])  # Pre-populate with notes
        entry_notes.pack()

        # Function to save the edited recipe
        def save_edited_recipe():
            edited_recipe = {
                "name": entry_name.get(),
                "categories": [category_var.get() for category_var in category_vars if
                               category_var.get() not in ["", "Create a New Category"]],
                "ingredients": entry_ingredients.get(),
                "instructions": entry_instructions.get(),
                "notes": entry_notes.get()
            }

            # Validate the input
            if not (edited_recipe["name"] and edited_recipe["ingredients"] and edited_recipe["instructions"]):
                messagebox.showerror("Error", "Please fill in all required fields.")
            else:
                # Check if any of the selected categories are not in user_defined_categories
                for category in edited_recipe["categories"]:
                    if category and category not in user_defined_categories:
                        user_defined_categories.append(category)

                # Update the recipe details and save data
                selected_recipe.update(edited_recipe)
                update_recipe_list()
                save_data()
                edit_recipe_window.destroy()

        # Button to save the edited recipe
        save_button = tk.Button(edit_recipe_window, text="Save Recipe", command=save_edited_recipe)
        save_button.pack()

    # Initial update of the recipe list
    update_recipe_list()


# Function to open the "Settings" window
def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    # Default window size configuration
    label_window_size = tk.Label(settings_window, text="Default Window Size:")
    label_window_size.pack()

    default_sizes = ["900x900 (900px)", "1200x1200 (1200px)", "1400x1400 (1400px)"]

    default_size_var = tk.StringVar()
    default_size_var.set("1200x1200 (1200px)")  # Set a default size

    default_size_combobox = ttk.Combobox(settings_window, textvariable=default_size_var, values=default_sizes)
    default_size_combobox.pack()

    # Function to apply the selected default window size
    def apply_default_size():
        selected_size = default_size_var.get()
        # Parse the selected size to get the dimensions
        dimensions = selected_size.split(" ")[0]
        width, height = map(int, dimensions.split("x"))
        # You can store or use the width and height as needed
        messagebox.showinfo("Default Window Size", f"Default Window Size set to {width}x{height}")

    default_size_button = tk.Button(settings_window, text="Apply Default Size", command=apply_default_size)
    default_size_button.pack()

    # Category configuration (Remove Category)
    label_categories = tk.Label(settings_window, text="Categories:")
    label_categories.pack()

    category_var = tk.StringVar()

    # Populate the categories from the user_defined_categories list
    category_combobox = ttk.Combobox(settings_window, textvariable=category_var, values=user_defined_categories)
    category_combobox.pack()

    # Function to remove the selected category
    def remove_category():
        selected_category = category_var.get()
        if selected_category:
            # Ask for confirmation before removing the category
            confirmation = messagebox.askyesno("Confirmation",
                                               f"Are you sure you want to remove the category '{selected_category}'?")
            if confirmation:
                # Remove the category from the list of user-defined categories
                user_defined_categories.remove(selected_category)

                # Remove the category from all recipes
                for recipe in saved_recipes:
                    if selected_category in recipe['categories']:
                        recipe['categories'].remove(selected_category)

                category_combobox.set("")  # Clear the selected category
                save_data()  # Save data after removing the category
                messagebox.showinfo("Category Removed", f"Category '{selected_category}' has been removed.")

    remove_category_button = tk.Button(settings_window, text="Remove Category", command=remove_category)
    remove_category_button.pack()


# Button to open the "Add Recipe" window
add_recipe_button = tk.Button(root, text="Add Recipe", command=open_add_recipe_window)
add_recipe_button.pack()

# Button to open the "View Recipes" window
view_recipes_button = tk.Button(root, text="View Recipes", command=open_view_recipes_window)
view_recipes_button.pack()

# Button to open the "Settings" window
settings_button = tk.Button(root, text="Settings", command=open_settings_window)
settings_button.pack()

# Button to exit the application
exit_button = tk.Button(root, text="Exit", command=lambda: [save_data(), root.quit()])
exit_button.pack()

# Start the main application loop
root.mainloop()
