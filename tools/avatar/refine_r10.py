"""Three-dimensional hair shell with reference-projected color and side-profile fit.
Photo color remains view-dependent evidence, not a scan or clean PBR albedo.
"""
from pathlib import Path
import bpy,math,json
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r10-multiview';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r9-refinement/aria-head-r9.blend'))
h=bpy.data.objects['ARIA R9 - reference face'];h.name='ARIA R10 - fitted face'
for o in list(bpy.data.objects):
 if 'hair foundation' in o.name or 'front strands' in o.name:bpy.data.objects.remove(o,do_unlink=True)
# Bake the earlier facial fit, then preserve the new profile pass as an editable key.
import importlib
TS=importlib.import_module('bl_ext.aria_local.mpfb.services.targetservice').TargetService;TS.bake_targets(h)
bpy.context.view_layer.update();bvh=BVHTree.FromObject(h,bpy.context.evaluated_depsgraph_get())
front_rows=np.array([100,130,148,168,184,193,207,215,232,247])
profile_x=np.array([707,719,724,731,742,729,733,730,722,707])
zs=1.336+(150-front_rows)/1200;desired=-(profile_x-600)/1200
shifts=[]
for z,want in zip(zs,desired):
 hit,_,_,_=bvh.ray_cast(Vector((0,-.4,float(z))),Vector((0,1,0)))
 shifts.append(float(want-hit.y) if hit else 0)
shifts=np.clip(shifts,-.010,.020)
def depth_shift(x,y,z):
 s=np.interp(z,zs[::-1],np.array(shifts)[::-1],left=0,right=0)
 return s*math.exp(-(x/.030)**2)*max(0,min(1,(-y-.065)/.04))
h.shape_key_add(name='Basis - frontal fit');key=h.shape_key_add(name='Side profile refinement')
for v,k in zip(h.data.vertices,key.data):k.co.y+=depth_shift(*v.co)
key.value=1
for o in bpy.data.objects:
 if o.type=='MESH' and o!=h:o.location.y+=depth_shift(*o.location)
bpy.context.view_layer.update();bvh=BVHTree.FromObject(h,bpy.context.evaluated_depsgraph_get())
image=bpy.data.images.get('ARIA supplied front - three-quarter - profile')
if not image:image=bpy.data.images.load(str(root/'assets/characters/aria-custom/r6-candidate/reference-three-views.png'),check_existing=True)

def photomat(name,uvname='Photo',strength=.65):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
 p.inputs['Roughness'].default_value=.65;p.inputs['Specular IOR Level'].default_value=.07
 tex=n.new('ShaderNodeTexImage');tex.image=image;uv=n.new('ShaderNodeUVMap');uv.uv_map=uvname;l.new(uv.outputs[0],tex.inputs[0])
 l.new(tex.outputs['Color'],p.inputs['Base Color']);l.new(tex.outputs['Color'],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=strength
 return m
frontmat=photomat('Reference hair color - frontal projection')
sidemat=photomat('Reference hair color - side projection',strength=.45)
def mesh(name,verts,faces,uvs,mat):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);d.materials.append(mat)
 layer=d.uv_layers.new(name='Photo')
 for loop in d.loops:layer.data[loop.index].uv=uvs[loop.vertex_index]
 for p in d.polygons:p.use_smooth=True
 return o
# Image-space silhouettes authored against the reference (front image panel only).
rows=np.array([17,25,40,60,80,100,125,150,175,200,225,250,275,300,330,360,388])
outerL=np.array([130,92,65,46,34,26,22,21,24,22,17,12,5,3,4,5,8])
innerL=np.array([135,139,141,140,133,115,101,86,77,78,91,107,103,88,68,61,58])
outerR=np.array([147,168,188,205,215,218,218,216,214,216,223,231,242,249,254,256,258])
innerR=np.array([135,140,145,155,163,179,188,193,197,190,173,160,165,180,191,199,206])
def hair_depth(x,z,t):
 r=1-(x/.111)**2-((z-1.342)/.117)**2
 y=-.014-.104*math.sqrt(max(.005,r))
 if z<1.27:y=-.068+.008*math.sin((1.27-z)*35+t*2)
 hit,_,_,_=bvh.ray_cast(Vector((x,-.4,z)),Vector((0,1,0)))
 if hit and hit.y<.02:y=min(y,hit.y-.004)
 return y
for side,outer,inner in [('L',outerL,innerL),('R',outerR,innerR)]:
 verts=[];uvs=[];faces=[];N=125;M=18
 for j in range(N):
  py=17+(388-17)*j/(N-1);xo=np.interp(py,rows,outer);xi=np.interp(py,rows,inner)
  for i in range(M):
   t=i/(M-1);px=xo*(1-t)+xi*t;x=(px-135)/1200;z=1.336+(150-py)/1200;y=hair_depth(x,z,t)
   verts.append((x,y,z));uvs.append((px/773,1-py/396))
 for j in range(N-1):
  for i in range(M-1):
   a=j*M+i;faces.append((a,a+1,a+M+1,a+M))
 o=mesh('ARIA R10 - photographic hair shell '+side,verts,faces,uvs,frontmat)
 solid=o.modifiers.new('Hair surface thickness','SOLIDIFY');solid.thickness=.0015
# Rear hair volume: actual curved surface, using the supplied side-view color.
verts=[];uvs=[];faces=[];N=85;M=80
for j in range(N):
 t=j/(N-1);z=1.447-.307*t;width=.012+.104*math.sin(min(1,t/.43)*math.pi/2)
 for i in range(M):
  a=math.pi*i/(M-1);x=width*math.cos(a);y=-.002+(.030+.064*min(1,t/.4))*math.sin(a)
  x+=.003*math.sin(t*19+i*.12)*t
  py=150+(1.336-z)*1200;px=max(524,min(632,598-y*1100))
  verts.append((x,y,z));uvs.append((px/773,1-max(16,min(388,py))/396))
for j in range(N-1):
 for i in range(M-1):
  a=j*M+i;faces.append((a,a+1,a+M+1,a+M))
mesh('ARIA R10 - rear hair volume',verts,faces,uvs,sidemat)

# Indigo collar follows the actual neck surface rather than a floating cone.
v=[];f=[];uv=[]
for row,z in enumerate([1.152,1.18,1.211,1.238]):
 for i in range(96):
  a=math.tau*i/96;direction=Vector((math.cos(a),math.sin(a),0));center=Vector((0,-.012,z));hit,_,_,_=bvh.ray_cast(center,direction)
  co=hit+direction*.0015 if hit else center+direction*.05;v.append(tuple(co));uv.append(((135+co.x*1200)/773,1-(150+(1.336-z)*1200)/396))
for row in range(3):
 for i in range(96):a=row*96+i;f.append((a,row*96+(i+1)%96,(row+1)*96+(i+1)%96,a+96))
m=bpy.data.materials.new('Deep indigo collar');m.diffuse_color=(.017,.018,.045,1);m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=m.diffuse_color
mesh('ARIA R10 - fitted collar',v,f,uv,m)

scene=bpy.context.scene;scene['status']='R10 photographic hair-shell and frontal texture projection study. Three-dimensional surfaces; not strand hair or scan. Profile under review.'
scene.cycles.samples=40;target=Vector((0,-.065,1.324));cam=scene.camera;cam.data.ortho_scale=.33
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r10.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
(out/'profile-fit.json').write_text(json.dumps({'front_rows':list(front_rows.astype(float)),'profile_x':list(profile_x.astype(float)),'depth_shifts_m':list(np.array(shifts).astype(float)),'method':'Authored profile points aligned approximately to front landmarks; not calibrated photographs'},indent=2))
print('R10_SAVED')
