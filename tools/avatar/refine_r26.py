from pathlib import Path
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r26-review';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r25-review/aria-head-r25.blend'))
h=bpy.data.objects['ARIA R25 - face'];h.name='ARIA R26 - face';mask=h.data.color_attributes['PhotoProjectionWeight']
for v in h.data.vertices:
 x,y,z=v.co
 if z>1.25:
  side=max(0,min(1,(.050-abs(x))/.019));side=side*side*(3-2*side);old=mask.data[v.index].color[0];mask.data[v.index].color=(old*side,old*side,old*side,1)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R26 appearance study with central facial projection. Likeness is incomplete; no facial rig or final export claimed.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r26.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R26_SAVED')
