# Import the necessary packages
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect to the database
DATABASE_URI = 'mysql+mysqlconnector://cf-python:password@localhost/task_database1'

# Create a session to connect to the database
engine = create_engine(DATABASE_URI)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class to be inherited by the other classes
Base = declarative_base()

# Create a class for the user table
class Recipe(Base): 
    __tablename__ = 'recipes_app' # Name of the table in the database
    # Define the columns for the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    directions = Column(String(1000))
    difficulty = Column(String(20))

    # Define the string representation of the recipe
    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', directions='{self.directions} difficulty='{self.difficulty}')>"
    
    def __str__(self):
        ingredients_list = "\n".join(f"\t\t{i}. {ingredient}" for i, ingredient in enumerate(self.ingredients.split(', '), 1))
        return (
            f"\tID: {self.id}\n"
            f"Recipe '{self.name}':\n"
            f"\tIngredients:\n{ingredients_list}\n"
            f"\tCooking Time: {self.cooking_time} minutes\n"
            f"\tDirections: {self.directions}\n"
            f"\tDifficulty: {self.difficulty}\n"  # Ensure this is on a new line
    )
    # Define the method for calculating the difficulty of the recipe 
    def calc_difficulty(self, cooking_time, ingredients):
        if (cooking_time < 10) and (len(ingredients) < 4):
            difficulty_level = "Easy"
        elif (cooking_time < 10) and (len(ingredients) >= 4):
            difficulty_level = "Medium"
        elif (cooking_time >= 10) and (len(ingredients) < 4):
            difficulty_level = "Intermediate"
        elif (cooking_time >= 10) and (len(ingredients) >= 4):
            difficulty_level = "Hard"
        else:
            print("Something happened, please try again")

        return difficulty_level
    
    # Define the method for returning the ingredients as a list
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(', ')

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Create a function to add a new recipe to the database
def create_recipe(session):
    # Collect the details of the recipe
    name = input("Enter the recipe name (max 50 characters): ")
    while len(name) > 50 or not all(c.isalnum() or c.isspace() for c in name):
        name = input("Invalid input. Enter the recipe name (max 50 characters, alphanumeric and spaces allowed): ")

    ingredients = input("Enter the ingredients, separated by commas: ")
    ingredients_list = ingredients.split(', ')
    print("Ingredients:")
    for i, ingredient in enumerate(ingredients_list, 1):
        print(f"{i}. {ingredient}")

    cooking_time = input("Enter the cooking time in minutes: ")
    while not cooking_time.isnumeric():
        cooking_time = input("Invalid input. Enter the cooking time in minutes (numeric): ")
    cooking_time = int(cooking_time)

    directions = input("Enter the cooking directions: ")

    # Create a new Recipe object without difficulty
    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time, directions=directions)

    # Calculate the difficulty
    difficulty = recipe_entry.calc_difficulty(cooking_time, ingredients_list)

    # Update the difficulty attribute of the Recipe object
    recipe_entry.difficulty = difficulty

    # Add the new recipe to the session and commit it to the database
    session.add(recipe_entry)
    session.commit()

    print(f"Recipe '{name}' has been added to the database.")

# Create a function to view all recipes in the database
def view_all_recipes(session):
    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    # If there are no recipes, inform the user and return to the main menu
    if not recipes:
        print("There are no recipes in the database.")
        return None

    # Loop through the recipes and display each one
    for recipe in recipes:
        print(recipe)  # This calls the __str__ method of the Recipe object    

def search_by_ingredients(session):
    # Check if the table has any entries
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Ask the user for an ingredient
    ingredient_to_search = input("Enter the ingredient you want to search for: ")

    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    # Initialize a list to store recipes that contain the ingredient
    matching_recipes = []

    # Loop through the recipes and check if the ingredient is in the ingredients list
    for recipe in recipes:
        if ingredient_to_search in recipe.ingredients.split(', '):
            matching_recipes.append(recipe)

    # If no recipes contain the ingredient, inform the user and return
    if not matching_recipes:
        print(f"No recipes found with the ingredient '{ingredient_to_search}'.")
        return None

    # Display the matching recipes
    print(f"Recipes containing '{ingredient_to_search}':")
    for recipe in matching_recipes:
        print(recipe)  # This calls the __str__ method of the Recipe object

# Create a function to edit a recipe
def edit_recipe(session):
    # Check if the table has any entries
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Retrieve the id and name for each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display the recipes to the user
    for id, name in results:
        print(f"{id}. {name}")

    # Ask the user to pick a recipe
    recipe_id = input("Enter the id of the recipe you want to edit: ")
    if not recipe_id.isnumeric() or not session.get(Recipe, int(recipe_id)):
        print("Invalid input.")
        return None

    # Retrieve the recipe
    recipe_to_edit = session.get(Recipe, int(recipe_id))

    # Display the recipe attributes
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time}")
    print(f"4. Directions: {recipe_to_edit.directions}")

    # Ask the user which attribute they want to edit
    attribute = input("Enter the number of the attribute you want to edit: ")
    if attribute == '1':
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute == '2':
        new_ingredients = input("Enter the new ingredients, separated by commas: ")
        recipe_to_edit.ingredients = new_ingredients
    elif attribute == '3':
        new_cooking_time = input("Enter the new cooking time: ")
        while not new_cooking_time.isnumeric():
            new_cooking_time = input("Invalid input. Enter the new cooking time (numeric): ")
        recipe_to_edit.cooking_time = int(new_cooking_time)
    elif attribute == '4':
        new_directions = input("Enter the new directions: ")
        recipe_to_edit.directions = new_directions
    else:
        print("Invalid input.")
        return None

    # Recalculate the difficulty
    ingredients_list = recipe_to_edit.ingredients.split(', ')
    recipe_to_edit.difficulty = recipe_to_edit.calc_difficulty(recipe_to_edit.cooking_time, ingredients_list)

    # Commit the changes to the database
    session.commit()

    print(f"Recipe '{recipe_to_edit.name}' has been updated.")

def delete_recipe(session):
    # Check if the table has any entries
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Retrieve the id and name for each recipe
    results = session.query(Recipe.id, Recipe.name).all()

    # Display the recipes to the user
    for id, name in results:
        print(f"{id}. {name}")

    # Ask the user to pick a recipe
    recipe_id = input("Enter the id of the recipe you want to delete: ")
    if not recipe_id.isnumeric() or not session.get(Recipe, int(recipe_id)):
        print("Invalid input.")
        return None

    # Retrieve the recipe
    recipe_to_delete = session.get(Recipe, int(recipe_id))

    # Delete the recipe
    session.delete(recipe_to_delete)
    session.commit()

    print(f"Recipe '{recipe_to_delete.name}' has been deleted.")

def main_menu(session):
    while True:
        print("\nRecipe App")
        print("*************")
        print("1. Add a new recipe")
        print("2. View all recipes")
        print("3. Search by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("---------------------------")
        print("Type 'quit' to exit the app")
        print("---------------------------")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            create_recipe(session)
        elif choice == '2':
            view_all_recipes(session)
        elif choice == '3':
            search_by_ingredients(session)
        elif choice == '4':
            edit_recipe(session)
        elif choice == '5':
            delete_recipe(session)
        elif choice == 'quit':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    # Create a new session
    session = Sessionlocal()

    # Call the main menu function
    main_menu(session)    