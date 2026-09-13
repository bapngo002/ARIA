"""Correct masked texture blending and close/smooth the hair crown."""
from pathlib import Path
import bpy,math,json
import numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r13-appearance';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r12-unified-hair/aria-head-r12.blend'))
h=bpy.data.objects['ARIA R12 - face'];h.name='ARIA R13 - reference face'
front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[:,:,:,0];side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[:,:,:,0]
image=bpy.data.images.get('ARIA supplied front - three-quarter - profile')
def sample(arr,x,y):return float(arr[max(0,min(395,int(y))),max(0,min(arr.shape[1]-1,int(x)))])
hair=bpy.data.objects['ARIA R12 - continuous textured hair volume'];hair.name='ARIA R13 - textured hair volume';d=hair.data;mixdata=d.color_attributes['ProjectionMix'];N=192;M=192
for j in range(N):
 py=18+370*j/(N-1)
 for i in range(M):
  idx=j*M+i;v=d.vertices[idx];x,y,z=v.co;a=math.tau*i/M
  wf=max(0,-math.sin(a))**4;ws=abs(math.cos(a))**4
  af=sample(front[1],135+x*1200,py);ass=sample(side[1],600-y*1200-516,py)
  # A source contributes color only where that source actually contains hair.
  w=wf*af/(wf*af+ws*ass+1e-9)
  alpha=max(0,min(1,((wf*af+ws*ass)/(wf+ws+1e-9)-.30)/.45))
  mixdata.data[idx].color=(w,w,w,alpha)
  if j<6:
   f=.12+.88*j/6;v.co.x*=f;v.co.y=(v.co.y+.020)*f-.020;v.co.z+=.004*(1-j/6)
# Add a gentle mesh smoothing pass to remove the contour-sampling steps.
sm=hair.modifiers.new('Soft hair silhouette','SMOOTH');sm.factor=.65;sm.iterations=4

# Use the profile source for side-facing skin, with class-aware blending.
material=h.data.materials[0];nodes=material.node_tree.nodes;links=material.node_tree.links
profileuv=h.data.uv_layers.new(name='ProfileSkin')
for lp in h.data.loops:
 co=h.data.shape_keys.key_blocks['Side profile refinement'].data[lp.vertex_index].co
 profileuv.data[lp.index].uv=((600-co.y*1200)/773,1-(150+(1.336-co.z)*1200)/396)
blend=h.data.color_attributes.new(name='SkinViewBlend',type='FLOAT_COLOR',domain='POINT')
for i,v in enumerate(h.data.vertices):
 x,y,z=h.data.shape_keys.key_blocks['Side profile refinement'].data[i].co;py=150+(1.336-z)*1200
 # Frontal importance falls toward the ears; original mouth/nose color stays frontal.
 w=max(0,min(1,(.063-abs(x))/.030))
 fs=sample(front[2]+front[3]+front[4],135+x*1200,py);ss=sample(side[2]+side[3]+side[4],600-y*1200-516,py)
 w=w*fs/(w*fs+(1-w)*ss+1e-8)
 blend.data[i].color=(w,w,w,1)
fronttex=next(n for n in nodes if n.type=='TEX_IMAGE')
sidetex=nodes.new('ShaderNodeTexImage');sidetex.image=image;uvnode=nodes.new('ShaderNodeUVMap');uvnode.uv_map=profileuv.name;links.new(uvnode.outputs[0],sidetex.inputs[0])
attr=nodes.new('ShaderNodeVertexColor');attr.layer_name=blend.name
viewmix=nodes.new('ShaderNodeMixRGB');links.new(attr.outputs['Color'],viewmix.inputs[0]);links.new(sidetex.outputs['Color'],viewmix.inputs[1]);links.new(fronttex.outputs['Color'],viewmix.inputs[2])
fallbackmix=next(n for n in nodes if n.type=='MIX_RGB' and n!=viewmix);links.new(viewmix.outputs[0],fallbackmix.inputs[2])
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R13 image-guided appearance candidate. True 3D head and hair hull with projected photo colors; animation not verified.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r13.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R13_SAVED')
