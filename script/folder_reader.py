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

def find_missing_files_by_names(filenames, folder):
    # List to store the paths of found files
    missing_files = []
    
    # Loop through each filename in the provided list
    for filename in filenames:
        # Generate the full path to the file
        file_path = os.path.join(folder, filename + '.md')
        # print(f"\n-- Finding files in {folder} for {file_path}")
        
        # Check if the file exists in the folder
        if not os.path.isfile(file_path):
            missing_files.append(filename)
        
    
    return missing_files