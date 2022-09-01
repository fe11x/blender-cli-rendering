# blender --background --python 08_greasepencil_animation.py --render-frame 1 -- </path/to/output/image> <resolution_percentage> <num_samples>

# blender --background --python 08_animation.py --render-anim -- /tmp/a 50 8
# ffmpeg -r 10 -i /tmp/a%04d.png -pix_fmt yuv420p out.mp4     # fps 10 image per second

import bpy
import os
import sys

working_dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(working_dir_path)

import utils
from utils import init_grease_pencil, draw_line, draw_circle, draw_sphere, draw_sphere_on_timeline


#if __name__ == '__main__':
if True:
    material = bpy.data.materials.new("mymaterial")
    bpy.data.materials.create_gpencil_data(material)
    material.grease_pencil.color = (1, 0, 0, 1) # color red

    gp_layer = init_grease_pencil(material=material)
    gp_frame = gp_layer.frames.new(0)

    draw_line(gp_frame, (0, 0, 0), (1, 0, 0))
    draw_line(gp_frame, (1, 0, 0), (1, 0, 1))

    draw_circle(gp_frame, (0, 0, 0), 2, 32)
    draw_sphere(gp_frame, 1, 2)

    draw_sphere_on_timeline(gp_layer, 1, 60)

    # Args
    output_file_path = bpy.path.relpath(str(sys.argv[sys.argv.index('--') + 1]))
    resolution_percentage = int(sys.argv[sys.argv.index('--') + 2])
    num_samples = int(sys.argv[sys.argv.index('--') + 3])

    scene = bpy.context.scene

    # Animation Setting
    utils.set_animation(scene, fps=24, frame_start=1, frame_end=60)    # gen 60 frames

    # Render Setting
    camera_object = bpy.data.objects["Camera"]
    utils.set_output_properties(scene, resolution_percentage, output_file_path)
    utils.set_eevee_renderer(scene, camera_object, num_samples)     # faster

    # Set world
    world = bpy.data.worlds['World']
    world.use_nodes = True
    # changing these values does affect the render.
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
    bg.inputs[1].default_value = 1.0
