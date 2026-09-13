from pathlib import Path
import bpy, numpy as np, math
from mathutils import Vector
root=Path(__file__).resolve().parents[2]; out=root/'assets/characters/aria-custom/r17-clean-hair'; out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r16-review/aria-head-r16.blend'))
hair=bpy.data.objects['ARIA R16 - hair volume'];hair.name='ARIA R17 - clean hair projection';d=hair.data
front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0];side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
# Sample only high-confidence hair pixels, preserving source rows wherever possible.
for name,mask,offset in [('Front',front,0),('Side',side,516)]:
 uv=d.uv_layers[name]; threshold=float(mask.max())*.88
 for lp in d.loops:
  u,v=uv.data[lp.index].uv;py=max(0,min(395,round((1-v)*396)));px=max(0,min(mask.shape[1]-1,round(u*773-offset)))
  if mask[py,px]<threshold:
   found=np.where(mask[py]>threshold)[0]
   if not len(found):
    rows=np.where(np.max(mask,axis=1)>threshold)[0];py=int(rows[np.argmin(abs(rows-py))]);found=np.where(mask[py]>threshold)[0]
   px=int(found[np.argmin(abs(found-px))])
  uv.data[lp.index].uv=((px+offset+.5)/773,1-(py+.5)/396)
# The crown should form a rounded silhouette rather than a pointed tip.
for v in d.vertices:
 if v.co.z>1.437:v.co.z=1.437+(v.co.z-1.437)*.30
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R17 likeness work in progress: fitted mesh and original photo projections; hair UVs constrained to hair class. Not approved, not rigged.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r17.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R17_SAVED')

