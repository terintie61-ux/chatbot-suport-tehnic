import json
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_data')
PROCESSED_BIGDATA_PATH = os.path.join(PROCESSED_DATA_PATH, 'BigData')

#print(RAW_DATA_PATH)


# Necessary Categories:

# Air_Fryer_Recipes.json
# Apple_Pie.json
# Bagels.json
# Baked_Beans.json
# Banana_Breads.json
# Beef_Recipes.json
# Beef_Stews.json
# Beef_Stroganoff.json
# Beef_Tenderloin.json
# Biscuits.json
# Blintzes.json
# Blondies.json
# Blueberry_Pie.json
# Borscht.json
# Breads.json
# Breakfast_And_Brunch.json
# Breakfast_Burritos.json
# Broccoli_Salads.json
# Brownies.json
# Bruschetta.json
# Buffalo_Chicken_Dips.json
# Buffalo_Chicken_Wings.json
# Bulgogi.json
# Burgers.json
# Burritos.json
# Cabbage_Rolls.json
# Cakes.json
# Camping_Recipes.json
# Canning_And_Preserving.json
# Carrot_Cakes.json
# Cherry_Pie.json
# Chess_Pie.json
# Chicken_And_Dumplings.json
# Chicken_Cacciatore.json
# Chicken_Cordon_Bleu.json
# Chicken_Noodle_Soups.json
# Chicken_Parmesan.json
# Chicken_Salads.json
# Chilaquiles.json
# Chili_Recipes.json

# Chocolate_Cakes.json
# Chocolate_Chip_Cookies.json
# Chocolate_Fudge.json
# Chowders.json
# Christmas_Cookies.json
# Christmas.json
# Cinnamon_Rolls.json
# Cobblers.json
# Cocktails.json
# Coffee_Cakes.json
# Coleslaws.json
# Cookies.json

# Cooking_For_A_Crowd.json
# Cooking_For_One.json
# Cooking_For_Two.json

# Cupcakes.json
# Danishes.json
# Desserts.json

# Dinner.json
# Doughnuts.json
# Easter.json

# Egg_Rolls.json
# Egg_Salads.json
# Fajitas.json
# Falafel.json
# French_Onion_Soups.json
# Fried_Chicken.json
# Fried_Rice.json
# Fries.json
# Fruit_Salads.json

# Ground_Beef.json
# Ground_Chicken.json
# Ground_Lamb.json
# Ground_Pork.json
# Ground_Turkey.json

# Guacamole.json
# Gyros.json
# Healthy_Recipes.json
# Homemade_Pasta.json
# Ice_Cream.json

# # Chinese.json
# Indian.json
# Italian.json
# Korean.json
# Mexican.json
# Romenian.json

# Lamb.json
# Lasagna.json
# Lemon_Bars.json

# Lemonade.json

# Low_Calorie.json
# Low_Cholesterol.json
# Low_Fat.json
# Low_Glycemic_Impact.json
# Low_Sodium.json

# Lunch.json
# Macaroons.json

# Mojitos.json

# Mushrooms.json
# Nachos.json
# Oatmeal.json
# Omelets.json
# Pancakes.json
# Pasta_Carbonara.json
# Pickles.json
# Picnic_Recipes.json
# Pies.json
# Pizza.json
# Popcorn.json
# Pork_Chops.json
# Pork.json
# Vegetarian.json
# Waffles.json




#Category for Files
# 1.Cuisine(Romania,India,Mexican...)
# 2.Meal Time Served(Breakfast,Lunch,Dinner)
# 3.Desserts
# 4.Meat-based
# 5.Ground meat
# 6.Healthy/Dietary
# 7.Drinks
# 8.Main Dishes/Meals("Pizza.json","Burgers.json", "Burritos.json", "Fajitas.json", "Lasagna.json", "Pasta_Carbonara.json","Calzones")
# 9.Side Dish/Appetizers
# 10.Soups
# 11.Ocasional-based
# 12.Bakery
# 13 Others

"""
file_name = "Waffles.json"
category_name = "desserts"

main_category = {"Main_category": f"{category_name}"}

with open(os.path.join(RAW_DATA_PATH,f"{file_name}"),"r",encoding="utf-8") as file:
    data = json.load(file)



all_necessary_keys = ["recipe_title","category","ingredients","num_ingredients","directions","healthiness_score","health_level","tastes"]



cleaned_data = []

for recipe in data[:20]:
    filtered_recipe = {}

    for key in all_necessary_keys:
        if key in recipe:
            filtered_recipe[key] = recipe[key]

    cleaned_data.append(filtered_recipe)

#print(cleaned_data[0].keys())
#print(json.dumps(cleaned_data,indent=4))



cleaned_data.insert(0,main_category)




output_path = os.path.join(PROCESSED_BIGDATA_PATH,f"{category_name}\\{file_name}")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

"""


# Process Romanian file
#all_necessary_keys = ["recipe_title","category","ingredients","num_ingredients","directions","healthiness_score","health_level","tastes"]
#rom_keys = ["nume","category","ingrediente"]


"""
import json
import os

INPUT_FILE = "Romenian.json"
OUTPUT_FILE = "ConvertedRomanian.json"

def genereaza_directions(nume, ingrediente):
    # simplu (poți face mai smart ulterior)
    pasi = f"Pentru a prepara {nume}, urmează acești pași:\n"
    
    for i, ing in enumerate(ingrediente, 1):
        pasi += f"{i}. Pregătește {ing}. "
    
    pasi += "Amestecă ingredientele și gătește conform metodei tradiționale."
    
    return pasi


with open(os.path.join(RAW_DATA_PATH,INPUT_FILE), "r", encoding="utf-8") as f:
    data = json.load(f)

rezultat = []

data = data["retete"]

for item in data[:20]:  # maxim 20
    ingrediente = item.get("ingrediente", [])

    new_obj = {
        "recipe_title": item.get("nume"),
        "category": "romanian",
        "ingredients": ingrediente,
        "num_ingredients": len(ingrediente),
        "directions": genereaza_directions(item.get("nume"), ingrediente),
        "healthiness_score": item.get("scor_sanatate"),
        "health_level": item.get("nivel_sanatate"),
        "tastes": [item.get("gust_principal") ]
    }

    rezultat.append(new_obj)

# salvare
with open(os.path.join(PROCESSED_BIGDATA_PATH,"cuisine","Romanian.json"), "w", encoding="utf-8") as f:
    json.dump(rezultat, f, indent=4, ensure_ascii=False)

print("✅ Conversie completă!")
"""