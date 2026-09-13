"""Use segmented hair silhouettes to build curved, textured front/side surfaces."""
from pathlib import Path
import bpy,math,json
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r11-hair-fit';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r10-multiview/aria-head-r10.blend'))
h=bpy.data.objects['ARIA R10 - fitted face'];h.name='ARIA R11 - fitted head'
for o in list(bpy.data.objects):
 if o.type=='MESH' and ('hair shell' in o.name or 'rear hair volume' in o.name):bpy.data.objects.remove(o,do_unlink=True)
front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0]
side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
image=bpy.data.images.get('ARIA supplied front - three-quarter - profile')
shape=[]
for py in range(396):
 fs=np.where(front[py]>.55)[0];ss=np.where(side[py]>.55)[0]
 if len(fs)>0:rx=max(abs(fs.min()-135),abs(fs.max()-135))/1200
 else:rx=.01
 if len(ss)>0:ys=(600-(ss+516))/1200;yc=(ys.max()+ys.min())/2;ry=(ys.max()-ys.min())/2
 else:yc=0;ry=.01
 shape.append((max(.005,rx),float(yc),max(.005,float(ry))))
shape=np.array(shape)
# Smooth silhouette parameters between image scanlines.
for col in range(3):shape[:,col]=np.convolve(np.pad(shape[:,col],(4,4),mode='edge'),np.ones(9)/9,mode='valid')
bpy.context.view_layer.update();bvh=BVHTree.FromObject(h,bpy.context.evaluated_depsgraph_get())
mat=bpy.data.materials.new('Segmented reference hair');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF')
tex=n.new('ShaderNodeTexImage');tex.image=image;uvn=n.new('ShaderNodeUVMap');uvn.uv_map='HairPhoto';l.new(uvn.outputs[0],tex.inputs[0]);l.new(tex.outputs['Color'],p.inputs['Base Color']);l.new(tex.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.60;p.inputs['Roughness'].default_value=.7;p.inputs['Specular IOR Level'].default_value=.05
attr=n.new('ShaderNodeVertexColor');attr.layer_name='Segmentation';l.new(attr.outputs['Alpha'],p.inputs['Alpha'])
for view,mask,sgn in [('front',front,0),('left',side,-1),('right',side,1)]:
 verts=[];uvs=[];alphas=[];faces=[];step=2;W=(mask.shape[1]-1)//step+1;H=(mask.shape[0]-1)//step+1
 for j in range(H):
  py=j*step;z=1.336+(150-py)/1200;rx,yc,ry=shape[py]
  for i in range(W):
   px=i*step
   if view=='front':
    x=(px-135)/1200;y=yc-ry*math.sqrt(max(.002,1-(x/rx)**2))
    hit,_,_,_=bvh.ray_cast(Vector((x,-.4,z)),Vector((0,1,0)))
    if hit and mask[py,px]>.5:y=min(y,hit.y-.003)
    u=px/773
   else:
    y=(600-(px+516))/1200;x=sgn*rx*math.sqrt(max(.002,1-((y-yc)/ry)**2))
    hit,_,_,_=bvh.ray_cast(Vector((sgn*.4,y,z)),Vector((-sgn,0,0)))
    if hit and mask[py,px]>.5:x=sgn*max(abs(x),abs(hit.x)+.003)
    # Keep side surface from occluding frontal surface at their join.
    x*=.992;u=(px+516)/773
   verts.append((x,y,z));uvs.append((u,1-py/396));alphas.append(float(max(0,min(1,(mask[py,px]-.25)/.5))))
 for j in range(H-1):
  for i in range(W-1):
   a=j*W+i;ids=(a,a+1,a+W+1,a+W)
   if sum(alphas[k] for k in ids)>1.4:faces.append(ids)
 d=bpy.data.meshes.new(view+' hair surface');d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new('ARIA R11 - curved hair '+view,d);bpy.context.scene.collection.objects.link(o);d.materials.append(mat)
 uv=d.uv_layers.new(name='HairPhoto');color=d.color_attributes.new(name='Segmentation',type='FLOAT_COLOR',domain='POINT')
 for loop in d.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
 for idx,val in enumerate(alphas):color.data[idx].color=(1,1,1,val)
 for p in d.polygons:p.use_smooth=True
 # The mask controls the mesh edge; unused grid points do not contribute geometry.

scene=bpy.context.scene;scene.cycles.samples=40;scene.cycles.transparent_max_bounces=24
scene['status']='R11 segmented front/side hair surfaces; photo texture projection; under visual review.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r11.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R11_SAVED')
