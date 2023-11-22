import bpy
import os

def export_scene_to_glb(blend_file_path, output_folder):
    # Open the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Construct the GLB file path
    base_name = os.path.splitext(os.path.basename(blend_file_path))[0]
    glb_output_path = os.path.join(output_folder, base_name + ".glb")

    # Export to GLB
    bpy.ops.export_scene.gltf(filepath=glb_output_path, export_format='GLB')
    print(f"Exported {blend_file_path} to {glb_output_path}")

# Path to the output folder
output_folder = 'F:\\x1x1\\output'

# Read the file paths from a text file
with open('F:\\x1x1\\files_to_process.txt', 'r') as file:
    files_to_process = file.read().splitlines()

# Process each file
for blend_file_path in files_to_process:
    export_scene_to_glb(blend_file_path, output_folder)
