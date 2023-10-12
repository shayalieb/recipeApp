import pickle

def display_recipe(recipe):
    print(f"Recipe Name: {recipe['name']}")
    print(f"Cooking Time: {recipe['time']}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data):
    print("Available ingredients:")
    for i, ingredient in enumerate(data['all_ingredients']):
        print(f"{i}. {ingredient}")

    try:
        ingredient_index = int(input("Pick a number from the list to search for recipes with that ingredient: "))
        ingredient_searched = data['all_ingredients'][ingredient_index]
    except:
        print("Incorrect input. Please enter a valid number.")
    else:
        print(f"Recipes with {ingredient_searched}:")
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

filename = input("Enter the filename: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found.")
else:
    search_ingredient(data)