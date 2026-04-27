#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Model optimizat pentru acuratețe maximă
Autor: Maria
"""

import os
import json
import glob
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
from collections import Counter
import re
warnings.filterwarnings('ignore')

# Verificare CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🔥 Dispozitiv: {device}")
if torch.cuda.is_available():
    print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")

# ==================== CONFIGURARE ====================
CONFIG = {
    'batch_size': 256,           # Mărit pentru GPU
    'max_features': 15000,       # Mărit pentru mai multe cuvinte
    'epochs': 50,                # Mai multe epoci
    'learning_rate': 0.0012,
    'weight_decay': 0.000105,      # Regularizare
    'dropout_rate': 0.4,         # Dropout mai mare
    'hidden_sizes': [1024, 512, 256, 128],  # Rețea mai profundă
    'use_pretrained': True,      # Folosește embeddings pre-antrenate
    'embedding_dim': 300,        # Dimensiune embedding
}

# ==================== GRUPARE CATEGORII ====================

# Grupare manuală pentru a reduce numărul de clase
MAPARE_CATEGORII = {
    # Prăjituri
    'Angel Food Cake': 'Cakes',
    'Angel Food Cakes': 'Cakes',
    'Birthday Cake': 'Cakes',
    'Black Forest Cake': 'Cakes',
    'Blueberry Cake': 'Cakes',
    'Bundt Cake': 'Cakes',
    'Carrot Cake': 'Cakes',
    'Carrot Cakes': 'Cakes',
    'Chocolate Cake': 'Cakes',
    'Chocolate Cakes': 'Cakes',
    'Christmas Cake': 'Cakes',
    'Coconut Cake': 'Cakes',
    'Coffee Cake': 'Cakes',
    'Coffee Cakes': 'Cakes',
    'Lemon Cake': 'Cakes',
    'Pineapple Cake': 'Cakes',
    'Pound Cake': 'Cakes',
    'Pumpkin Cake': 'Cakes',
    'Red Velvet Cake': 'Cakes',
    'Spice Cake': 'Cakes',
    'Sponge Cake': 'Cakes',
    'Strawberry Cake': 'Cakes',
    'Upside-Down Cake': 'Cakes',
    'Wedding Cakes': 'Cakes',
    'White Cake': 'Cakes',
    'Yellow Cake': 'Cakes',
    'Zucchini Cake': 'Cakes',
    
    # Fursecuri și prăjituri mici
    'Bar Cookies': 'Cookies',
    'Blondies': 'Cookies',
    'Brownies': 'Cookies',
    'Butter Cookies': 'Cookies',
    'Cake Mix Cookies': 'Cookies',
    'Chocolate Chip Cookies': 'Cookies',
    'Chocolate Cookies': 'Cookies',
    'Christmas Cookies': 'Cookies',
    'Cookie Icing And Frosting': 'Cookies',
    'Cut-Out Cookies': 'Cookies',
    'Drop Cookies': 'Cookies',
    'Filled Cookies': 'Cookies',
    'Fruit Cookies': 'Cookies',
    'Gingerbread Cookies': 'Cookies',
    'Gingersnaps': 'Cookies',
    'Hanukkah Cookies': 'Cookies',
    'Holiday Cookies': 'Cookies',
    'International Cookies': 'Cookies',
    'Macaroons': 'Cookies',
    'Meringue Cookies': 'Cookies',
    'Molasses Cookies': 'Cookies',
    'No-Bake Cookies': 'Cookies',
    'Nut Cookies': 'Cookies',
    'Oatmeal Cookies': 'Cookies',
    'Oatmeal Raisin Cookies': 'Cookies',
    'Peanut Butter Cookies': 'Cookies',
    'Pizzelle Cookies': 'Cookies',
    'Pumpkin Cookies': 'Cookies',
    'Refrigerator Cookies': 'Cookies',
    'Shortbread Cookies': 'Cookies',
    'Snickerdoodles': 'Cookies',
    'Spice Cookies': 'Cookies',
    'Spritz Cookies': 'Cookies',
    'Sugar Cookies': 'Cookies',
    'Thumbprint Cookies': 'Cookies',
    'Whoopie Pies': 'Cookies',
    'Zucchini Cookies': 'Cookies',
    
    # Pâini
    'Banana Bread': 'Breads',
    'Banana Breads': 'Breads',
    'Biscuit': 'Breads',
    'Biscuits': 'Breads',
    'Bread Machine': 'Breads',
    'Breads': 'Breads',
    'Challah': 'Breads',
    'Christmas Bread': 'Breads',
    'Cornbread': 'Breads',
    'Cranberry Bread': 'Breads',
    'Easter Bread': 'Breads',
    'Egg Bread': 'Breads',
    'English Muffins': 'Breads',
    'Flat Bread': 'Breads',
    'Flatbreads': 'Breads',
    'French Toast': 'Breads',
    'Garlic Bread': 'Breads',
    'Gluten-Free Bread': 'Breads',
    'Healthy Bread': 'Breads',
    'Holiday Bread': 'Breads',
    'Indian Bread': 'Breads',
    'Irish Soda Bread': 'Breads',
    'Italian Bread': 'Breads',
    'Mexican Bread': 'Breads',
    'Monkey Bread': 'Breads',
    'No-Knead Bread Recipes': 'Breads',
    'Potato Bread': 'Breads',
    'Pumpkin Bread': 'Breads',
    'Quick Bread': 'Breads',
    'Roll And Bun Recipes': 'Breads',
    'Rye Bread': 'Breads',
    'Sourdough Bread': 'Breads',
    'White Bread': 'Breads',
    'Whole Grain Bread': 'Breads',
    'Whole Wheat Breads': 'Breads',
    'Yeast Bread': 'Breads',
    'Yeast Breads': 'Breads',
    'Zucchini Bread': 'Breads',
    'Zucchini Breads': 'Breads',
    
    # Mic dejun
    'Breakfast And Brunch': 'Breakfast',
    'Breakfast Bacon': 'Breakfast',
    'Breakfast Bowls': 'Breakfast',
    'Breakfast Bread': 'Breakfast',
    'Breakfast Burritos': 'Breakfast',
    'Breakfast Casseroles': 'Breakfast',
    'Breakfast Cereals': 'Breakfast',
    'Breakfast Cookies': 'Breakfast',
    'Breakfast Drinks': 'Breakfast',
    'Breakfast Eggs': 'Breakfast',
    'Breakfast Meat And Seafood': 'Breakfast',
    'Breakfast Pizza': 'Breakfast',
    'Breakfast Potatoes': 'Breakfast',
    'Breakfast Quiche': 'Breakfast',
    'Breakfast Sausage': 'Breakfast',
    'Breakfast Strata': 'Breakfast',
    'Breakfast Stratas': 'Breakfast',
    'Crepes And Blintzes': 'Breakfast',
    'French Toast Casserole': 'Breakfast',
    'Frittatas': 'Breakfast',
    'Grits': 'Breakfast',
    'Hash Brown Breakfast Casserole': 'Breakfast',
    'Hash Brown Potatoes': 'Breakfast',
    'Healthy Breakfast And Brunch': 'Breakfast',
    'Oatmeal': 'Breakfast',
    'Omelets': 'Breakfast',
    'Overnight Oats': 'Breakfast',
    'Paleo Breakfast And Brunch': 'Breakfast',
    'Pancakes': 'Breakfast',
    'Potato Breakfast Casserole': 'Breakfast',
    'Quiche': 'Breakfast',
    'Sausage Breakfast Casserole': 'Breakfast',
    'Southern Breakfast And Brunch': 'Breakfast',
    'Vegetarian Breakfast And Brunch': 'Breakfast',
    'Waffles': 'Breakfast',
    'Whole Grain Pancakes': 'Breakfast',
    
    # Supe
    'Beef Soup': 'Soups',
    'Butternut Squash Soups': 'Soups',
    'Chicken Noodle Soups': 'Soups',
    'Chicken Soup': 'Soups',
    'Chowders': 'Soups',
    'Clam Chowder': 'Soups',
    'Corn Chowder': 'Soups',
    'Cream Of Mushroom Soup': 'Soups',
    'French Onion Soups': 'Soups',
    'Lentil Soups': 'Soups',
    'Minestrone Soups': 'Soups',
    'Mushroom Soups': 'Soups',
    'Pork Soup': 'Soups',
    'Soup': 'Soups',
    'Vegetarian Soups And Stews': 'Soups',
    
    # Salate
    'Beef Salad': 'Salads',
    'Broccoli Salads': 'Salads',
    'Caesar Salad': 'Salads',
    'Coleslaws': 'Salads',
    'Dessert Salads': 'Salads',
    'Diabetic Salads': 'Salads',
    'Fruit Salads': 'Salads',
    'Green Salads': 'Salads',
    'Healthy Salads': 'Salads',
    'Italian Salads': 'Salads',
    'Jell-O Salads': 'Salads',
    'Kale Salad': 'Salads',
    'Low-Calorie Salads': 'Salads',
    'Low-Fat Salads': 'Salads',
    'Low-Sodium Salads': 'Salads',
    'Main Dish Salads': 'Salads',
    'Mexican Salads': 'Salads',
    'Pasta Salad': 'Salads',
    'Pasta Salads': 'Salads',
    'Potato Salad': 'Salads',
    'Spinach Salad': 'Salads',
    'Strawberry Salad': 'Salads',
    'Vegetarian Pasta Salad': 'Salads',
    'Waldorf Salads': 'Salads',
    
    # Carne
    'Bbq & Grilled Beef': 'Meat',
    'Bbq & Grilled Lamb': 'Meat',
    'Bbq & Grilled Pork': 'Meat',
    'Beef Appetizers': 'Meat',
    'Beef Brisket': 'Meat',
    'Beef Casserole': 'Meat',
    'Beef Chili': 'Meat',
    'Beef Chuck': 'Meat',
    'Beef Enchiladas': 'Meat',
    'Beef Leftovers': 'Meat',
    'Beef Main Dishes': 'Meat',
    'Beef Meatloaf': 'Meat',
    'Beef Pie': 'Meat',
    'Beef Pizza': 'Meat',
    'Beef Recipes': 'Meat',
    'Beef Ribs': 'Meat',
    'Beef Sandwiches': 'Meat',
    'Beef Sausage': 'Meat',
    'Beef Short Loin': 'Meat',
    'Beef Sirloin': 'Meat',
    'Beef Steaks': 'Meat',
    'Beef Stew': 'Meat',
    'Beef Stews': 'Meat',
    'Beef Stir-Fry': 'Meat',
    'Beef Stroganoff': 'Meat',
    'Beef Tenderloin': 'Meat',
    'Burritos': 'Meat',
    'Chicken Adobo': 'Meat',
    'Chicken And Dumplings': 'Meat',
    'Chicken Cacciatore': 'Meat',
    'Chicken Casserole': 'Meat',
    'Chicken Chili': 'Meat',
    'Chicken Cordon Bleu': 'Meat',
    'Chicken Enchiladas': 'Meat',
    'Chicken Fajitas': 'Meat',
    'Chicken Lasagna': 'Meat',
    'Chicken Leftovers': 'Meat',
    'Chicken Main Dishes': 'Meat',
    'Chicken Marsala': 'Meat',
    'Chicken Parmesan': 'Meat',
    'Chicken Piccata': 'Meat',
    'Chicken Pizza': 'Meat',
    'Chicken Salads': 'Meat',
    'Chicken Teriyaki': 'Meat',
    'Chicken Wings': 'Meat',
    'Chilaquiles': 'Meat',
    'Chili': 'Meat',
    'Chili Recipes': 'Meat',
    'Chinese Beef Main Dishes': 'Meat',
    'Chinese Chicken Main Dishes': 'Meat',
    'Chinese Main Dishes': 'Meat',
    'Chinese Pork Main Dishes': 'Meat',
    'Corned Beef': 'Meat',
    'Corned Beef And Cabbage': 'Meat',
    'Cooking Beef For Two': 'Meat',
    'Cooking Chicken For Two': 'Meat',
    'Cooking Pork For Two': 'Meat',
    'Curry Main Dishes': 'Meat',
    'Deep Fried Main Dishes': 'Meat',
    'Enchiladas': 'Meat',
    'Fajitas': 'Meat',
    'Filet Mignon': 'Meat',
    'Flank Steak': 'Meat',
    'Flat Iron Steak': 'Meat',
    'French Main Dishes': 'Meat',
    'Fried Chicken': 'Meat',
    'Goulash': 'Meat',
    'Greek Main Dishes': 'Meat',
    'Ground Beef': 'Meat',
    'Ground Beef Casserole': 'Meat',
    'Ground Chicken': 'Meat',
    'Ground Lamb': 'Meat',
    'Ground Pork': 'Meat',
    'Ground Turkey': 'Meat',
    'Gyros': 'Meat',
    'Hamburgers': 'Meat',
    'Healthy Main Dishes': 'Meat',
    'Indian Main Dishes': 'Meat',
    'Italian Main Dishes': 'Meat',
    'Italian Meatballs': 'Meat',
    'Korean Main Dishes': 'Meat',
    'Lamb': 'Meat',
    'Lamb Burgers': 'Meat',
    'Lamb Chops': 'Meat',
    'Lamb Shanks': 'Meat',
    'Lamb Stew': 'Meat',
    'Leg Of Lamb': 'Meat',
    'Low-Calorie Main Dishes': 'Meat',
    'Low-Cholesterol Main Dishes': 'Meat',
    'Low-Fat Main Dishes': 'Meat',
    'Low-Sodium Main Dishes': 'Meat',
    'Meat And Poultry Appetizers': 'Meat',
    'Meat Lasagna': 'Meat',
    'Meatball Appetizers': 'Meat',
    'Meatballs': 'Meat',
    'Meatloaf': 'Meat',
    'Mexican Main Dishes': 'Meat',
    'Paleo Main Dishes': 'Meat',
    'Pork': 'Meat',
    'Pork Casserole': 'Meat',
    'Pork Chili': 'Meat',
    'Pork Chops': 'Meat',
    'Pork Loin': 'Meat',
    'Pork Main Dishes': 'Meat',
    'Pork Meatloaf': 'Meat',
    'Pork Pie': 'Meat',
    'Pork Ribs': 'Meat',
    'Pork Sandwiches': 'Meat',
    'Pork Sausage': 'Meat',
    'Pork Shoulder': 'Meat',
    'Pork Stew': 'Meat',
    'Pork Stir-Fry': 'Meat',
    'Pork Tenderloin': 'Meat',
    'Prime Rib': 'Meat',
    'Quesadillas': 'Meat',
    'Ribs': 'Meat',
    'Roasts': 'Meat',
    'Sandwiches': 'Meat',
    'Shepherd\'S Pie': 'Meat',
    'Sloppy Joes': 'Meat',
    'Slow Cooker Main Dishes': 'Meat',
    'Southern Main Dishes': 'Meat',
    'Steaks And Chops': 'Meat',
    'Stir-Fries': 'Meat',
    'Stuffed Bell Peppers': 'Meat',
    'Stuffed Main Dishes': 'Meat',
    'Tacos': 'Meat',
    'Thai Main Dishes': 'Meat',
    'Turkey Burgers': 'Meat',
    'Turkey Casserole': 'Meat',
    'Turkey Chili': 'Meat',
    'Turkey Leftovers': 'Meat',
    'Turkey Main Dishes': 'Meat',
    'Turkey Meatloaf': 'Meat',
    'Veal Recipes': 'Meat',
    'Vegan Main Dishes': 'Meat',
    'Vegetarian Main Dishes': 'Meat',
    'Veggie Burgers': 'Meat',
    
    # Pește și fructe de mare
    'Seafood Appetizers': 'Seafood',
    'Seafood Casserole': 'Seafood',
    'Seafood Leftovers': 'Seafood',
    'Seafood Main Dishes': 'Seafood',
    'Seafood Pasta Salad': 'Seafood',
    'Shrimp Appetizers': 'Seafood',
    
    # Deserturi
    'Candy': 'Desserts',
    'Caramel Desserts': 'Desserts',
    'Cheesecake': 'Desserts',
    'Cheesecake Bars': 'Desserts',
    'Cheesecake Cupcakes': 'Desserts',
    'Cheesecakes': 'Desserts',
    'Chocolate Desserts': 'Desserts',
    'Christmas Desserts': 'Desserts',
    'Cobblers': 'Desserts',
    'Crisps And Crumbles': 'Desserts',
    'Cupcakes': 'Desserts',
    'Custards And Puddings': 'Desserts',
    'Dessert Filling Recipes': 'Desserts',
    'Dessert Glaze Recipes': 'Desserts',
    'Dessert Sauces': 'Desserts',
    'Dessert Tarts': 'Desserts',
    'Desserts': 'Desserts',
    'Diabetic Desserts': 'Desserts',
    'Frozen Desserts': 'Desserts',
    'Fruit Desserts': 'Desserts',
    'Fruit Pies': 'Desserts',
    'Gluten-Free Desserts': 'Desserts',
    'Healthy Desserts': 'Desserts',
    'Ice Cream': 'Desserts',
    'Ice Cream Pie': 'Desserts',
    'Indian Desserts': 'Desserts',
    'Italian Desserts': 'Desserts',
    'Low-Calorie Desserts': 'Desserts',
    'Low-Cholesterol Desserts': 'Desserts',
    'Low-Fat Desserts': 'Desserts',
    'Mexican Desserts': 'Desserts',
    'Mousse': 'Desserts',
    'Mousses': 'Desserts',
    'No-Bake Cheesecake': 'Desserts',
    'No-Bake Pies': 'Desserts',
    'Nut Desserts': 'Desserts',
    'Paleo Desserts': 'Desserts',
    'Pies': 'Desserts',
    'Pumpkin Cheesecakes': 'Desserts',
    'Pumpkin Pie': 'Desserts',
    'Specialty Desserts': 'Desserts',
    'Sweet Potato Pie': 'Desserts',
    'Thanksgiving Pies': 'Desserts',
    'Vegan Main Dishes': 'Desserts',
    'Vintage Pies': 'Desserts',
    
    # Băuturi
    'Beer Cocktails': 'Drinks',
    'Blended Cocktails': 'Drinks',
    'Bloody Marys': 'Drinks',
    'Bourbon Drinks': 'Drinks',
    'Champagne Drinks': 'Drinks',
    'Christmas Drink Recipes': 'Drinks',
    'Cocktails': 'Drinks',
    'Cosmopolitans': 'Drinks',
    'Daiquiris': 'Drinks',
    'Drink Flavoring & Simple Syrups': 'Drinks',
    'Drinks': 'Drinks',
    'Eggnog': 'Drinks',
    'Gin Drinks': 'Drinks',
    'Halloween Drinks': 'Drinks',
    'Hawaiian': 'Drinks',
    'Indian Drinks': 'Drinks',
    'Italian Drinks': 'Drinks',
    'Lemonade': 'Drinks',
    'Liqueurs': 'Drinks',
    'Margaritas': 'Drinks',
    'Martinis': 'Drinks',
    'Mexican Drinks': 'Drinks',
    'Mojitos': 'Drinks',
    'Mulled Wine': 'Drinks',
    'New Year\'S Drinks With Alcohol': 'Drinks',
    'New Year\'S Drinks Without Alcohol': 'Drinks',
    'Rum Drinks': 'Drinks',
    'Smoothies': 'Drinks',
    'Tequila Drinks': 'Drinks',
    'Vodka Drinks': 'Drinks',
    'Whiskey Drinks': 'Drinks',
    
    # Aperitive
    'Appetizers And Snacks': 'Appetizers',
    'Bacon Appetizers': 'Appetizers',
    'Bean And Pea Appetizers': 'Appetizers',
    'Beef Appetizers': 'Appetizers',
    'Canapes And Crostini': 'Appetizers',
    'Cheese Appetizers': 'Appetizers',
    'Diabetic Appetizers': 'Appetizers',
    'Fruit Appetizers': 'Appetizers',
    'Gluten-Free Appetizers': 'Appetizers',
    'Healthy Appetizers': 'Appetizers',
    'High-Fiber Appetizers': 'Appetizers',
    'Holiday Appetizers': 'Appetizers',
    'Italian Appetizers': 'Appetizers',
    'Jalapeno Poppers': 'Appetizers',
    'Kosher Appetizers': 'Appetizers',
    'Labor Day Appetizers': 'Appetizers',
    'Low-Calorie Appetizers': 'Appetizers',
    'Low-Cholesterol Appetizers': 'Appetizers',
    'Meat And Poultry Appetizers': 'Appetizers',
    'Meatball Appetizers': 'Appetizers',
    'Mexican Appetizers': 'Appetizers',
    'Mushroom Appetizers': 'Appetizers',
    'Nuts And Seeds Appetizers': 'Appetizers',
    'Olive Appetizers': 'Appetizers',
    'Pasta Appetizers': 'Appetizers',
    'Pastry Appetizers': 'Appetizers',
    'Seafood Appetizers': 'Appetizers',
    'Shrimp Appetizers': 'Appetizers',
    'Slow Cooker Appetizers': 'Appetizers',
    'Spicy Appetizers': 'Appetizers',
    'Thanksgiving Appetizers': 'Appetizers',
    'Vegetable Appetizers': 'Appetizers',
    'Vegetarian Appetizers': 'Appetizers',
    'Wraps And Rolls Appetizers': 'Appetizers',
    
    # Garnituri
    'Side Dishes': 'Sides',
    'Diabetic Side Dishes': 'Sides',
    'Gluten-Free Side Dishes': 'Sides',
    'Healthy Side Dishes': 'Sides',
    'High-Fiber Side Dishes': 'Sides',
    'Indian Side Dishes': 'Sides',
    'Italian Side Dishes': 'Sides',
    'Kosher Side Dishes': 'Sides',
    'Labor Day Side Dishes': 'Sides',
    'Low-Calorie Side Dishes': 'Sides',
    'Low-Cholesterol Side Dishes': 'Sides',
    'Low-Fat Side Dishes': 'Sides',
    'Low-Sodium Side Dishes': 'Sides',
    'Mexican Side Dishes': 'Sides',
    'New Year\'S Side Dishes': 'Sides',
    'Paleo Side Dishes': 'Sides',
    'Side Dish Casseroles': 'Sides',
    'Thanksgiving Side Dishes': 'Sides',
    'Vegetarian Side Dishes': 'Sides',
    
    # Diverse
    'Canning And Preserving': 'Preserving',
    'Jams And Jellies': 'Preserving',
    'Pickles': 'Preserving',
    'Pickled Vegetables': 'Preserving',
    'Relishes': 'Preserving',
    
    'Keto': 'Keto',
    'Keto Diet': 'Keto',
    'Paleo': 'Paleo',
    'Paleo Diet': 'Paleo',
    'Whole30': 'Whole30',
    'Whole30 Recipes': 'Whole30',
    
    'Gluten-Free': 'GlutenFree',
    'Gluten-Free Recipes': 'GlutenFree',
    
    'Vegetarian': 'Vegetarian',
    'Vegetarian Bbq & Grilling': 'Vegetarian',
    'Vegetarian Breakfast And Brunch': 'Vegetarian',
    'Vegetarian Casseroles': 'Vegetarian',
    'Vegetarian Chili': 'Vegetarian',
    'Vegetarian Enchiladas': 'Vegetarian',
    'Vegetarian Lasagna': 'Vegetarian',
    'Vegetarian Main Dish Casseroles': 'Vegetarian',
    'Vegetarian Main Dishes': 'Vegetarian',
    'Vegetarian Mushroom Main Dishes': 'Vegetarian',
    'Vegetarian Pie': 'Vegetarian',
    'Vegetarian Protein': 'Vegetarian',
    'Vegetarian Quiche': 'Vegetarian',
    'Vegetarian Side Dishes': 'Vegetarian',
    'Vegetarian Slow Cooker Recipes': 'Vegetarian',
    'Vegetarian Soups And Stews': 'Vegetarian',
    
    'Vegan': 'Vegan',
    'Vegan Main Dishes': 'Vegan',
    'Vegan Recipes': 'Vegan',
    
    'Christmas': 'Holiday',
    'Diwali': 'Holiday',
    'Easter': 'Holiday',
    'Halloween': 'Holiday',
    'Hanukkah': 'Holiday',
    'July 4Th': 'Holiday',
    'Kwanzaa': 'Holiday',
    'Labor Day': 'Holiday',
    'Lunar New Year': 'Holiday',
    'Mardi Gras': 'Holiday',
    'Passover': 'Holiday',
    'Purim Recipes': 'Holiday',
    'Rosh Hashanah Recipes': 'Holiday',
    'Seder Recipes': 'Holiday',
    'Thanksgiving': 'Holiday',
    
    'Casseroles': 'Casseroles',
    'Breakfast Casseroles': 'Casseroles',
    'Noodle Casserole': 'Casseroles',
    'Noodle Casseroles': 'Casseroles',
    'Rice Casserole': 'Casseroles',
    'Side Dish Casseroles': 'Casseroles',
    'Tater Tot Casserole': 'Casseroles',
    
    # Lasagna
    'Lasagna': 'Pasta',
    'Chicken Lasagna': 'Pasta',
    'Eggplant Lasagna': 'Pasta',
    'Meat Lasagna': 'Pasta',
    'Spinach Lasagna': 'Pasta',
    'Vegetarian Lasagna': 'Pasta',
    'Zucchini Lasagna': 'Pasta',
    
    # Paste
    'Fettuccini': 'Pasta',
    'Linguine': 'Pasta',
    'Macaroni And Cheese': 'Pasta',
    'Manicotti': 'Pasta',
    'Pasta Carbonara': 'Pasta',
    'Pasta Main Dishes': 'Pasta',
    'Pasta Primavera': 'Pasta',
    'Spaghetti': 'Pasta',
    'Ziti': 'Pasta',
    
    # Pizza
    'Pizza': 'Pizza',
    'Pizza Dough': 'Pizza',
    'Pizza Dough And Crusts': 'Pizza',
    'Pizza Sauce': 'Pizza',
    'Beef Pizza': 'Pizza',
    'Breakfast Pizza': 'Pizza',
    'Chicken Pizza': 'Pizza',
    'Pepperoni Pizza': 'Pizza',
    'Veggie Pizza': 'Pizza',
}

def grupeaza_categoria(categorie):
    """Grupează categoria într-una mai largă"""
    for pattern, group in MAPARE_CATEGORII.items():
        if pattern.lower() in categorie.lower() or categorie.lower() in pattern.lower():
            return group
    # Dacă nu găsește grupare, păstrează categoria originală
    return categorie

# ==================== MODEL ÎMBUNĂTĂȚIT ====================

class AttentionLayer(nn.Module):
    """Strat de atenție pentru focus pe cuvinte importante"""
    def __init__(self, hidden_size):
        super(AttentionLayer, self).__init__()
        self.attention = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        attention_weights = torch.softmax(self.attention(x), dim=1)
        weighted_output = x * attention_weights
        return weighted_output.sum(dim=1)

class EnhancedNeuralClassifier(nn.Module):
    """Model neuronal îmbunătățit cu atenție și residual connections"""
    def __init__(self, input_size, num_classes, hidden_sizes=[1024, 512, 256, 128]):
        super(EnhancedNeuralClassifier, self).__init__()
        
        self.layers = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        self.residual_connections = []
        
        prev_size = input_size
        
        for i, hidden_size in enumerate(hidden_sizes):
            self.layers.append(nn.Linear(prev_size, hidden_size))
            self.batch_norms.append(nn.BatchNorm1d(hidden_size))
            self.dropouts.append(nn.Dropout(0.3))
            
            # Residual connection dacă dimensiunile se potrivesc
            self.residual_connections.append(prev_size == hidden_size)
            prev_size = hidden_size
        
        # Strat de atenție
        self.attention = AttentionLayer(hidden_sizes[-1])
        
        # Strat final
        self.final_layer = nn.Linear(hidden_sizes[-1], num_classes)
        
        # Funcții de activare
        self.relu = nn.ReLU()
        self.softmax = nn.LogSoftmax(dim=1)
    
    def forward(self, x):
        for i, (layer, bn, dropout, use_residual) in enumerate(zip(
            self.layers, self.batch_norms, self.dropouts, self.residual_connections
        )):
            identity = x
            
            x = layer(x)
            x = bn(x)
            x = self.relu(x)
            
            # Residual connection
            if use_residual and i > 0:
                # Asigură dimensiuni compatibile
                if identity.shape[1] != x.shape[1]:
                    identity = identity[:, :x.shape[1]]
                x = x + identity
            
            x = dropout(x)
        
        # Atenție
        # x = self.attention(x.unsqueeze(1))
        
        x = self.final_layer(x)
        return self.softmax(x)

# ==================== SCRIPT PRINCIPAL ====================

print("=" * 70)
print("🚀 MODEL OPTIMIZAT PENTRU ACURATEȚE MAXIMĂ")
print("=" * 70)

# 1. Încărcare date
print("\n[1] 📁 Incarc si grupez datele...")

cale_json = 'data/raw_data/*.json'
if not os.path.exists('data/raw_data'):
    cale_json = '../../data/raw_data/*.json'

fisiere_json = glob.glob(cale_json)
toate_retetele = []

for fisier in fisiere_json:
    try:
        with open(fisier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                toate_retetele.extend(data)
            else:
                toate_retetele.append(data)
    except Exception as e:
        pass

print(f"Am incarcat {len(toate_retetele)} retete")

# 2. Extragere și grupare cuvinte
print("\n[2] 🔍 Extrag și grupez cuvintele...")

texte = []
intentii = []

for reteta in toate_retetele:
    text = reteta.get('combined_text', '')
    if not text:
        titlu = reteta.get('recipe_title', '')
        descriere = reteta.get('description', '')
        ingrediente = ' '.join(reteta.get('ingredients', []))
        instructiuni = ' '.join(reteta.get('directions', []))
        text = f"{titlu} {descriere} {ingrediente} {instructiuni}"
    
    # Grupare categorie
    categorie_originala = reteta.get('category', 'general')
    categorie_grupata = grupeaza_categoria(categorie_originala)
    
    if text and categorie_grupata and len(text) > 100:
        texte.append(text[:5000])
        intentii.append(categorie_grupata)

print(f"Am extras {len(texte)} exemple valide")

# Verifică distribuția după grupare
clase_counts = Counter(intentii)
print(f"\nClase după grupare: {len(clase_counts)}")
for cls, count in sorted(clase_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f"  {cls}: {count} exemple")

# 3. Filtrare clase cu prea puține exemple
min_exemple = 5
clase_valide = [c for c, count in clase_counts.items() if count >= min_exemple]
print(f"\nClase valide (min {min_exemple} exemple): {len(clase_valide)}")

date_filtrate = [(text, intent) for text, intent in zip(texte, intentii) if intent in clase_valide]
texte_filtrate = [d[0] for d in date_filtrate]
intentii_filtrate = [d[1] for d in date_filtrate]

print(f"Exemple după filtrare: {len(texte_filtrate)}")

# 4. Codificare
print("\n[3] 🏷️ Codific etichetele...")

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(intentii_filtrate)
num_classes = len(label_encoder.classes_)
print(f"Număr clase finale: {num_classes}")

# 5. Vectorizare (TF-IDF cu n-grame extinse)
print("\n[4] 📝 Vectorizez textul...")

vectorizer = TfidfVectorizer(
    max_features=CONFIG['max_features'],
    ngram_range=(1, 3),           # Bigrame și trigrame
    stop_words='english',
    min_df=3,                      # Ignoră cuvinte rare
    max_df=0.95,                   # Ignoră cuvinte prea comune
    sublinear_tf=True,             # Normalizare
    use_idf=True
)

X = vectorizer.fit_transform(texte_filtrate).toarray()
print(f"Dimensiune vectori: {X.shape}")

# 6. Împărțire
print("\n[5] ✂️ Impart datele...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Antrenare: {len(X_train)} exemple")
print(f"Test: {len(X_test)} exemple")

# 7. Standardizare (important pentru rețele neuronale)
print("\n[6] 📊 Standardizez datele...")

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 8. DataLoader
print("\n[7] 🔄 Pregatesc DataLoader-ul...")

class ReteteDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

train_dataset = ReteteDataset(X_train, y_train)
test_dataset = ReteteDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=CONFIG['batch_size'], shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=CONFIG['batch_size'], shuffle=False)

# 9. Model
print("\n[8] 🧠 Construiesc modelul îmbunătățit...")

model = EnhancedNeuralClassifier(
    input_size=CONFIG['max_features'],
    num_classes=num_classes,
    hidden_sizes=CONFIG['hidden_sizes']
).to(device)

print(f"Parametri model: {sum(p.numel() for p in model.parameters()):,}")

# 10. Optimizator și scheduler
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(
    model.parameters(), 
    lr=CONFIG['learning_rate'],
    weight_decay=CONFIG['weight_decay']
)
scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=5, T_mult=2)

# 11. Antrenare
print("\n[9] 🏋️ Antrenez modelul...")

best_accuracy = 0
best_model_state = None

for epoch in range(CONFIG['epochs']):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for data, target in train_loader:
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        
        # Gradient clipping pentru stabilitate
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(target).sum().item()
        total += target.size(0)
    
    train_acc = 100. * correct / total
    
    # Evaluare
    model.eval()
    test_correct = 0
    test_total = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)
            test_correct += pred.eq(target).sum().item()
            test_total += target.size(0)
    
    test_acc = 100. * test_correct / test_total
    
    scheduler.step()
    
    # Salvează cel mai bun model
    if test_acc > best_accuracy:
        best_accuracy = test_acc
        best_model_state = model.state_dict().copy()
    
    print(f"Epoca {epoch+1:2d}/{CONFIG['epochs']} | "
          f"Loss: {total_loss/len(train_loader):.4f} | "
          f"Train: {train_acc:.2f}% | "
          f"Test: {test_acc:.2f}% | "
          f"Best: {best_accuracy:.2f}%")

# 12. Încarcă cel mai bun model
model.load_state_dict(best_model_state)

# 13. Evaluare finală detaliată
print("\n[10] 📊 Evaluare finală...")

model.eval()
all_preds = []
all_targets = []

with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        pred = output.argmax(dim=1)
        all_preds.extend(pred.cpu().numpy())
        all_targets.extend(target.cpu().numpy())

final_acc = accuracy_score(all_targets, all_preds)
final_f1 = f1_score(all_targets, all_preds, average='weighted')

print(f"\n🎯 Rezultate finale:")
print(f"   Acuratețe: {final_acc:.2%}")
print(f"   F1-Score (weighted): {final_f1:.2%}")

# 14. Salvare
print("\n[11] 💾 Salvez modelul...")

os.makedirs('models/saved', exist_ok=True)

torch.save({
    'model_state_dict': model.state_dict(),
    'model_config': {
        'input_size': CONFIG['max_features'],
        'num_classes': num_classes,
        'hidden_sizes': CONFIG['hidden_sizes']
    },
    'accuracy': final_acc,
    'f1_score': final_f1
}, 'models/saved/model_optimizat.pt')

print("  ✅ Model salvat: models/saved/model_optimizat.pt")

joblib.dump(vectorizer, 'models/saved/vectorizer_optimizat.pkl')
joblib.dump(label_encoder, 'models/saved/label_encoder_optimizat.pkl')
joblib.dump(scaler, 'models/saved/scaler.pkl')

print("  ✅ Vectorizator, encoder și scaler salvați")

# 15. Testare
print("\n[12] 🧪 Testez cu exemple noi...")

model.eval()
exemple_test = [
    "Cum se fac clatite pufoase?",
    "Reteta de pizza cu ciuperci",
    "Ingrediente pentru ciorba de legume",
    "Sarmale traditionale romanesti",
    "Cum fac paine de casa?",
    "Branza de vaci reteta",
    "Tort de ciocolata",
    "Paste carbonara reteta originala",
    "Mici pe gratar",
    "Cozonac pufos de casa"
]

for exemplu in exemple_test:
    X_test = vectorizer.transform([exemplu]).toarray()
    X_test = scaler.transform(X_test)
    X_tensor = torch.FloatTensor(X_test).to(device)
    
    with torch.no_grad():
        output = model(X_tensor)
        pred = output.argmax(dim=1).item()
    
    intentie = label_encoder.inverse_transform([pred])[0]
    confidenta = torch.softmax(output, dim=1)[0][pred].item()
    print(f"  '{exemplu}' → {intentie} (confidență: {confidenta:.2%})")

# 16. Rezumat
print("\n" + "=" * 70)
print("📊 REZUMAT FINAL")
print("=" * 70)
print(f"\n🔥 GPU: {torch.cuda.get_device_name(0)}")
print(f"📁 Total retete: {len(toate_retetele)}")
print(f"📝 Exemple valide: {len(texte_filtrate)}")
print(f"🏷️ Clase originale: 1027")
print(f"🏷️ Clase grupate: {num_classes}")
print(f"🎯 Acuratețe finală: {final_acc:.2%}")
print(f"🎯 F1-Score: {final_f1:.2%}")
print(f"\n💾 Modele salvate:")
print(f"   - models/saved/model_optimizat.pt (PyTorch + CUDA)")
print(f"   - models/saved/vectorizer_optimizat.pkl")
print(f"   - models/saved/label_encoder_optimizat.pkl")
print(f"   - models/saved/scaler.pkl")
print("\n✅ Antrenare completată cu succes!")