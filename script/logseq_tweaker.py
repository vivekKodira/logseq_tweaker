import re
import os
import json

from dotenv import load_dotenv
from folder_reader import read_files_in_folder

# Load environment variables from a .env file
load_dotenv()

CHILD_BLOCK_STRICT_MODE = None

def extract_reference_words(text):
    """
    Extracts words wrapped with [[ and ]] or preceded by #.
    
    :param text: The input string
    :return: A list of matched words
    """
    # Regular expression to match words wrapped in [[ ]] or preceded by #
    pattern = r'\[\[(.*?)\]\]|#(\w+)'
    matches = re.findall(pattern, text)
    
    # Combine matches from both groups and filter out empty strings
    results = [match[0] or match[1] for match in matches]
    return results

def get_unique_items(input_array):
    return list(set(input_array))

def find_missing_files_by_names(references, folder):
    # Loop through each filename in the provided list
    references_list = list(references.keys())
    for reference in references_list:
        # Generate the full path to the file
        file_path = os.path.join(folder, reference + '.md')
        references[reference]["exists"] = "Y" if os.path.isfile(file_path) else "N"

def parse_journal(file_name, file_content, references):
    lines = file_content.split('\n');
    base_name, extension = os.path.splitext(file_name)
    for i, line in enumerate(lines):
        topics = extract_reference_words(line)
        if topics:
            for topic in topics:
                if topic not in references:
                    references[topic] = {"journals":{}}
                topic_references = references[topic]
                child_blocks = []
                if not CHILD_BLOCK_STRICT_MODE:
                        child_blocks.append(line.strip())
                # Look ahead at the next lines to find child blocks
                j = i + 1
                shouldloop = True
                while j < len(lines) and shouldloop:
                    next_line = lines[j]
                    # IF the line is indented and not empty, add it to the child block
                    if (next_line.startswith('   ') or next_line.startswith('\t')) and next_line.strip():
                        child_blocks.append(next_line.strip())
                    else:
                        shouldloop = False
                    j += 1
                if child_blocks:
                    if base_name not in topic_references["journals"]:
                        topic_references["journals"][base_name] = []
                    topic_references["journals"][base_name] += child_blocks
    return references

def write_to_file(file_path, references, reference, mode="w"):
    pages_path = file_path + '/pages'
    file_path = pages_path+'/'+reference+'.md'
    file_contents = ""
    if mode == 'a':
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
    with open(file_path, mode) as f:
        if mode == "a":
            f.write(f"\n\n")
        for journal, child_blocks in references[reference]["journals"].items():
            f.write(f"- [[{journal}]]\n")
            for child_block in child_blocks:
                if file_contents.find(child_block) == -1:
                    f.write(f"\t{child_block}\n")
                    if os.getenv("TRANSFER_MODE") == "MOVE":
                        delete_line_containing_string(file_path+'/journals/'+journal+'.md', child_block)
            f.write("\n")
    return

def write_output(references, file_path):
    pages_path = file_path + '/pages'
    missing_references = []
    existing_references = []
    reference_keys = list(references.keys())
    for key in reference_keys:
        if references[key]["exists"] == "N":
            missing_references.append(key)
    existing_references = set(reference_keys) - set(missing_references)
    with open(pages_path+'/logseq_tweaker_output.md', 'w') as f:
        f.write(f"This file is generated automatically each time the logseq_tweaker program is run.\n\n")
        f.write(f"## Missing References (These have been created as files and the contents added)\n")
        for missing_reference in missing_references:
            f.write(f"\t- [[{missing_reference}]]\n")
        f.write(f"## Child References in journals pointing to existing files\n")
        for existing_reference in existing_references:
            f.write(f"\t- [[{existing_reference}]]\n")
    for missing_reference in missing_references:
        write_to_file(file_path, references, missing_reference, 'w')
    for existing_reference in existing_references:
        write_to_file(file_path, references, existing_reference, 'a')
    return

def delete_line_containing_string(file_path, target_string):
    try:
        # Read all lines from the file
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Filter out lines containing the target string
        updated_lines = [line for line in lines if target_string not in line]
        
        # Write the updated lines back to the file
        with open(file_path, "w") as file:
            file.writelines(updated_lines)
        
        print(f"Lines containing '{target_string}' have been removed from {file_path}.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    workspace_path = os.getenv("WORKSPACE_PATH")
    if not workspace_path:
        workspace_path = input("Enter the path to the Logseq folder: ")
    isStrictMode = os.getenv("CHILD_BLOCK_STRICT_MODE")
    if not isStrictMode:
        isStrictMode = input("Enable strict mode for child blocks? (Y/N): ")
    CHILD_BLOCK_STRICT_MODE = isStrictMode == "Y"

    references = {}
    try:
        files = read_files_in_folder(workspace_path + '/journals')
        for file_name, content in files.items():
            # parse the journal and find all the references
            parse_journal(file_name, content, references)
        find_missing_files_by_names(references, workspace_path + '/pages')
        #print(json.dumps(references, indent=4))
        write_output(references, workspace_path)
        print("Output has been written to logseq_tweaker_output.md")

    except Exception as e:
        print(f"Error: {e}")
