import bpy
import os

# Function to export a single object as GLB
def export_glb(obj, file_path):
    duplicates = duplicate_hierarchy(obj, 2)
    for dup in duplicates:
        dup.location = (0, 0, 0)
        dup.select_set(True)
    bpy.ops.export_scene.gltf(filepath=file_path, use_selection=True, export_format='GLB')
    bpy.ops.object.delete()

# Duplicate an object and its children up to 'levels' deep
def duplicate_hierarchy(obj, levels):
    if levels < 0:
        return []
    duplicates = []
    obj_duplicate = obj.copy()
    obj_duplicate.data = obj.data.copy()
    bpy.context.collection.objects.link(obj_duplicate)
    duplicates.append(obj_duplicate)
    for child in obj.children:
        duplicates.extend(duplicate_hierarchy(child, levels - 1))
    return duplicates

# Function to get the hierarchy level of an object
def get_hierarchy_level(obj):
    level = 0
    while obj.parent:
        level += 1
        obj = obj.parent
    return level

# Function to recursively find all .blend files in a directory
def find_blend_files(directory):
    blend_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".blend"):
                blend_files.append(os.path.join(root, file))
    return blend_files

# Directory containing .blend files
blend_files_directory = 'D:\\download 3d file'
output_directory = 'D:\\download 3d file\\export'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
print("Output directory ensured")

# Get all .blend files
blend_files = find_blend_files(blend_files_directory)

for blend_file in blend_files:
    # Open the blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file)

    # Loop through all mesh objects in the scene
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and get_hierarchy_level(obj) <= 2:
            file_name = f"{obj.name}.glb"
            file_path = os.path.join(output_directory, file_name)
            bpy.ops.object.select_all(action='DESELECT')
            try:
                export_glb(obj, file_path)
                print(f"Exported {file_name}")
            except Exception as e:
                print(f"Failed to export {file_name}: {str(e)}")

    print(f"Processed {blend_file}")

print("All files processed.")


#Type cd "C:\Program Files\Blender Foundation\Blender 3.6" and press Enter.
#Run the Script Using Blender's Python:  this code is just work with 3.6 blender is not work in 4 or 3 

#Assuming Blender's executable is in this directory, run the script with the following command:

#blender --background --python c:\FindAllBlendAndConvert.py 
