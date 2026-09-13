"""Build an isolated, reviewable R4-derived facial animation candidate.
Uses existing MPFB and CC0 MakeHuman targets/assets; never deploys ARIA.
"""
from pathlib import Path
import bpy,importlib,math,json,random,bmesh
import numpy as np
from mathutils import Vector,Matrix
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/characters/aria-custom/r6-candidate';OUT.mkdir(parents=True,exist_ok=True)
TOOLS=Path('D:/UserData/ARIA/tools')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/characters/aria-custom/aria-head-r4.blend'))
def service(name,cls):return getattr(importlib.import_module('bl_ext.aria_local.mpfb.services.'+name),cls)
TS=service('targetservice','TargetService');HS=service('humanservice','HumanService')
h=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
h.name='ARIA_R6_Head'
TS.bake_targets(h)
for m in h.modifiers:m.show_viewport=False
bpy.context.view_layer.update()
def group_center(name):
 idx=h.vertex_groups[name].index
 pts=[v.co for v in h.data.vertices if any(g.group==idx for g in v.groups)]
 return sum(pts,Vector())/len(pts)
centers={n:group_center(n) for n in ['joint-l-eye','joint-r-eye','joint-head','joint-neck']}
rig=HS.add_builtin_rig(h,'default');rig.name='ARIA_R6_Rig'
print('RIG',list(rig.data.bones.keys()),flush=True)

def mat(name,color,rough=.5):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
 return m
skin=mat('R6 warm skin - flat color study',(.55,.34,.26),.52)
lips=mat('R6 muted rose lips',(.34,.095,.082),.46)
mouth=mat('R6 oral cavity',(.055,.006,.009),.7)
h.data.materials.clear()
for m in [skin,lips,mouth]:h.data.materials.append(m)
for p in h.data.polygons:
 c=p.center
 # Lip faces follow a bounded front-surface region; not a painted skin texture.
 x,y,z=sum((h.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
 if y<-.11 and (x/.020)**2+((z-1.280)/.006)**2<1:p.material_index=1
 elif abs(x)<.027 and 1.26<z<1.30 and -.104<y<-.045:p.material_index=2
 else:p.material_index=0

assets=[]
for folder,name,typ in [('teeth','teeth_base','Teeth'),('tongue','tongue01','Tongue')]:
 path=TOOLS/'avatar-assets'/folder/name/(name+'.mhclo')
 obj=HS.add_mhclo_asset(str(path),h,asset_type=typ,subdiv_levels=0)
 obj.name='ARIA_R6_'+typ;assets.append((obj,path))

for p in sorted((TOOLS/'extra-targets/assets/faceunits01/targets/faceunits').glob('*.target')):
 TS.load_target(h,str(p),name=p.stem,weight=0)
assert len(h.data.shape_keys.key_blocks)==53
keys=h.data.shape_keys.key_blocks
Mhclo=getattr(importlib.import_module('bl_ext.aria_local.mpfb.entities.clothes.mhclo'),'Mhclo')
for obj,path in assets:
 mapping=Mhclo();mapping.load(str(path));obj.shape_key_add(name='Basis')
 for key in list(keys)[1:]:
  coords=[]
  for idx,info in mapping.verts.items():
   delta=sum(((key.data[v].co-h.data.vertices[v].co)*w for v,w in zip(info['verts'],info['weights'])),Vector())
   if delta.length>1e-7:coords.append((idx,delta))
 if coords:
   k=obj.shape_key_add(name=key.name)
   for idx,delta in coords:k.data[idx].co+=delta
 if obj.name=='ARIA_R6_Teeth':
  # Keep the stock dental/gum mesh behind the R4 lower lip during jaw opening.
  for v in obj.data.vertices:v.co.y+=.006
  for k in obj.data.shape_keys.key_blocks:
   for v in k.data:v.co.y+=.006

# Make the R4 brows and lid details follow facial targets using local weighted
# correspondences. Keep them in one mesh for a practical export draw-call count.
curves=[o for o in bpy.data.objects if o.type=='CURVE']
bpy.ops.object.select_all(action='DESELECT')
for o in curves:o.select_set(True)
bpy.context.view_layer.objects.active=curves[0]
bpy.ops.object.convert(target='MESH');bpy.ops.object.join()
detail=bpy.context.object;detail.name='ARIA_R6_Brows_Lashes_LidMargins'
kd=KDTree(len(h.data.vertices))
for v in h.data.vertices:kd.insert(v.co,v.index)
kd.balance()
near=[];weights=[]
for v in detail.data.vertices:
 ns=kd.find_n(v.co,3);ids=[n[1] for n in ns];ws=np.array([1/max(n[2],.00005)**2 for n in ns]);ws/=ws.sum()
 near.append(ids);weights.append(ws)
near=np.array(near);weights=np.array(weights)
base=np.empty((len(h.data.vertices),3),np.float32);h.data.vertices.foreach_get('co',base.ravel())
dbase=np.empty((len(detail.data.vertices),3),np.float32);detail.data.vertices.foreach_get('co',dbase.ravel())
detail.shape_key_add(name='Basis')
for key in list(keys)[1:]:
 arr=np.empty_like(base);key.data.foreach_get('co',arr.ravel());delta=((arr-base)[near]*weights[:,:,None]).sum(axis=1)
 if np.max(np.abs(delta))>1e-6:
  k=detail.shape_key_add(name=key.name);k.data.foreach_set('co',(dbase+delta).astype(np.float32).ravel())

def bind_head(o,bone='head'):
 o.parent=rig
 if o.type=='MESH':
  g=o.vertex_groups.get(bone) or o.vertex_groups.new(name=bone);g.add(list(range(len(o.data.vertices))),1,'REPLACE')
  a=o.modifiers.new('Head binding','ARMATURE');a.object=rig
bind_head(detail)

# Eye rotations use morphs too, so the same named sliders survive GLB and FBX.
for o in list(bpy.data.objects):
 if not o.name.startswith(('joint-l-eye','joint-r-eye')) or o.type!='MESH':continue
 side='Left' if o.name.startswith('joint-l') else 'Right'
 bind_head(o);o.shape_key_add(name='Basis')
 for direction,axis,angle in [('Up','X',-.35),('Down','X',.35),('In','Z',-.3 if side=='Left' else .3),('Out','Z',.3 if side=='Left' else -.3)]:
  k=o.shape_key_add(name='eyeLook'+direction+side);rot=Matrix.Rotation(angle,3,axis)
  for v in k.data:v.co=rot@v.co

# Remove helpers and crop to an open bust after all correspondences are resolved.
bodyidx=h.vertex_groups['body'].index
remove=[v.index for v in h.data.vertices if not any(g.group==bodyidx for g in v.groups) or v.co.z<1.145]
bpy.ops.object.select_all(action='DESELECT');h.select_set(True);bpy.context.view_layer.objects.active=h
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
for idx in remove:h.data.vertices[idx].select=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.delete(type='VERT');bpy.ops.object.mode_set(mode='OBJECT')
for mod in list(h.modifiers):
 if mod.type in ['MASK','SUBSURF']:h.modifiers.remove(mod)
for mod in h.modifiers:mod.show_viewport=True
sub=h.modifiers.new('Baked facial smoothing','SUBSURF');sub.levels=1;sub.render_levels=1
service('exportservice','ExportService')._apply_modifiers_keep_shapekeys(h,[sub.name])
for mod in list(h.modifiers):
 if mod.type=='SUBSURF':h.modifiers.remove(mod)
keys=h.data.shape_keys.key_blocks
# Smooth per-vertex color prevents polygon-shaped lipstick edges.
color=h.data.color_attributes.new(name='ARIA complexion',type='FLOAT_COLOR',domain='POINT')
for v in h.data.vertices:
 x,y,z=v.co
 f=math.exp(-((x/.020)**4+((z-1.2785)/.0055)**4))*max(0,min(1,(-y-.108)/.009))
 basecol=np.array([.55,.34,.26]);lipcol=np.array([.37,.13,.12])
 complexion=basecol*(1-f)+lipcol*f
 cloth=max(0,min(1,(1.211-z)/.0015))
 color.data[v.index].color=(*list(complexion*(1-cloth)+np.array([.018,.024,.068])*cloth),1)
node=skin.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name=color.name
skin.node_tree.links.new(node.outputs['Color'],skin.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
fabric=mat('Indigo fabric',(.018,.024,.068),.72);h.data.materials.append(fabric)
for p in h.data.polygons:
 c=sum((h.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
 p.material_index=0
bpy.context.view_layer.update()
scalpbvh=BVHTree.FromObject(h,bpy.context.evaluated_depsgraph_get())

# Sculpted hair blockout: scalp shell plus swept, tapered locks. All are actual mesh.
hairmat=mat('R6 dark brown hair',(.023,.013,.010),.4)
hairlight=mat('R6 brown hair highlights',(.041,.025,.018),.43)
verts=[];faces=[]
def tube(points,width,depth):
 start=len(verts);n=8
 for i,p in enumerate(points):
  p=Vector(p);t=i/(len(points)-1);tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
  tangent.normalize();axis=tangent.cross(Vector((0,1,0))).normalized();other=tangent.cross(axis).normalized()
  taper=(.25+.75*math.sin(math.pi*(.08+.9*t))**.45)*(1-.85*t**8)
  for j in range(n):
   a=math.tau*j/n;verts.append(tuple(p+axis*math.cos(a)*width*taper+other*math.sin(a)*depth*taper))
 for i in range(len(points)-1):
  for j in range(n):faces.append((start+i*n+j,start+i*n+(j+1)%n,start+(i+1)*n+(j+1)%n,start+(i+1)*n+j))
def bez(p0,p1,p2,p3,t):return (1-t)**3*Vector(p0)+3*(1-t)**2*t*Vector(p1)+3*(1-t)*t*t*Vector(p2)+t**3*Vector(p3)
# Cap ellipsoid follows head proportions; front hairline remains above brows.
rows=22;cols=96
for i in range(rows):
 for j in range(cols):
  az=math.tau*j/cols;front=(1+math.cos(az))/2
  end=2.05-.92*front**4;polar=.012+(end-.012)*i/(rows-1)
  center=Vector((0,-.025,1.34));direction=Vector((math.sin(polar)*math.sin(az),-math.sin(polar)*math.cos(az),math.cos(polar)))
  hit,normal,_,_=scalpbvh.ray_cast(center,direction)
  co=hit+normal*.003 if hit is not None else center+direction*.095
  verts.append(tuple(co))
for i in range(rows-1):
 for j in range(cols):faces.append((i*cols+j,i*cols+(j+1)%cols,(i+1)*cols+(j+1)%cols,(i+1)*cols+j))
rng=random.Random(62)
for side in [-1,1]:
 for j in range(32):
  s=j/31
  p0=(.009+side*.015*s,-.072+.135*s,1.446-.025*s*s)
  p1=(side*(.057+.025*s),-.105+.15*s,1.437-.028*s)
  p2=(side*(.096+.013*s),-.073+.16*s,1.356-.03*s)
  p3=(side*(.083+.027*s),-.045+.17*s,1.30-.06*s)
  pts=[bez(p0,p1,p2,p3,t/30) for t in range(31)]
  # Extensions form the long silhouette visible over the shoulders.
  end=Vector(p3)
  tangent=(end-Vector(p2)).normalized()
  q1=end+tangent*.04;q2=end+Vector((side*.024,.014,-.07));q3=end+Vector((side*(.018+.012*math.sin(s*5)),.005,-.14-.02*math.sin(s*4)))
  for k in range(1,31):pts.append(bez(end,q1,q2,q3,k/30))
  tube(pts,.004+.002*rng.random(),.0018)
# Fill the rear silhouette with curved locks, rather than exposing a bald cap.
for side in [-1,1]:
 for j in range(55):
  s=j/54;pts=[]
  for k in range(38):
   t=k/37;x=(.010+.009*s)*(1-t)+side*(.066+.008*s)*math.sin(t*math.pi/2)
   z=1.424+.010*s-.012*math.sin(t*math.pi/2)-(.049-.018*s)*t**1.4
   hit,normal,_,_=scalpbvh.ray_cast(Vector((x,-.4,z)),Vector((0,1,0)))
   if hit is not None:pts.append(hit+normal*(.0045+.0015*math.sin(math.pi*t)))
  if len(pts)>2:tube(pts,.0013,.00055)
for j in range(35):
 s=(j/34-.5)*2;x=.07*s
 pts=[bez((x,.050,1.41-.035*s*s),(x*1.4,.105,1.38),(x*1.5,.095,1.22),(x*1.55,.063,1.12+.025*abs(s)),t/55) for t in range(56)]
 tube(pts,.005,.002)
data=bpy.data.meshes.new('R6 layered hair geometry');data.from_pydata(verts,[],faces);data.update()
hair=bpy.data.objects.new('ARIA_R6_Hair_Blockout',data);bpy.context.scene.collection.objects.link(hair)
for m in [hairmat,hairlight]:data.materials.append(m)
for p in data.polygons:p.use_smooth=True;p.material_index=1 if (p.index//416)%5==0 else 0
bind_head(hair)

# Indigo high collar, fitted outside the bust at the lower neckline.
v=[];f=[]
for row,z in enumerate([1.190,1.209,1.218]):
 for j in range(96):
  a=math.tau*j/96;center=Vector((0,-.012,z));direction=Vector((math.cos(a),math.sin(a),0))
  hit,normal,_,_=scalpbvh.ray_cast(center,direction)
  co=hit+direction*.0025 if hit is not None else center+direction*.045
  v.append(tuple(co))
for i in range(2):
 for j in range(96):f.append((i*96+j,i*96+(j+1)%96,(i+1)*96+(j+1)%96,(i+1)*96+j))
d=bpy.data.meshes.new('collar');d.from_pydata(v,[],f);d.update();collar=bpy.data.objects.new('ARIA_R6_Indigo_Collar',d);bpy.context.scene.collection.objects.link(collar)
d.materials.append(mat('Indigo fabric',(.018,.024,.068),.72))
for p in d.polygons:p.use_smooth=True
bind_head(collar,'neck01' if 'neck01' in rig.data.bones else 'head')

# Pack the actual supplied three-view reference, retaining earlier references.
ref=OUT/'reference-three-views.png'
if ref.exists():
 im=bpy.data.images.load(str(ref));im.name='User supplied three-view reference 2026-09-13';im.pack()

scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=120;scene.render.fps=30
meshes=[o for o in bpy.data.objects if o.type=='MESH']
def values(frame,setting):
 for o in meshes:
  if not o.data.shape_keys:continue
  for k in list(o.data.shape_keys.key_blocks)[1:]:
   k.value=setting.get(k.name,0);k.keyframe_insert('value',frame=frame)
for frame,setting in [(1,{}),(20,{}),(24,{'eyeBlinkLeft':1,'eyeBlinkRight':1}),(28,{}),(45,{'jawOpen':.45}),(60,{}),(80,{'mouthSmileLeft':.5,'mouthSmileRight':.5}),(95,{'eyeLookOutLeft':.5,'eyeLookInRight':.5}),(120,{})]:values(frame,setting)
headbone=rig.pose.bones['head'];headbone.rotation_mode='XYZ'
for fr,a in [(1,0),(45,-.10),(80,.12),(120,0)]:
 headbone.rotation_euler.z=a;headbone.keyframe_insert('rotation_euler',frame=fr)
scene.frame_set(1)
target=Vector((0,-.06,1.325));cam=scene.camera;cam.data.ortho_scale=.325
def camera(offset):
 cam.location=target+Vector(offset);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));scene.cycles.samples=24
scene['status']='R6 CANDIDATE: R4 base, hair blockout, ARKit-style morphs. Likeness and full expression QA pending; no Pi deployment.'
scene['source']='MakeHuman MPFB base + extra-targets faceunits01; teeth_base and tongue01 CC0. Custom hair is a blockout.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'aria-face-r6.blend'))

report={'status':scene['status'],'head_vertices':len(h.data.vertices),'head_faces':len(h.data.polygons),'head_quads':sum(len(p.vertices)==4 for p in h.data.polygons),'morphs':list(keys.keys())[1:],'bones':len(rig.data.bones),'meshes':{o.name:len(o.data.vertices) for o in meshes},'sample_animation':'120 frames / 30 fps; blink, jawOpen, smile, gaze and head turn; no audio lip sync','sources':['https://github.com/makehumancommunity/extra-targets','https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html']}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
bpy.ops.object.select_all(action='DESELECT')
for o in meshes+[rig]:o.select_set(True)
bpy.context.view_layer.objects.active=h
bpy.ops.export_scene.gltf(filepath=str(OUT/'aria-face-r6.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_morph=True,export_skins=True,export_apply=False)
bpy.ops.export_scene.fbx(filepath=str(OUT/'aria-face-r6.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},use_mesh_modifiers=False,add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,path_mode='COPY',embed_textures=True)
for name,offset,frame in [('front',(0,-1.2,0),1),('three-quarter',(.65,-1,0),1),('profile',(1.2,0,0),1),('blink',(0,-1.2,0),24),('mouth-open',(.28,-1.2,0),45)]:
 scene.frame_set(frame);camera(offset);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R6_COMPLETE',json.dumps(report),flush=True)
