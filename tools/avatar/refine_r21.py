from pathlib import Path
import bpy,numpy as np,math
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r21-profile-fit';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r20-continuous-hair/aria-head-r20.blend'))
h=bpy.data.objects['ARIA R18 - face'];dg=bpy.context.evaluated_depsgraph_get();evaluated=h.evaluated_get(dg);coords=[v.co.copy() for v in evaluated.to_mesh().vertices]
h.shape_key_clear()
for v,co in zip(h.data.vertices,coords):v.co=co
h.name='ARIA R21 - reference profile head';h.shape_key_add(name='Basis');k=h.shape_key_add(name='Profile silhouette adjustment')
ys=np.array([145,155,165,175,185,195,205,215,225,235,245,260]);ds=np.array([0,-.0027,-.0029,-.0017,-.0006,.0054,.0030,.0025,.0026,-.0068,-.0076,0])
for v in k.data:
 x,y,z=v.co;py=150+(1.336-z)*1200;v.co.y+=np.interp(py,ys,ds)*math.exp(-(x/.025)**2)*max(0,min(1,(-y-.04)/.04))
k.value=1
vg=h.vertex_groups.new(name='Side surface smoothing')
for v in h.data.vertices:
 w=max(0,min(1,(abs(v.co.x)-.037)/.02))*max(0,min(1,(v.co.z-1.23)/.03))
 if w:vg.add([v.index],w,'REPLACE')
mod=h.modifiers.new('Gentle side surface smoothing','SMOOTH');mod.factor=.5;mod.iterations=5;mod.vertex_group=vg.name
mask=h.data.color_attributes['PhotoProjectionWeight']
for v in h.data.vertices:
 if v.co.z>1.30:
  fade=max(0,min(1,(.054-abs(v.co.x))/.013));c=mask.data[v.index].color[:];mask.data[v.index].color=(c[0]*fade,c[1]*fade,c[2]*fade,1)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R21 photo-guided profile study; incomplete likeness, no validated facial animation.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r21.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R21_SAVED')
