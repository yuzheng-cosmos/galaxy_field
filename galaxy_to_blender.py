import bpy
import os
import random

def import_images_and_distribute(image_folder, volume_size, num_images=None, color_ramp_positions=None):
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Create an empty object to act as the global transparency controller
    controller = bpy.data.objects.new("Transparency_Controller", None)
    bpy.context.collection.objects.link(controller)

    # Add a custom property to the controller for global transparency
    controller["global_transparency"] = 1.0

    # Get all image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
    
    # If num_images is not specified, use all images
    if num_images is None:
        num_images = len(image_files)
    image_files = image_files[:num_images]

    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        
        # Import image as plane
        bpy.ops.import_image.to_plane(files=[{"name": img_file}], directory=image_folder)
        
        # Get the imported plane
        plane = bpy.context.active_object
        
        # Create an emission shader with transparency
        mat = bpy.data.materials.new(name="Emission_Transparent_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        mat.node_tree.nodes.remove(bsdf)
        
        # Add Emission Shader
        emission = mat.node_tree.nodes.new(type="ShaderNodeEmission")
        
        # Add Transparent Shader
        transparent = mat.node_tree.nodes.new(type="ShaderNodeBsdfTransparent")
        
        # Add Mix Shader
        mix_shader = mat.node_tree.nodes.new(type="ShaderNodeMixShader")
        
        # Add Image Texture
        tex_image = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
        tex_image.image = bpy.data.images.load(img_path)
        
        # Connect Image Texture Color to Emission Color
        mat.node_tree.links.new(tex_image.outputs["Color"], emission.inputs["Color"])
        
        # Add Math Node to control emission strength
        math_node = mat.node_tree.nodes.new(type="ShaderNodeMath")
        math_node.operation = 'MULTIPLY'
        math_node.inputs[1].default_value = 2.0  # Adjust this value to control brightness
        
        mat.node_tree.links.new(tex_image.outputs["Color"], math_node.inputs[0])
        mat.node_tree.links.new(math_node.outputs[0], emission.inputs["Strength"])
        
        # Add RGB to BW node
        rgb_to_bw = mat.node_tree.nodes.new(type="ShaderNodeRGBToBW")
        mat.node_tree.links.new(tex_image.outputs["Color"], rgb_to_bw.inputs["Color"])
        
        # Add Color Ramp node
        color_ramp = mat.node_tree.nodes.new(type="ShaderNodeValToRGB")
        color_ramp.color_ramp.interpolation = 'LINEAR'
        if color_ramp_positions:
            color_ramp.color_ramp.elements[0].position = color_ramp_positions[0]
            color_ramp.color_ramp.elements[1].position = color_ramp_positions[1]
        
        mat.node_tree.links.new(rgb_to_bw.outputs["Val"], color_ramp.inputs["Fac"])
        
        # Add a Math Node to multiply the color ramp output with global transparency
        transparency_math = mat.node_tree.nodes.new(type="ShaderNodeMath")
        transparency_math.operation = 'MULTIPLY'
        
        mat.node_tree.links.new(color_ramp.outputs["Color"], transparency_math.inputs[0])
        transparency_math.inputs[1].default_value = 1.0  # This will be controlled by the driver
        
        # Add driver to the second input of the transparency_math node
        driver = transparency_math.inputs[1].driver_add("default_value").driver
        driver.type = 'SCRIPTED'
        
        var = driver.variables.new()
        var.name = 'global_transparency'
        var.targets[0].id = controller
        var.targets[0].data_path = '["global_transparency"]'
        
        driver.expression = 'global_transparency'
        
        # Connect the transparency_math output to the Mix Shader Fac input
        mat.node_tree.links.new(transparency_math.outputs["Value"], mix_shader.inputs["Fac"])
        
        # Connect Emission and Transparent shaders to Mix Shader
        mat.node_tree.links.new(transparent.outputs["BSDF"], mix_shader.inputs[1])
        mat.node_tree.links.new(emission.outputs["Emission"], mix_shader.inputs[2])
        
        # Connect Mix Shader to Material Output
        mat.node_tree.links.new(mix_shader.outputs["Shader"], mat.node_tree.nodes["Material Output"].inputs["Surface"])
        
        # Assign material to plane
        if plane.data.materials:
            plane.data.materials[0] = mat
        else:
            plane.data.materials.append(mat)
        
        # Set blend mode and shadow mode for transparency
        plane.active_material.blend_method = 'BLEND'
        plane.active_material.shadow_method = 'NONE'

        # Randomly position the plane within the volume
        plane.location = (
            random.uniform(-volume_size / 2, volume_size / 2),
            random.uniform(-volume_size / 2, volume_size / 2),
            random.uniform(-volume_size / 2, volume_size / 2)
        )

        # Randomly rotate the plane
        plane.rotation_euler = (
            random.uniform(0, 3.14159),
            random.uniform(0, 3.14159),
            random.uniform(0, 3.14159)
        )

# Folder containing the images
image_folder = '/Users/yuzheng/Downloads/galaxy_field/cropped_images'

# Size of the cube volume (e.g., 100)
volume_size = 10

# Number of images to import (None means import all images)
num_images = 10

# Color ramp positions for transparency (adjust as needed)
color_ramp_positions = [0,0.7]

import_images_and_distribute(image_folder, volume_size, num_images, color_ramp_positions)
