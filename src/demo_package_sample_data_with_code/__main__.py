"""
Reads data from packaged resources for π, e, and the meaning of life.

Entry point for package.
See, e.g., https://docs.python.org/3/library/__main__.html
"""

import demo_package_sample_data_with_code.constants as constants
from demo_package_sample_data_with_code.example import print_value_from_resource

print("I am here, in __main__.py.")
print("\n" + 15*"# " + "\n")
print_value_from_resource("π", constants.PACKAGENAME_PI, constants.FILENAME_PI)
print_value_from_resource("e", constants.PACKAGENAME_E, constants.FILENAME_E)
print_value_from_resource("Meaning of life", constants.PACKAGENAME_MOL, constants.FILENAME_MOL)
print("\n" + 15*"* " + "\n")
