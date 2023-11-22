import os

def find_3d_files(root_folder, extensions):
    found_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(tuple(extensions)):
                found_files.append(os.path.join(root, file))
    return found_files

root_folder = 'D:\\download 3d file\\3D Scan Store – 10 x Animation Ready Body Scan Pack'  # Your specified root folder
extensions = ['.fbx', '.blend', '.obj', '.stl',".glb"]
files_to_process = find_3d_files(root_folder, extensions)

# Specify the output file path
output_file_path = 'F:\\x1x1\\files_to_process.txt'

# Export the list of file paths to a text file in F:\x1x1
with open(output_file_path, 'w', encoding='utf-8', errors='replace') as file:
    for path in files_to_process:
        file.write("%s\n" % path)
