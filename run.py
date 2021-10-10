import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('recipes')


def add_new_recipe():
    """
    Accepts user input to enter the name of a recipe, a URL,
    whether the recipe is for a vegan or vegetarian
    """

    while True:
        print("Please enter the name of the recipe, followed by the URL.\n")

        recipe_entry = input("Please enter your recipe name here\n")
        url_entry = input("Please enter the recipe's URL\n")

        user_entry = recipe_entry, url_entry

        if check_entry(recipe_entry, url_entry):
            print("Recipe entry is valid")
            break

    return user_entry


def check_entry(recipe, url):
    """
    Checks to see whether either the recipe entry or url entry is empty
    """
    if not recipe and not url:
        print("Recipe and url entry are empty, please add a recipe and url")
        return False
    elif not recipe:
        print("Recipe entry is empty, please add a recipe name")
        return False
    elif not url:
        print("URL entry is empty. Please add a URL")
        return False

    return True


def determine_worksheet():
    """
    Determines which worksheet the recipe should be appended
    to based on whether it is suitable for vegans or vegetarians
    """

    is_vegan = input("Is the recipe Vegan friendly? Yes or No\n")
    is_vegetarian = input("Is the recipe Vegetarian? Yes or No\n")

    if is_vegan == "Yes" and is_vegetarian == "Yes":
        worksheet = "vegan_recipes"
    elif is_vegan == "Yes" and is_vegetarian == "No":
        worksheet = "vegan_recipes"
    elif is_vegan == "No" and is_vegetarian == "Yes":
        worksheet = "vegetarian_recipes"
    elif is_vegan == "No" and is_vegetarian == "No":
        worksheet = "meat_recipes"
    elif not is_vegan == "Yes" or "No":
        f"The entry {is_vegan} is invalid. Please try again"
        return False
    elif not is_vegetarian == "Yes" or "No":
        f"The entry {is_vegetarian} is invalid. Please try again"
        return False

    return worksheet


def add_to_worksheet(recipes, worksheet):
    """
    Process the list of details into the corresponding
    worksheet. Updates the recipe and URL tab to include
    the data
    """
    print(f"Adding the delicious recipe to {worksheet} worksheet")
    update_worksheet = SHEET.worksheet(worksheet)
    update_worksheet.append_row(recipes)
    print(f"Recipe safely stored in the {worksheet} worksheet")


def run_again():
    """
    Provides the user with the option to run the program again
    """
    while True:
        print("Would you like to add another recipe?")
        repeat_entry = input("Yes or No\n")

        if repeat_entry == "Yes":
            main()
        elif repeat_entry == "No":
            print("Thank you for adding your recipes")
            return False
        elif not repeat_entry == "Yes" or "No":
            print("Please select a valid option")

    return repeat_entry


def main():
    """
    Runs all program functions
    """
    recipes = add_new_recipe()
    correct_worksheet = determine_worksheet()
    add_to_worksheet(recipes, correct_worksheet)
    run_again()


main()
