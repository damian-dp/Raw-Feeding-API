# Pet Raw Feeding API

This API is designed to support a raw feeding recipe management system for dog owners. It allows users to create, manage, and share recipes for raw dog food, tailored to their pets' specific needs.

## Key Features:

1. User Management:
   - User registration and authentication
   - Profile management (update details, change password)
   - User roles (regular users, admins)

2. Dog Management:
   - Add, update, and remove dogs from a user's profile
   - Store essential information like breed, weight, and age

3. Recipe Creation and Management:
   - Create custom raw feeding recipes
   - Assign recipes to one or more dogs
   - Mark recipes as public or private
   - Edit and delete recipes

4. Ingredient Database:
   - Comprehensive list of approved raw feeding ingredients
   - Nutritional information for each ingredient (calories, protein, fat)
   - Categorisation of ingredients

5. Recipe Ingredients Management:
   - Add ingredients to recipes with specific quantities
   - Remove or update ingredients in recipes
   - Calculate nutritional totals for recipes

6. Dog-Recipe Association:
   - Assign multiple recipes to a dog
   - View all recipes for a specific dog
   - Remove recipe assignments from dogs

7. Shopping List Generation:
   - Generate shopping lists based on selected recipes
   - Aggregate ingredients across multiple recipes

8. Search and Filtering:
   - Search recipes by name, ingredients, or dog
   - Filter recipes by public/private status
   - Search ingredients by name or category

9. Nutritional Analysis:
   - Calculate nutritional content of recipes
   - Compare recipe nutrition to dog's requirements

## How It Works:

1. Users register and create profiles for their dogs.
2. Users can create custom recipes using the ingredient database.
3. Recipes are assigned to one or more dogs, ensuring each recipe has a purpose.
4. The API calculates nutritional information for recipes based on ingredients and quantities.
5. Users can generate shopping lists for selected recipes.
6. Recipes can be shared publicly, allowing other users to view and use them.