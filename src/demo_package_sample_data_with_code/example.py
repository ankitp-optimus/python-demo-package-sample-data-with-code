"""
Reads and prints approximations to (a) π, from a text file at the root of the package source directory and (b) `e` from
a text file in a subfolder "sample_data". 
"""

from importlib.resources import files

import sys

import demo_package_sample_data_with_code.constants as constants

def print_value_from_resource(message, packagename, filename):
    """
    Outputs the text read from a resource (identified by its immediately enclosing package and the resource’s filename),
    and prefix this output by the supplied `message`.
    """
    data = read_text_from_resource(packagename, filename)
    print(f"{message}: {data}")

def read_text_from_resource(packagename, filename):
    """
    Read and return text from a resource identified by its immediately enclosing package and the resource’s filename.

    If either the file/module is not found, or if the returned string is empty, instead return a string expressing
    cluelessness that will be incorporated into __main__.py's output.
    """
    try:
        # The following is equivalent to using the “/” in the next following line.
        # resource_location_as_string = files(packagename).joinpath(filename)
        resource_location_as_string = files(packagename) / filename

        # Use the following substitute only to test the "module not found" trap
        # resource_location_as_string = files('nonexistent_package') / filename

        data = resource_location_as_string.read_text()

        if not data:
            data = constants.CLUELESS_STRING
            print(f"\nOops! I found and read the data file {filename}, but it was empty.")
            print(f"Location:\n»» {resource_location_as_string}.")


        # Uncomment next line to test unanticipated error in the try … except block
        # y = 3/0
        
    except ModuleNotFoundError as errormessage_MNF:
        print(f"\nOops! The package name «{packagename}» was not a module that could be found.")
        print(f"»» {errormessage_MNF}")
        data = constants.CLUELESS_STRING
        return data
    except FileNotFoundError as errormessage_FNF:
        print(f"\nOops! The data file «{filename}» wasn’t found at this location:\n»» {resource_location_as_string}.")
        print(errormessage_FNF)
        data = constants.CLUELESS_STRING
        return data
    else:
        return data
    