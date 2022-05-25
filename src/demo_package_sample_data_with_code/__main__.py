"""
Reads data from packaged resources for π, e, and the meaning of life.

Entry point for package.
See, e.g., https://docs.python.org/3/library/__main__.html
"""

import os

from . import constants
from . my_module import check_CLI_for_user_input
from . my_module import print_value_from_resource


def main():
    print("I am here, in __main__.py.")
    print("\n" + 15*"# " + "\n")

    print(f"\nThe current working directory: {os.getcwd()} \n")

    # Checks for command line argument 
    user_contribution = check_CLI_for_user_input()
    if len(user_contribution) == 0:
        print("The user declined to share any knowledge. 🙁\n")
    else:
        user_wisdom = " ".join(user_contribution)
        print(f"The user chose to share: “{user_wisdom}”\n")

    print_value_from_resource("π", constants.PACKAGENAME_PI, constants.FILENAME_PI)
    print_value_from_resource("e", constants.PACKAGENAME_E, constants.FILENAME_E)
    print("\nPlease don’t be concerned when you see the following error message. It’s expected.")
    print_value_from_resource("Meaning of life", constants.PACKAGENAME_MOL, constants.FILENAME_MOL)
    print("\n" + 15*"* " + "\n")


if __name__ == "__main__":
    main()