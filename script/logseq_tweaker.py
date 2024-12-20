import re
import os

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
    for i, line in enumerate(lines):
        topics = extract_reference_words(line)
        if topics:
            for topic in topics:
                if topic not in references:
                    references[topic] = {"journals":{}}
                topic_references = references[topic]
                if file_name not in topic_references["journals"]:
                    topic_references["journals"][file_name] = []
                
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
                    topic_references["journals"][file_name] += child_blocks
    return references

def write_output(references, file_path):
    missing_references = []
    existing_references = []
    reference_keys = list(references.keys())
    for key in reference_keys:
        if references[key]["exists"] == "N":
            missing_references.append(key)
    existing_references = set(reference_keys) - set(missing_references)
    with open(file_path+'/logseq_tweaker_output.md', 'w') as f:
        f.write(f"This file is generated automatically each time the logseq_tweaker program is run.\n\n")
        f.write(f"## Missing References\n")
        for missing_reference in missing_references:
            f.write(f"\t- [[{missing_reference}]]\n")
        
        f.write(f"## Child References in journals pointing to existing files\n")
        for existing_reference in existing_references:
            f.write(f"\t- [[{existing_reference}]]\n")

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
        # print(references)
        write_output(references, workspace_path + '/pages')
        print("Output has been written to logseq_tweaker_output.md")
    except Exception as e:
        print(f"Error: {e}")
