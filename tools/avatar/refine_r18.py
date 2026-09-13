from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r18-side-cleanup';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r17-clean-hair/aria-head-r17.blend'))
h=bpy.data.objects['ARIA R16 - face'];h.name='ARIA R18 - face';m=h.data.materials[0];n=m.node_tree.nodes;l=m.node_tree.links
arr=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[:,:,:,0]
a=np.zeros((396,773,4),dtype=np.float32);valid=np.clip((arr[2]+arr[3]+arr[4]-.4)/.4,0,1);a[:,:258,:3]=valid[:,:,None];a[:,:,3]=1
im=bpy.data.images.new('Reference skin validity',width=773,height=396,alpha=True);im.pixels.foreach_set(a[::-1].ravel());im.pack()
t=n.new('ShaderNodeTexImage');t.image=im;u=n.new('ShaderNodeUVMap');u.uv_map='ReferenceFrontProjection';l.new(u.outputs[0],t.inputs[0])
mix=next(x for x in n if x.type=='MIX_RGB' and x.inputs[1].links and getattr(x.inputs[1].links[0].from_node,'layer_name','')=='FallbackColor')
old=mix.inputs[0].links[0].from_socket;mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(old,mul.inputs[0]);l.new(t.outputs['Color'],mul.inputs[1]);l.new(mul.outputs[0],mix.inputs[0])
# Restrict the front projection on highly oblique temple surfaces.
mask=h.data.color_attributes['PhotoProjectionWeight']
for v in h.data.vertices:
 x,y,z=v.co
 if z>1.30:
  fade=max(0,min(1,(.068-abs(x))/.018));c=mask.data[v.index].color[:];mask.data[v.index].color=(c[0]*fade,c[1]*fade,c[2]*fade,1)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R18 side cleanup appearance study; actual meshes, photographic material, incomplete likeness and animation.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r18.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R18_SAVED')
