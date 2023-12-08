import bpy
import os

TARGET_SIZE_MB = 80  # Target file size in MB

def resize_image(image, scale_factor):
    if image.size[0] > 0 and image.size[1] > 0:
        new_size = (int(image.size[0] * scale_factor), int(image.size[1] * scale_factor))
        image.scale(new_size[0], new_size[1])

def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)  # Size in MB

def process_glb_file(glb_path, target_size):
    # Clear existing data
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Import GLB file
    bpy.ops.import_scene.gltf(filepath=glb_path)

    # Initial scale factor for resizing images
    scale_factor = 0.5

    while True:
        # Resize textures
        for mat in bpy.data.materials:
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        resize_image(node.image, scale_factor)

        # Export the model
        bpy.ops.export_scene.gltf(filepath=glb_path)

        # Check the file size
        current_size = get_file_size(glb_path)
        if current_size <= target_size:
            break
        else:
            # Increase the aggressiveness of the scale factor
            scale_factor *= 0.75  # You can adjust this factor

# Path to your GLB files
path_to_glb_files = 'C:\\Users\\filsuf\\Desktop\\test'

# Process each GLB file in the directory
for filename in os.listdir(path_to_glb_files):
    if filename.lower().endswith('.glb'):
        glb_path = os.path.join(path_to_glb_files, filename)
        process_glb_file(glb_path, TARGET_SIZE_MB)


#blender --background --python c:\t.py
