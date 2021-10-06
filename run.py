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


def option_selection():
    """
    Provides the user with the option to add, amend, remove or
    print their recipes
    """
    while True:
        print("Please select from one of the following options\n")
        print("To add a new recipe, please enter 1\n")
        print("To amend an existing recipe, please enter 2\n")
        print("To delete an existig recipe, please enter 3\n")
        print("To print a number of recipes, please enter 4\n")

        option_choice = int(input("Please enter your choice here\n"))

        if option_choice == 1:
            add_new_recipe()
        elif option_choice == 2:
            amend_existing_recipe()
        elif option_choice == 3:
            delete_existing_choice()
        elif option_choice == 4:
            show_recipes()

        if validate_option(option_choice):
            print("Thank you for your selection\n")
            break

    return option_choice


def validate_option(entry):
    """
    Checks the user choice regarding whether to add, amend, delete
    or view existing recipes. Returns a ValueError if the number
    is not an integer, or whether it is not one of the four
    numbers
    """
    try:
        if entry == 0 or entry >= 5:
            raise ValueError(
                f"Please enter a valid number. You entered {entry}"
            )
    except ValueError as incorrect:
        print(f"Invalid data: {incorrect}, please try again\n")
        return False

    return True


def add_new_recipe():
    """
    Accepts user input to enter the name of a recipe, a URL,
    whether the recipe is for a vegan or vegetarian
    """

    while True:
        print("Please enter the name of the recipe, followed by the URL.")

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
    if not recipe and url:
        print("Recipe and url entry are empty, please add a recipe and url")
    elif not recipe:
        print("Recipe entry is empty, please add a recipe name")
    elif not url:
        print("URL entry is empty. Please add a URL")

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


def amend_existing_recipe():
    """
    Pulls through the existing data from the specified worksheet
    Prints the values as a dictionary to allow the user to indicate
    which item to amend
    """
    print("To amend the meat recipe list, please enter 1")
    print("To amend the vegan recipe list, please enter 2")
    print("To amend the vegetarian recipe, please enter 3\n")
    user_choice = int(input("Please enter your choice here"))

    if user_choice == 1:
        worksheet = "meat_recipes"
    elif user_choice == 2:
        worksheet = "vegan_recipes"
    elif user_choice == 3:
        worksheet = "vegetarian_recipes"

    return worksheet


def delete_existing_choice():
    """
    Pulls through the existing data from the specified worksheet
    Prints the values as a dictionary to allow the user to indicate
    which item to delete
    """


def show_recipes():
    """
    Pulls through a random number of recipes from the google sheet
    and prints to the terminal
    """


def repeat_process():
    """
    Provides the user with the option to return to the beginning
    to add another recipe
    """

    user_choice = input("Would you like to start again? Yes or No\n")
    if user_choice == "Yes":
        option_selection()
    elif user_choice == "No":
        print("Thank you for action")
    else:
        print("Please enter a valid option")
        repeat_process()


option_selection()
recipes = add_new_recipe()
correct_worksheet = determine_worksheet()
add_to_worksheet(recipes, correct_worksheet)
repeat_process()
