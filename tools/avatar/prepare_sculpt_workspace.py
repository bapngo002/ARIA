"""Create a reference-only Blender workspace; does not generate a character mesh."""
from pathlib import Path
import bpy
from mathutils import Quaternion

root = Path(__file__).resolve().parents[2]
out = root / 'assets/characters/aria-custom'
out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = 'ARIA custom character - references only'
scene['status'] = 'REFERENCE SETUP ONLY: no new sculpt, rig or approved likeness yet.'
scene['reference_limit'] = 'AI-generated views are approximate, not calibrated orthographic geometry.'
refs = bpy.data.collections.new('Approved direction and approximate views')
scene.collection.children.link(refs)
for name, filename, x, size in (
    ('Concept 1 - visual target', '01-long-hair.png', -2.15, 1.9),
    ('Three-view reference - approximate angles', '01-turnaround-reference.png', .65, 3.5),
):
    image = bpy.data.images.load(str(root / 'docs/design/aria-face-concepts' / filename))
    image.pack()
    obj = bpy.data.objects.new(name, None)
    refs.objects.link(obj)
    obj.empty_display_type = 'IMAGE'
    obj.data = image
    obj.empty_display_size = size
    obj.location = (x, .05, 1.5)
    obj.rotation_euler = (1.57079632679, 0, 0)
    obj.hide_select = True
sculpt = bpy.data.collections.new('Custom sculpt - awaiting geometry')
scene.collection.children.link(sculpt)
notes = bpy.data.texts.new('START HERE')
notes.write('ARIA custom character\n\nReference-only workspace. The rejected anime model is not included.\n'
            'Create and sculpt a new head in the Custom sculpt collection.\n'
            'Match the original concept first; the generated three-view sheet is not a measured blueprint.\n'
            'No model, likeness, rig, facial expressions or Pi runtime is verified by this file.\n')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.overlay.show_floor = False
            space.region_3d.view_rotation = Quaternion((1, 0, 0), 1.57079632679)
            space.region_3d.view_perspective = 'ORTHO'
            space.region_3d.view_location = (-.45, 0, 1.5)
            space.region_3d.view_distance = 6.5
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(out / 'aria-custom-sculpt.blend'))
assert all(im.packed_file for im in bpy.data.images if im.source == 'FILE')
print('ARIA_REFERENCE_WORKSPACE_OK', bpy.app.version_string)
