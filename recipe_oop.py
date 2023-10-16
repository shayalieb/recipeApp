# Creating the class Recipe
class Recipe(object):
    all_ingredients = []

    # Define the method
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficultly = ""

    # Getter, and Setter methods
    # Getter - name
    def get_name(self):
        return self.name
    # Setter - name
    def set_name(self, name):
        self.name = name 
    
    # Getter - cooking_time
    def get_cooking_time(self):
        return self.cooking_time
    #Setter - cooking_time
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # Method: add_ingredients. 
    # This will take the number of arguments and them to the ingredients of the recipe
    def add_ingredients(self, *args):
        self.ingredients = args
        self.update_all_ingredients()

    # Getter - Ingredients
    def get_ingredients(self):
        print("\nIngredients: ")
        print("=============")
        for ingredients in self.ingredients:
            print(' - ' + str(ingredient))

    #Getter = Difficulty level
    def get_difficulty(self):
        difficulty =  self.calc_difficulty(self.cooking_time, self.ingredients)
        output = "Difficulty: " + str(self.cooking_time)
        self.difficultly = difficulty
        return output         
    
    # Method for calculating the recipe difficulty
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

    # Method for searching ingredients
    def search_ingredients(self, ingredient, ingredients):
        if ingredient in self.ingredients:
            return True
        else:
            return False

    # Method for updating ingredients list
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)

    # How the recipe will show in wll defined and easy to read string
    def __str__(self):
        output = "Name: " + self.name + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nIngredients: " + str(self.ingredients) + \
            "\nDifficulty: " + str(self.difficultly) + \
            "\n---------------------"
        for ingredient in self.ingredients:
            output += " - " + ingredient + "\n"
        return output    

    # Search for a specific ingredient in a recipe
    def recipe_search(self, recipe_list, ingredient):
        data = recipe_list
        search_term = ingredient
        for recipe in data:
            if self.search_ingredients(search_term, recipe.ingredients):  # Fix the method name here
                print(recipe)

# The recipe list 
recipe_list = []

#Recipes
tea = Recipe("Tea")
tea.add_ingredients("Hot Water", "Tea Bags", "Sugar")
tea.set_cooking_time(5)
tea.get_difficulty()
recipe_list.append(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Ground Coffee", "Hot Water", "Sugar", "Milk")
coffee.set_cooking_time(5)
coffee.get_difficulty()
recipe_list.append(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Flour", "Sugar", "Eggs", "Milk", "Butter", "Pure Vanilla")
cake.set_cooking_time(50)
cake.get_difficulty()
recipe_list.append(cake)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Banana", "Milk", "Sugar", "Ice")
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()
recipe_list.append(banana_smoothie)

# How it will be presented to the user
print("----------------------------------")
print("Recipe List")
print("----------------------------------")
for recipe in recipe_list:
    print(recipe)
print('----------------------------------')
print("Results for recipe_search 'Water': ")
print('----------------------------------')
tea.recipe_search(recipe_list, "Water")

print('----------------------------------')
print("Results for recipe_search 'Sugar': ")
print('----------------------------------')
tea.recipe_search(recipe_list, "Sugar")

print('----------------------------------')
print("Results for recipe_search 'Bananas': ")
print('----------------------------------')
tea.recipe_search(recipe_list, "Bananas")


