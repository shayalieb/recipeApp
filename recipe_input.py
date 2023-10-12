import pickle

def take_recipe():
    # Take recipe details from the user
    recipe_name = input("Enter the recipe name: ")
    cooking_time = input("Enter the cooking time: ")
    ingredients = input("Enter the ingredients (comma separated): ").split(',')

    # Calculate the difficulty of the recipe
    difficulty = calc_difficulty(ingredients, cooking_time)

    # Gather all these attributes into a dictionary
    recipe = {
        'name': recipe_name,
        'time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

    return recipe

#Define the difficulty levels
def calc_difficulty(ingredients, cooking_time):
    cooking_time = int(cooking_time)  # Ensure cooking_time is an integer
    num_ingredients = len(ingredients)

    if cooking_time < 10 and num_ingredients < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = 'Intermediate'
    else:
        difficulty = 'Hard'

    return difficulty

filename = input("Enter the filename: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

num_recipes = int(input("How many recipes would you like to enter? "))

for _ in range(num_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)
    print(f"Recipe '{recipe['name']}' has been added successfully.")

    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data['recipes_list'] = recipes_list
data['all_ingredients'] = all_ingredients

filename = 'recipe.txt'

with open(filename, 'wb') as file:
    # Use pickle.dump() to store the data
    pickle.dump(data, file)