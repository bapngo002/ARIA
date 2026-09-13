"""Correct reference-texture visibility after the silhouette edits."""
from pathlib import Path
import bpy,math
import numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r15-appearance';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r14-likeness/aria-head-r14.blend'))
h=bpy.data.objects['ARIA R14 - face'];h.name='ARIA R15 - reference face'
m=h.data.materials[0];nodes=m.node_tree.nodes;links=m.node_tree.links
fronttex=next(n for n in nodes if n.type=='TEX_IMAGE' and n.inputs['Vector'].links and getattr(n.inputs['Vector'].links[0].from_node,'uv_map','')=='ReferenceFrontProjection')
mix=next(n for n in nodes if n.type=='MIX_RGB' and n.inputs[1].links and getattr(n.inputs[1].links[0].from_node,'layer_name','')=='FallbackColor')
# Profile images carry occlusion and cannot be projected across the eye region.
links.new(fronttex.outputs['Color'],mix.inputs[2])
hair=bpy.data.objects['ARIA R14 - reference hair volume'];hair.name='ARIA R15 - 3D hair shell';d=hair.data
front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0];side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
def sample(mask,x,y):return float(mask[max(0,min(395,int(y))),max(0,min(mask.shape[1]-1,int(x)))])
uf=np.zeros((len(d.vertices),2));us=uf.copy()
for lp in d.loops:uf[lp.vertex_index]=d.uv_layers['Front'].data[lp.index].uv;us[lp.vertex_index]=d.uv_layers['Side'].data[lp.index].uv
attrs=d.color_attributes['ProjectionMix']
for i,v in enumerate(d.vertices):
 af=sample(front,uf[i,0]*773,(1-uf[i,1])*396);ass=sample(side,us[i,0]*773-516,(1-us[i,1])*396)
 a=math.tau*(i%192)/192;wf=max(0,-math.sin(a))**4;ws=abs(math.cos(a))**4
 weight=wf*af/(wf*af+ws*ass+1e-8)
 confidence=min(af,ass) if math.sin(a)<.05 else ass
 alpha=max(0,min(1,(confidence-.28)/.50));attrs.data[i].color=(weight,weight,weight,alpha)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R15 corrected appearance candidate. Photo-projected 3D surfaces; source-like frontal appearance, unverified animation and exact likeness.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r15.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R15_SAVED')
