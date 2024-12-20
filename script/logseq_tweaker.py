import re

from folder_reader import read_files_in_folder, find_missing_files_by_names

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

def parse_journal(file_name, file_content):
    # print(f"\n--- Content of {file_name} has been read")
    references = []
    for line in file_content.split('\n'):
        topics = []
        topics += extract_reference_words(line)
        if topics:
            references += topics
    return get_unique_items(references)

if __name__ == "__main__":
    workspace_path = input("Enter the path to the Logseq folder: ")
    references = []
    try:
        files = read_files_in_folder(workspace_path + '/journals')
        for file_name, content in files.items():
            references += parse_journal(file_name, content)
        references = get_unique_items(references)
        missing_references = find_missing_files_by_names(references, workspace_path + '/pages')
        print(f"The following journal references are missing actual files: \n")
        print(missing_references)
    except Exception as e:
        print(f"Error: {e}")
