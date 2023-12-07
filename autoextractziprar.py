import subprocess
import os

def extract_rar(file_path, extract_path):
    try:
        # Ensure the directory exists
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        # Running the 7z command
        subprocess.run(['7z', 'x', file_path, '-o' + extract_path, '-aoa'], check=True)

        print(f"Extracted to: {extract_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def unzip_all_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.rar'):
                file_path = os.path.join(root, file)
                print(f"Unzipping: {file_path}")
                extract_path = os.path.join(root, os.path.splitext(file)[0])
                extract_rar(file_path, extract_path)

unzip_all_in_directory('D:\\files\\files')


#cd c:/ python FindMoveZip.py   you should install 7zip and set the path in windows ...
