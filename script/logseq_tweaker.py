'''
Generated using ChatGPT using the prompt 
"Write a python program to read each file in a specified folder into memory"
'''
import os
from pathlib import Path

def read_files_in_folder(folder_path):
    """
    Reads all files in the specified folder into memory.

    :param folder_path: Path to the folder containing the files
    :return: Dictionary with file names as keys and file contents as values
    """
    file_contents = {}

    # Ensure the folder path is valid
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory.")

    # Iterate over all files in the folder
    for file in folder.iterdir():
        if file.is_file():  # Ensure it's a file
            try:
                # Read the file's contents
                with open(file, 'r', encoding='utf-8') as f:
                    file_contents[file.name] = f.read()
            except Exception as e:
                print(f"Error reading {file.name}: {e}")

    return file_contents

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    try:
        files = read_files_in_folder(folder_path)
        for file_name, content in files.items():
            print(f"\n--- Content of {file_name} ---\n{content}\n")
    except Exception as e:
        print(f"Error: {e}")
