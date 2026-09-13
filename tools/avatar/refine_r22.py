from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r22-hair-mask';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r21-profile-fit/aria-head-r21.blend'))
hair=bpy.data.objects['ARIA R20 - continuous hair'];hair.name='ARIA R22 - hair';m=hair.data.materials[0];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
a=np.zeros((396,773,4),dtype=np.float32);a[:,:,3]=1
for name,offset in [('front',0),('profile',516)]:
 mask=np.load('D:/UserData/ARIA/tools/avatar-fit-data/'+name+'-segmentation.npy')[1,:,:,0];a[:,offset:offset+mask.shape[1],:3]=np.clip((mask-.55)/.25,0,1)[:,:,None]
im=bpy.data.images.new('Hair validity at texture pixels',width=773,height=396,alpha=True);im.pixels.foreach_set(a[::-1].ravel());im.pack()
tex=[]
for uv in ['Side','Front']:
 t=n.new('ShaderNodeTexImage');t.image=im;u=n.new('ShaderNodeUVMap');u.uv_map=uv;l.new(u.outputs[0],t.inputs[0]);tex.append(t)
attr=n.new('ShaderNodeVertexColor');attr.layer_name='ProjectionMix';mix=n.new('ShaderNodeMixRGB');l.new(attr.outputs['Color'],mix.inputs[0]);l.new(tex[0].outputs['Color'],mix.inputs[1]);l.new(tex[1].outputs['Color'],mix.inputs[2]);old=p.inputs['Alpha'].links[0].from_socket;mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(old,mul.inputs[0]);l.new(mix.outputs[0],mul.inputs[1]);l.new(mul.outputs[0],p.inputs['Alpha'])
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R22 per-pixel hair classification removes projected skin from hair mesh. Likeness and animation incomplete.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r22.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R22_SAVED')
