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
        print("Please enter the name of the recipe, followed by the URL.")
        print("Then, please enter whether the recipe is suitable for Vegans") 
        print("And finally, Vegetarians")

        recipe_entry = input("Please enter your recipe name here\n")
        url_entry = input("Please enter the recipe's URL\n")
        is_vegan = input("Is the recipe Vegan friendly? Yes or No\n")
        is_vegetarian = input("Is the recipe Vegetarian? Yes or No\n")

        user_entry = recipe_entry, url_entry, is_vegan, is_vegetarian

        if check_entry(user_entry):
            print(f"{user_entry} is valid")
            break

    return user_entry


def check_entry(values):
    try:
        [str(entries) for entries in values]
        if len(values) != 4:
            raise ValueError(
                f"Four entries are required. You have provided {len(values)}\n"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again\n")
        return False

    return True


add_new_recipe()