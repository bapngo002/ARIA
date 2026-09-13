"""Unify photographic hair projections onto one continuous 3D hull."""
from pathlib import Path
import bpy,math,json
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r12-unified-hair';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r11-hair-fit/aria-head-r11.blend'))
h=bpy.data.objects['ARIA R11 - fitted head'];h.name='ARIA R12 - face'
for o in list(bpy.data.objects):
 if 'curved hair' in o.name or 'fitted collar' in o.name:bpy.data.objects.remove(o,do_unlink=True)
profile=json.loads((root/'assets/characters/aria-custom/r10-multiview/profile-fit.json').read_text())
zs=1.336+(150-np.array(profile['front_rows']))/1200;sh=np.array(profile['depth_shifts_m'])
xz=np.r_[1.21,zs[::-1],1.425];ys=np.r_[0,sh[::-1],0]
key=h.data.shape_keys.key_blocks['Side profile refinement'];basis=h.data.shape_keys.key_blocks[0]
for v,b in zip(key.data,basis.data):
 x,y,z=b.co;s=np.interp(z,xz,ys)*math.exp(-(x/.030)**2)*max(0,min(1,(-y-.065)/.04));v.co=b.co;v.co.y+=s
key.value=1
# Replace the synthetic iris appearance with the reference color on actual eye spheres.
image=bpy.data.images.get('ARIA supplied front - three-quarter - profile')
def setup_eye(o):
 d=o.data;uv=d.uv_layers.new(name='ReferenceEye')
 for lp in d.loops:
  co=o.matrix_world@d.vertices[lp.vertex_index].co;uv.data[lp.index].uv=((135+co.x*1200)/773,1-(150+(1.336-co.z)*1200)/396)
 m=bpy.data.materials.new(o.name+' reference eye');m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.32;p.inputs['Specular IOR Level'].default_value=.12
 t=n.new('ShaderNodeTexImage');t.image=image;u=n.new('ShaderNodeUVMap');u.uv_map=uv.name;l.new(u.outputs[0],t.inputs[0]);l.new(t.outputs['Color'],p.inputs['Base Color']);l.new(t.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.3;d.materials.clear();d.materials.append(m)
for o in list(bpy.data.objects):
 if 'iris and pupil' in o.name:bpy.data.objects.remove(o,do_unlink=True)
 elif 'sclera' in o.name:setup_eye(o)

# Extend the reference projection to the neck and front of the indigo garment.
skin=h.data.materials[0];nodes=skin.node_tree.nodes;links=skin.node_tree.links
mask=h.data.color_attributes['PhotoProjectionWeight'];fallback=h.data.color_attributes.new(name='FallbackColor',type='FLOAT_COLOR',domain='POINT')
for i,v in enumerate(basis.data):
 x,y,z=v.co;front=max(0,min(1,(-y+.012)/.060));side=max(0,min(1,(.104-abs(x))/.014));top=max(0,min(1,(1.413-z)/.018));a=front*side*top
 mask.data[i].color=(a,a,a,1);f=max(0,min(1,(z-1.235)/.008));color=np.array([.018,.019,.05])*(1-f)+np.array([.57,.37,.30])*f;fallback.data[i].color=(*color,1)
attr=nodes.new('ShaderNodeVertexColor');attr.layer_name=fallback.name
mix=next(n for n in nodes if n.type=='MIX_RGB');links.new(attr.outputs['Color'],mix.inputs[1])

front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0];side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
shape=[]
for py in range(396):
 fs=np.where(front[py]>.55)[0];ss=np.where(side[py]>.55)[0]
 rx=max(abs(fs.min()-135),abs(fs.max()-135))/1200 if len(fs) else .005
 if len(ss): yy=(600-(ss+516))/1200;yc=(yy.max()+yy.min())/2;ry=(yy.max()-yy.min())/2
 else:yc=0;ry=.005
 shape.append((rx,yc,ry))
shape=np.array(shape)
for col in range(3):shape[:,col]=np.convolve(np.pad(shape[:,col],(8,8),mode='edge'),np.ones(17)/17,mode='valid')
bpy.context.view_layer.update();bvh=BVHTree.FromObject(h,bpy.context.evaluated_depsgraph_get())
verts=[];faces=[];uvfront=[];uvside=[];weights=[];alpha=[];N=192;M=192
for j in range(N):
 py=18+370*j/(N-1);z=1.336+(150-py)/1200;rx,yc,ry=shape[int(py)]
 for i in range(M):
  a=math.tau*i/M;x=rx*math.cos(a);y=yc+ry*math.sin(a)
  center=Vector((0,yc,z));direction=Vector((x,y-yc,0)).normalized();hit,_,_,_=bvh.ray_cast(center,direction)
  co=Vector((x,y,z))
  if hit and (hit-center).length>(co-center).length-.002:co=hit+direction*.003
  x,y,z=co;pxF=135+x*1200;pxS=600-y*1200
  wf=max(0,-math.sin(a))**4;ws=abs(math.cos(a))**4;w=wf/(wf+ws+1e-9)
  af=front[max(0,min(395,int(py))),max(0,min(257,int(pxF)))];aside=side[max(0,min(395,int(py))),max(0,min(256,int(pxS-516)))]
  confidence=w*af+(1-w)*aside
  verts.append(tuple(co));uvfront.append((pxF/773,1-py/396));uvside.append((pxS/773,1-py/396));weights.append(w);alpha.append(max(0,min(1,(float(confidence)-.25)/.50)))
for j in range(N-1):
 for i in range(M):
  ids=(j*M+i,j*M+(i+1)%M,(j+1)*M+(i+1)%M,(j+1)*M+i)
  if sum(alpha[k] for k in ids)>1.2:faces.append(ids)
d=bpy.data.meshes.new('Unified hair hull');d.from_pydata(verts,[],faces);d.update();hair=bpy.data.objects.new('ARIA R12 - continuous textured hair volume',d);bpy.context.scene.collection.objects.link(hair)
uf=d.uv_layers.new(name='Front');us=d.uv_layers.new(name='Side');col=d.color_attributes.new(name='ProjectionMix',type='FLOAT_COLOR',domain='POINT')
for lp in d.loops:uf.data[lp.index].uv=uvfront[lp.vertex_index];us.data[lp.index].uv=uvside[lp.vertex_index]
for i in range(len(verts)):col.data[i].color=(weights[i],weights[i],weights[i],alpha[i])
for p in d.polygons:p.use_smooth=True
mat=bpy.data.materials.new('Blended photographic hair');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.72;p.inputs['Specular IOR Level'].default_value=.04
textures=[]
for name in ['Side','Front']:
 t=n.new('ShaderNodeTexImage');t.image=image;u=n.new('ShaderNodeUVMap');u.uv_map=name;l.new(u.outputs[0],t.inputs[0]);textures.append(t)
attr=n.new('ShaderNodeVertexColor');attr.layer_name='ProjectionMix';mix=n.new('ShaderNodeMixRGB');l.new(attr.outputs['Color'],mix.inputs[0]);l.new(textures[0].outputs['Color'],mix.inputs[1]);l.new(textures[1].outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color']);l.new(mix.outputs[0],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.6;l.new(attr.outputs['Alpha'],p.inputs['Alpha']);d.materials.append(mat)
scene=bpy.context.scene;scene['status']='R12 unified 3D hair hull and photo-projection study, awaiting multiview comparison.';scene.cycles.samples=40
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r12.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R12_SAVED')
