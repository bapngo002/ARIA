from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r23-skin-blend';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r22-hair-mask/aria-head-r22.blend'))
h=bpy.data.objects['ARIA R21 - reference profile head'];h.name='ARIA R23 - face';m=h.data.materials[0];n=m.node_tree.nodes;l=m.node_tree.links
source=bpy.data.images['ARIA supplied front - three-quarter - profile'];a=np.array(source.pixels[:],dtype=np.float32).reshape(396,773,4)[::-1].copy();seg=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[:,:,:,0]
# Extend clean skin/garment edge colors into the unused projection area.
for py in range(396):
 valid=np.where((seg[2,py]+seg[3,py]+seg[4,py])>.75)[0]
 if len(valid)>5:
  lo,hi=int(valid.min()),int(valid.max());left=a[py,lo:min(lo+6,hi),:3].mean(0);right=a[py,max(lo,hi-5):hi+1,:3].mean(0)
  a[py,:lo,:3]=left;a[py,hi+1:258,:3]=right
 else:a[py,:258,:3]=(.67,.49,.44)
im=bpy.data.images.new('Expanded clean face projection',width=773,height=396,alpha=True);im.pixels.foreach_set(a[::-1].ravel());im.pack()
tex=next(x for x in n if x.type=='TEX_IMAGE' and x.inputs['Vector'].links and getattr(x.inputs['Vector'].links[0].from_node,'uv_map','')=='ReferenceFrontProjection' and x.image==source);tex.image=im
mix=next(x for x in n if x.type=='MIX_RGB' and x.inputs[1].links and getattr(x.inputs[1].links[0].from_node,'layer_name','')=='FallbackColor')
attr=next(x for x in n if x.type=='VERTEX_COLOR' and x.layer_name=='PhotoProjectionWeight');l.new(attr.outputs['Color'],mix.inputs[0])
mask=h.data.color_attributes['PhotoProjectionWeight'];fallback=h.data.color_attributes['FallbackColor']
for v in h.data.vertices:
 x,y,z=v.co;f=max(0,min(1,(-y+.025)/.09));side=max(0,min(1,(.095-abs(x))/.04));top=max(0,min(1,(1.42-z)/.035));w=f*side*top;mask.data[v.index].color=(w,w,w,1)
 if z>1.246:fallback.data[v.index].color=(.32,.205,.18,1)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R23 expanded skin-edge projection and continuous head study. Exact likeness/animation not approved.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r23.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R23_SAVED')

