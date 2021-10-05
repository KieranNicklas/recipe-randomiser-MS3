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

        user_entry = [recipe_entry, url_entry]

        if check_entry(user_entry):
            print("Recipe entry is valid")
            break

    return user_entry


def check_entry(values):
    """
    Inside the try, converts the values to strings.
    Raises a TypeError if the value cannot be converted
    to a string, or if there are not for entries.
    """
    try:
        [str(entries) for entries in values]
        if not len(values):
            raise TypeError(
                f"Four entries are required. You have provided {len(values)}\n"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again\n")
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
    else:
        worksheet = "meat_recipes"

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


recipes = add_new_recipe()
correct_worksheet = determine_worksheet()
add_to_worksheet(recipes, correct_worksheet)
