"""Landmark-guided R7 fit and photo-projected material study.
2D landmarks constrain silhouette/features, not a calibrated 3D scan.
"""
from pathlib import Path
import bpy,importlib,math,json
import numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2]
out=root/'assets/characters/aria-custom/r8-reference-fit';out.mkdir(parents=True,exist_ok=True)
data=Path('D:/UserData/ARIA/tools/avatar-fit-data')
refinfo=json.loads((data/'reference.json').read_text());srcinfo=json.loads((data/'source.json').read_text())
ref=np.array(refinfo['points']);src=np.array(srcinfo['points'])
# Scale is an authored convention, not a physical measurement of the character.
scale=1200.;cx=135.;cy=150.;eye_z=1.336
src2=np.c_[(src[:,0]-320)*.31/800,1.326+(400-src[:,1])*.31/800]
dst2=np.c_[(ref[:,0]-cx)/scale,eye_z+(cy-ref[:,1])/scale]
eyeids=[33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246,263,249,390,373,374,380,381,382,362,398,384,385,386,387,388,466]
lipids=[61,146,91,181,84,17,314,405,321,375,291,308,324,318,402,317,14,87,178,88,95,78,191,80,81,82,13,312,311,310,415,409,270,269,267,0,37,39,40,185]
oval=[10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109]
nose=[1,2,4,5,6,19,94,97,98,168,195,197,326,327]
brow=[70,63,105,66,107,55,65,52,53,46,300,293,334,296,336,285,295,282,283,276]
ids=sorted(set(eyeids+lipids+oval+nose+brow))
ctrl=src2[ids];delta=dst2[ids]-ctrl
anchors=np.array([[-.10,1.20],[0,1.19],[.10,1.20],[-.10,1.43],[0,1.455],[.10,1.43]])
ctrl=np.r_[ctrl,anchors];delta=np.r_[delta,np.zeros_like(anchors)]
origin=np.array([0,1.33]);c=(ctrl-origin)/.1
def kernel(d):
 r=np.sqrt((d*d).sum(axis=-1));return r*r*np.log(r+1e-12)
K=kernel(c[:,None]-c[None,:]);P=np.c_[np.ones(len(c)),c]
A=np.block([[K+np.eye(len(c))*2e-5,P],[P.T,np.zeros((3,3))]])
coef=np.linalg.solve(A,np.r_[delta,np.zeros((3,2))])
def displacement(points):
 q=(points-origin)/.1
 return kernel(q[:,None]-c[None,:])@coef[:-3]+np.c_[np.ones(len(q)),q]@coef[-3:]

bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r7-head-study/aria-head-r7.blend'))
h=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('ARIA R7'))
TS=importlib.import_module('bl_ext.aria_local.mpfb.services.targetservice').TargetService
HS=importlib.import_module('bl_ext.aria_local.mpfb.services.humanservice').HumanService
TS.bake_targets(h);h.name='ARIA R8 - reference-fitted face'
def deform(coords):
 a=np.array(coords,dtype=float);d=displacement(a[:,[0,2]])
 front=np.clip((-a[:,1]-.020)/.06,0,1);height=np.clip((a[:,2]-1.215)/.025,0,1)*np.clip((1.455-a[:,2])/.03,0,1)
 d*= (front*height)[:,None];a[:,0]+=d[:,0];a[:,2]+=d[:,1]
 return a
old=np.array([list(v.co) for v in h.data.vertices]);new=deform(old)
h.shape_key_add(name='Basis - R7');fit=h.shape_key_add(name='Reference landmark fit - 2D constraints')
for v,co in zip(fit.data,new):v.co=co
fit.value=1
# Photo UVs are attached to the fitted geometry, so they deform with future sculpting.
uv=h.data.uv_layers.new(name='ReferenceFrontProjection')
for loop in h.data.loops:
 x,y,z=new[loop.vertex_index];uv.data[loop.index].uv=((cx+x*scale)/773,1-(cy+(eye_z-z)*scale)/396)
image=bpy.data.images.load(str(root/'assets/characters/aria-custom/r6-candidate/reference-three-views.png'),check_existing=True);image.pack()
mat=bpy.data.materials.new('Reference photo skin projection - study');mat.use_nodes=True
nodes=mat.node_tree.nodes;links=mat.node_tree.links;p=nodes.get('Principled BSDF')
p.inputs['Roughness'].default_value=.68;p.inputs['Specular IOR Level'].default_value=.18
tex=nodes.new('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND';uvn=nodes.new('ShaderNodeUVMap');uvn.uv_map=uv.name;links.new(uvn.outputs['UV'],tex.inputs['Vector'])
mask=h.data.color_attributes.new(name='PhotoProjectionWeight',type='FLOAT_COLOR',domain='POINT')
for i,(x,y,z) in enumerate(new):
 front=max(0,min(1,(-y-.018)/.050));side=max(0,min(1,(.075-abs(x))/.020))
 top=max(0,min(1,(1.413-z)/.018));bottom=max(0,min(1,(z-1.238)/.012))
 f=front*side*top*bottom;mask.data[i].color=(f,f,f,1)
attr=nodes.new('ShaderNodeVertexColor');attr.layer_name=mask.name
mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[1].default_value=(.57,.37,.30,1)
links.new(attr.outputs['Color'],mix.inputs[0]);links.new(tex.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],p.inputs['Base Color'])
# Mostly unlit reference color plus subtle real shading: the reference contains lighting already.
links.new(mix.outputs[0],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.20
h.data.materials.clear();h.data.materials.append(mat)
for poly in h.data.polygons:poly.material_index=0
for o in list(bpy.data.objects):
 if o.type=='CURVE':bpy.data.objects.remove(o,do_unlink=True)
 elif o.type=='MESH' and o!=h:
  center=np.array(list(o.location));dd=displacement(center[[0,2]][None,:])[0];o.location.x+=dd[0];o.location.z+=dd[1]

# Fit stock CC0 hair using its authored correspondence to an untouched full MPFB base.
with bpy.data.libraries.load(str(root/'assets/characters/aria-custom/aria-head-r4.blend'),link=False) as (frm,to):
 to.objects=[n for n in frm.objects if n.startswith('ARIA head R4')]
temp=to.objects[0];bpy.context.scene.collection.objects.link(temp)
hair=HS.add_mhclo_asset('D:/UserData/ARIA/tools/avatar-assets/hair/long01/long01.mhclo',temp,asset_type='Hair',subdiv_levels=1,set_up_rigging=False)
hair.parent=None;hair.name='ARIA R8 - long hair foundation'
bpy.data.objects.remove(temp,do_unlink=True)
# Bend the lower locks into soft waves, keeping their natural alpha-card edges.
for v in hair.data.vertices:
 x,y,z=v.co;t=max(0,min(1,(1.36-z)/.19));sign=1 if x>=0 else -1
 v.co.x+=sign*.007*math.sin(t*math.pi*3+y*18)*t
 v.co.y+=.006*math.sin(t*math.pi*3+x*20)*t
 if z<1.17:v.co.z=1.17+(z-1.17)*.45
for m in hair.data.materials:
 if not m or not m.use_nodes:continue
 for n in m.node_tree.nodes:
  if n.type=='BSDF_PRINCIPLED':n.inputs['Roughness'].default_value=.62

scene=bpy.context.scene;scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=-.4
scene.cycles.samples=32;scene['status']='R8 image-guided fit and projected skin study; depth and exact likeness still under review.'
target=Vector((0,-.075,1.324));cam=scene.camera;cam.data.ortho_scale=.32
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.view_layer.objects.active=h
bpy.ops.object.select_all(action='DESELECT');h.select_set(True);bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r8.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
(out/'fit-report.json').write_text(json.dumps({'method':'Regularized thin-plate 2D landmark fit, frontal reference texture projection, stock CC0 long01 hair foundation','landmarks':len(ids),'rms_control_fit_mm':float(np.sqrt(np.mean((displacement(src2[ids])-(dst2[ids]-src2[ids]))**2))*1000),'scale_pixels_per_metre':scale,'not_verified':['3D depth','profile likeness','animation','Pi performance'],'reference_image_used_as_texture':True},indent=2),encoding='utf-8')
print('R8_SAVED')
