"""Remove projected hair from skin and fill unsupported scalp gaps in the hair hull."""
from pathlib import Path
import bpy,math
import numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r16-review';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r15-appearance/aria-head-r15.blend'))
h=bpy.data.objects['ARIA R15 - reference face'];h.name='ARIA R16 - face'
front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[:,:,:,0];side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[:,:,:,0]
def sample(mask,x,y):return float(mask[max(0,min(395,int(y))),max(0,min(mask.shape[1]-1,int(x)))])
skinuv=np.zeros((len(h.data.vertices),2))
for lp in h.data.loops:skinuv[lp.vertex_index]=h.data.uv_layers['ReferenceFrontProjection'].data[lp.index].uv
mask=h.data.color_attributes['PhotoProjectionWeight']
for i,uv in enumerate(skinuv):
 confidence=sample(front[2]+front[3]+front[4],uv[0]*773,(1-uv[1])*396)
 a=mask.data[i].color[0]*max(0,min(1,(confidence-.12)/.65));mask.data[i].color=(a,a,a,1)
hair=bpy.data.objects['ARIA R15 - 3D hair shell'];hair.name='ARIA R16 - hair volume';d=hair.data
uf=np.zeros((len(d.vertices),2));us=uf.copy()
for lp in d.loops:uf[lp.vertex_index]=d.uv_layers['Front'].data[lp.index].uv;us[lp.vertex_index]=d.uv_layers['Side'].data[lp.index].uv
extra=d.color_attributes.new(name='ScalpCoverage',type='FLOAT_COLOR',domain='POINT')
for i,v in enumerate(d.vertices):
 x,y,z=v.co;af=sample(front[1],uf[i,0]*773,(1-uf[i,1])*396);ass=sample(side[1],us[i,0]*773-516,(1-us[i,1])*396)
 old=d.color_attributes['ProjectionMix'].data[i].color;coverage=old[3]
 fill=max(0,min(1,(z-1.365)/.015))
 if y>-.015 and z>1.26:fill=1
 if abs(x)>.075 and z<1.35:fill=max(fill,max(0,min(1,(max(af,ass)-.1)/.5)))
 coverage=max(coverage,fill)
 extra.data[i].color=(max(0,min(1,(max(af,ass)-.2)/.5)),coverage,0,1)
m=d.materials[0];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');existing=p.inputs['Base Color'].links[0].from_socket
attr=n.new('ShaderNodeVertexColor');attr.layer_name='ScalpCoverage';sep=n.new('ShaderNodeSeparateColor');l.new(attr.outputs['Color'],sep.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.028,.019,.016,1);l.new(sep.outputs['Red'],mix.inputs[0]);l.new(existing,mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color']);l.new(mix.outputs[0],p.inputs['Emission Color']);l.new(sep.outputs['Green'],p.inputs['Alpha'])
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R16 reference appearance study with class-masked photo textures. Head/eyes/hair are true 3D meshes. Not animation-ready or approved.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r16.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('near-profile',(-1.2,-.22,0)),('true-profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R16_SAVED')
