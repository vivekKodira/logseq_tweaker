# This resets the sample Logseq workspace to its inital state. Do NOT run it.

import os
from pathlib import Path
import shutil
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    workspace_path = '/Users/vivekkodira/work/logseq_tweaker/sample_workspace'
    if str(Path.cwd()) != '/Users/vivekkodira/work/logseq_tweaker/script':
        print("Stop! This script is not meant to be run on actual workspaces")
        exit()
    directories = ["journals", "pages"]
    for directory in directories:
        try:
            source = str(Path.cwd()) + "/workspace_initial/"+directory
            target = workspace_path+"/"+directory
            if os.path.exists(target):  # Check if it's a folder
                shutil.rmtree(target)
            shutil.copytree(source , target)
        except FileNotFoundError:
            print(f"{directory} does not exist.")
        except PermissionError:
            print(f"Permission denied: {directory}")
        except Exception as e:
            print(f"Error: {e}")
    print("Workspace reset successfully.")