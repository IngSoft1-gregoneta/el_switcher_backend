import os
import sys

# Define the imports to add
imports = ["from models.fig_card import FigType, FigCard\n"]


def add_imports_to_file(filepath):
    # Read the file's contents
    with open(filepath, "r") as file:
        lines = file.readlines()

    # Check if imports are already in the file
    if all(import_line in lines for import_line in imports):
        print(f"Imports already exist in {filepath}")
        return

    # Write the imports at the top, then add the rest of the file's content
    with open(filepath, "w") as file:
        file.writelines(imports + lines)
    print(f"Added imports to {filepath}")


def main(directory):
    # Go through each .py file in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            add_imports_to_file(filepath)


if __name__ == "__main__":
    # Check if the directory argument was provided
    if len(sys.argv) != 2:
        print("Usage: python add_imports.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]
    main(target_directory)
