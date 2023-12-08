import bpy
import os
import math
from mathutils import Vector, Euler
import random
import string

def setup_scene():
    # Set the rendering engine to Cycles
    bpy.context.scene.render.engine = 'CYCLES'

    # Enable GPU rendering
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'OPTIX'  # Using OPTIX for RTX cards

    # Set the device to GPU
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    for device in bpy.context.preferences.addons['cycles'].preferences.devices:
        if device.type == 'OPTIX':
            device.use = True

    bpy.context.scene.cycles.device = 'GPU'

    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
   

    # Set up ambient lighting
    bpy.context.scene.world.light_settings.use_ambient_occlusion = True
    bpy.context.scene.world.light_settings.ao_factor = 1.5  # Slightly increased

    # Set background to white
    bpy.data.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (1, 1, 1, 1)

    # Add a sun lamp for stronger shadows
    sun_lamp_data = bpy.data.lights.new(name="Sun", type='SUN')
    sun_lamp_object = bpy.data.objects.new(name="Sun", object_data=sun_lamp_data)
    bpy.context.scene.collection.objects.link(sun_lamp_object)
    sun_lamp_object.location = (10, 10, 20)  # Adjust for desired shadow direction
    sun_lamp_object.rotation_euler = Euler((math.radians(50.0), math.radians(30.0), math.radians(45.0)), 'XYZ')
    sun_lamp_data.energy = 5.0  # Increased for stronger shadows

    # Add a camera
    cam = bpy.data.cameras.new("Camera")
    cam_obj = bpy.data.objects.new("Camera", cam)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam.type = 'PERSP'

    return cam_obj

def get_random_string(length):
    # Generates a random string of uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def normalize_object_scale(objects):
    # Calculate the combined bounding box of all objects
    min_coord = Vector((float('inf'), float('inf'), float('inf')))
    max_coord = Vector((float('-inf'), float('-inf'), float('-inf')))

    for obj in objects:
        obj_min = Vector(min([obj.matrix_world @ Vector(b) for b in obj.bound_box], key=lambda c: c.length))
        obj_max = Vector(max([obj.matrix_world @ Vector(b) for b in obj.bound_box], key=lambda c: c.length))
        min_coord = Vector(map(min, zip(min_coord, obj_min)))
        max_coord = Vector(map(max, zip(max_coord, obj_max)))

    # Scale and move all objects to fit within a standardized bounding box
    max_dimension = max(max_coord - min_coord)
    scale_factor = 1.0 / max_dimension if max_dimension > 0 else 1.0

    for obj in objects:
        obj.scale *= scale_factor
        obj.location -= min_coord * scale_factor

def fit_camera_to_objects(cam_obj, objects):
    normalize_object_scale(objects)

    # Calculate the center of all objects
    center = sum((obj.location for obj in objects), Vector()) / len(objects)

    # Adjust camera position
    cam_obj.location = center + Vector((0, -3, 2))
    cam_obj.rotation_euler = Euler((math.radians(60.0), 0.0, math.radians(45.0)), 'XYZ')

    # Frame all objects in the camera's view    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = cam_obj
    bpy.ops.view3d.camera_to_view_selected()

def import_file(file_path):
    # Import the file
    if file_path.endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=file_path)
    elif file_path.endswith('.obj'):
        bpy.ops.import_scene.obj(filepath=file_path)
    elif file_path.endswith('.stl'):
        bpy.ops.import_scene.stl(filepath=file_path)
    elif file_path.endswith('.blend'):
        bpy.ops.import_scene.blend(filepath=file_path)
    elif file_path.endswith('.glb') or file_path.endswith('.gltf'):
        bpy.ops.import_scene.gltf(filepath=file_path)
    return bpy.context.selected_objects

def import_and_process(file_path, output_folder):
    try:
        cam_obj = setup_scene()
        imported_objects = import_file(file_path)
        if not imported_objects:
            print(f"No objects imported for file: {file_path}")
            return

        fit_camera_to_objects(cam_obj, imported_objects)

        # Adjust render settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = 32
        bpy.context.scene.render.resolution_x = 960
        bpy.context.scene.render.resolution_y = 540
        bpy.context.scene.render.image_settings.file_format = 'PNG'

        # Create the filename for the rendered image
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        render_output = os.path.join(output_folder, base_name + '.png')

        # Render and save PNG
        bpy.context.scene.render.filepath = render_output
        bpy.ops.render.render(write_still=True)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

        
# Read the file list from the previously generated file
with open('C:\\Users\\meta\\Desktop\\file\\render.txt', 'r') as file:
    files_to_process = file.read().splitlines()

# Loop through each file
output_folder = 'D:\\maxGLB'  # Update to your desired output folder
for file_path in files_to_process:
    import_and_process(file_path, output_folder)


# this work like this 


#To run a Python script that uses Blender's Python API (bpy), you'll need to run the script within Blender's environment. Since you have Blender installed at C:\Program Files\Blender Foundation\Blender 3.6, you can either run the script directly in Blender or use Blender's command-line interface to execute the script. Here's how you can do both:

#Running the Script Inside Blender
#Open Blender:

#Navigate to the Blender installation folder (C:\Program Files\Blender Foundation\Blender 3.6).
#Run the Blender application.
#Load and Run the Script in Blender:

#In Blender, switch to the Scripting workspace.
#Open the Text Editor within Blender.
#Use the Open option in the Text Editor to load your Python script (FindMoveRenderAndGlbCreator.py).
#Once the script is loaded, click on the Run Script button to execute it.
#Running the Script Using Blender's Command-Line Interface
#Open Command Prompt:

#Press Win + R, type cmd, and press Enter to open the Command Prompt.
#Navigate to Blender's Directory:

#Type cd "C:\Program Files\Blender Foundation\Blender 3.6" and press Enter.
#Run the Script Using Blender's Python:

#Assuming Blender's executable is in this directory, run the script with the following command:

#blender --background --python c:\renderglb.py 
