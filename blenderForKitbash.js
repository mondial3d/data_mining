import bpy
import os

# Function to export a single object as GLB
def export_glb(obj, file_path):
    # Make a duplicate of the object and its children up to 2 levels deep
    duplicates = duplicate_hierarchy(obj, 2)
    
    # Move duplicates to the origin and select them
    for dup in duplicates:
        dup.location = (0, 0, 0)
        dup.select_set(True)
    
    # Export the selected objects
    bpy.ops.export_scene.gltf(filepath=file_path, use_selection=True, export_format='GLB')

    # Delete the duplicates
    bpy.ops.object.delete()

# Duplicate an object and its children up to 'levels' deep
def duplicate_hierarchy(obj, levels):
    if levels < 0:
        return []
    
    duplicates = []
    
    # Duplicate the object
    obj_duplicate = obj.copy()
    obj_duplicate.data = obj.data.copy()
    bpy.context.collection.objects.link(obj_duplicate)
    duplicates.append(obj_duplicate)
    
    # Duplicate children
    for child in obj.children:
        duplicates.extend(duplicate_hierarchy(child, levels - 1))
    
    return duplicates

# Directory to save the GLB files
output_directory = 'C:\\Users\\meta\\Desktop\\file\\GLB'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
print("Output directory ensured")

# Function to get the hierarchy level of an object
def get_hierarchy_level(obj):
    level = 0
    while obj.parent:
        level += 1
        obj = obj.parent
    return level

# Loop through all mesh objects in the scene
for obj in bpy.data.objects:
    # Check if the object is a mesh and its hierarchy level
    if obj.type == 'MESH' and get_hierarchy_level(obj) <= 2:
        # Prepare the file name and path
        file_name = f"{obj.name}.glb"
        file_path = os.path.join(output_directory, file_name)
        
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Export the object and its hierarchy up to 2 levels deep
        try:
            export_glb(obj, file_path)
            print(f"Exported {file_name}")
        except Exception as e:
            print(f"Failed to export {file_name}: {str(e)}")

print("Export complete.")
