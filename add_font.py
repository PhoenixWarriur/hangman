import site
import os


def find_library_path(library_name):
    try:
        # Get a list of all site-specific directories where libraries are installed
        site_dirs = site.getsitepackages()

        # Iterate through the directories and check if the library exists in any of them
        for site_dir in site_dirs:
            library_path = os.path.join(site_dir, library_name)
            if os.path.exists(library_path):
                return library_path

        # If the library is not found in any of the site directories, return None
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def add_file_to_directory(source_file_path, destination_directory):
    try:
        # Get the file name from the source file path
        file_name = os.path.basename(source_file_path)

        # Combine the destination directory and file name to get the full destination path
        destination_file_path = os.path.join(destination_directory, file_name)

        # Copy the source file to the destination directory
        os.makedirs(destination_directory, exist_ok=True)  # Create the destination directory if it doesn't exist
        os.replace(source_file_path, destination_file_path)

        print(f"File '{source_file_path}' added to '{destination_directory}' successfully.")

    except Exception as e:
        print(f"Error: {e}")

library_name = 'pyfiglet'
library_path = find_library_path(library_name)
source_file_path = 'big_money-ne.flf'

add_file_to_directory(source_file_path, library_path + '\\fonts')
