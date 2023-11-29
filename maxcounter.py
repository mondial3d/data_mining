import os

def find_max_file_count(directory):
    max_count = 0
    folder_with_max_count = ""

    for root, dirs, files in os.walk(directory):
        current_count = sum(1 for file in files if file.endswith('.max'))
        if current_count > max_count:
            max_count = current_count
            folder_with_max_count = root

    return folder_with_max_count, max_count

# Example usage:
# folder, count = find_max_file_count("path_to_your_directory")
# print(f"The folder with the most '.max' files is: {folder} with {count} files.")
