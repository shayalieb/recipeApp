# Configure the connection to the MySQl database
import mysql.connector

# SQL user connection attributes
conn = mysql.connector.connect(
    host='localhost', 
    user='cf-python', 
    passwd='password')

# The variable that will enable the 2 way server/client communication
cursor = conn.cursor()

# Query - Once connected, create the database if none exists
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database1")

# Query - Use the database task_database
cursor.execute("USE task_database1")

# Query - create the table in the database if none exists
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20),
directions VARCHAR(2000)
)''')

# Main menu
def main_menu(conn, cursor):
    choice = ""
    while (choice != "quit"):
        print("\n======================================================")
        print("\nMain Menu:")
        print("-------------")
        print("Pick a choice:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Update an existing recipe")
        print("   4. Delete a recipe")
        print("   5. View all recipes")
        print("\n   Type 'quit' to exit the program")
        choice = input("\nYour choice: ")
        print("\n======================================================\n")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            view_all_recipes(conn, cursor)

# Create new recipe function
def create_recipe(conn, cursor):
    # Prompt the user for details about the recipe
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients, separated by commas: ").split(',')
    directions = input("Enter the directions for the recipe: ")  # Add this line

    # Calculate the difficulty of the recipe
    difficulty = calc_difficulty(cooking_time, ingredients)

    # Convert the list of ingredients into a string
    ingredients_str = ", ".join(ingredients)

    # Build the SQL query
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty, directions) VALUES (%s, %s, %s, %s, %s)"
    values = (name, ingredients_str, cooking_time, difficulty, directions)

    # Execute the query
    cursor.execute(query, values)

    # Commit the changes
    conn.commit()

    print("The recipe was added to the database.")

# Calculate the difficulty level
def calc_difficulty(cooking_time, recipe_ingredients):
    print("Run the calc_difficulty with: ", cooking_time, recipe_ingredients)

    if (cooking_time < 10) and (len(recipe_ingredients) < 4):
        difficulty_level = "Easy"
    elif (cooking_time < 10) and (len(recipe_ingredients) >= 4):
        difficulty_level = "Medium"
    elif (cooking_time >= 10) and (len(recipe_ingredients) < 4):
        difficulty_level = "Intermediate"
    elif (cooking_time >= 10) and (len(recipe_ingredients) >= 4):
        difficulty_level = "Hard"
    else:
        print("Something bad happened, please try again")

    print("Difficulty level: ", difficulty_level)
    return difficulty_level

# Search for a recipe by ingredient
def search_recipe(conn, cursor):
    all_ingredients = []
    # Query - Select all the ingredients from the database
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    for recipe_ingredients_list in results:
        for recipe_ingredients in recipe_ingredients_list:
            recipe_ingredient_split = recipe_ingredients.split(", ")
            all_ingredients.extend(recipe_ingredient_split)

    all_ingredients = list(dict.fromkeys(all_ingredients))

    all_ingredients_list = list(enumerate(all_ingredients))

    print("\nAll ingredients list:")
    print("------------------------")

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0]+1) + ". " + tup[1])

    try:
        ingredient_searched_nber = input(
            "\nEnter the number corresponding to the ingredient you want to select from the above list: ")

        ingredient_searched_index = int(ingredient_searched_nber) - 1

        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

        print("\nYou selected the ingredient: ", ingredient_searched)

    except:
        print("An unexpected error occurred. Make sure to select a number from the list.")

    else:
        print("\nThe recipe(s) below include(s) the selected ingredient: ")
        print("-------------------------------------------------------")

        # Query - Select the recipes that include the selected ingredient
        cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s",
                       ('%' + ingredient_searched + '%', ))

        results_recipes_with_ingredient = cursor.fetchall()
        for row in results_recipes_with_ingredient:
            print("\nID: ", row[0])
            print("Name: ", row[1])
            print("Ingredients: ", row[2])
            print("Cooking Time: ", row[3])
            print("Difficulty: ", row[4])
            print(f"Directions: {row[5]}\n")

# Update an existing recipe
def update_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id_for_update = int(
        (input("\nEnter the ID of the recipe you want to update: ")))
    column_for_update = str(input(
        "\nEnter the data you want to update among name, cooking time and ingredients: (select 'name' or 'cooking_time' or 'ingredients'): "))
    updated_value = (input("\nEnter the new value for the recipe: "))
    print("Choice: ", updated_value)

    if column_for_update == "name":
        # Query - Update the recipe name in the database
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s",
                       (updated_value, recipe_id_for_update))
        print("Modification done.")

    elif column_for_update == "cooking_time":
        # Query - Update the recipe cooking time in the database
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s",
                       (updated_value, recipe_id_for_update))
         # Query - Select the recipe to update from the database
        cursor.execute("SELECT * FROM Recipes WHERE id = %s",
                       (recipe_id_for_update, ))
        result_recipe_for_update = cursor.fetchall()

        name = result_recipe_for_update[0][1]
        recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
        cooking_time = result_recipe_for_update[0][3]

        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        print("Updated difficulty: ", updated_difficulty)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (updated_difficulty, recipe_id_for_update))
        print("Modification done.")

    elif column_for_update == "ingredients":
        # Query - Update the recipe ingredients in the database
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s",
                       (updated_value, recipe_id_for_update))
         # Query - Select the recipe to update from the database
        cursor.execute("SELECT * FROM Recipes WHERE id = %s",
                       (recipe_id_for_update, ))
        result_recipe_for_update = cursor.fetchall()

        print("result_recipe_for_update: ", result_recipe_for_update)

        name = result_recipe_for_update[0][1]
        recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
        cooking_time = result_recipe_for_update[0][3]
        difficulty = result_recipe_for_update[0][4]

        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        print("Updated difficulty: ", updated_difficulty)
        # Query - Update the recipe difficulty in the database
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (updated_difficulty, recipe_id_for_update))
        print("Modification done.")

    conn.commit()


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id_for_deletion = (
        input("\nEnter the ID of the recipe you want to delete: "))
    # Query - Delete the recipe from the database
    cursor.execute("DELETE FROM Recipes WHERE id = (%s)",
                   (recipe_id_for_deletion, ))

    conn.commit()
    print("\nRecipe successfully deleted from the database.")


def view_all_recipes(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    print("All Recipes:")
    for row in results:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print("Ingredients:")
        ingredients = row[2].split(', ')
        for i, ingredient in enumerate(ingredients, start=1):
            print(f"   {i}. {ingredient}")
        print(f"Cooking Time: {row[3]}")
        print(f"Difficulty: {row[4]}")
        print(f"Directions: {row[5]}\n")  # Add this line

main_menu(conn, cursor)
print("Goodbye\n")