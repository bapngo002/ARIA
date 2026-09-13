"""R4-derived editable facial proportion study, intentionally no hair or rig.
The reference is qualitative and not calibrated; these are authored adjustments,
not an automatic reconstruction or a verified likeness.
"""
from pathlib import Path
import bpy,importlib,math,json
from mathutils import Vector,Quaternion

root=Path(__file__).resolve().parents[2]
out=root/'assets/characters/aria-custom/r7-head-study';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/aria-head-r4.blend'))
h=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
h.name='ARIA R7 - editable face study'
TS=importlib.import_module('bl_ext.aria_local.mpfb.services.targetservice').TargetService
TS.bake_targets(h)
body=h.vertex_groups['body'].index
remove=[v.index for v in h.data.vertices if v.co.z<1.15 or not any(g.group==body for g in v.groups)]
bpy.ops.object.select_all(action='DESELECT');h.select_set(True);bpy.context.view_layer.objects.active=h
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
for i in remove:h.data.vertices[i].select=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.delete(type='VERT');bpy.ops.object.mode_set(mode='OBJECT')
for m in list(h.modifiers):
 if m.type=='MASK':h.modifiers.remove(m);continue
 if m.type=='SUBSURF':m.levels=2;m.render_levels=2

def gauss(v,c,r):return math.exp(-((v-c)/r)**2)
def edits(co):
 x,y,z=co;front=max(0,min(1,(-y-.025)/.055))
 jaw=Vector((-x*.075*gauss(z,1.267,.027)*front,0,-.0006*gauss(z,1.244,.012)*front))
 nosew=gauss(x,0,.013)*gauss(z,1.309,.019)*max(0,min(1,(-y-.102)/.016))
 nose=Vector((-x*.16*nosew,.0012*gauss(z,1.300,.010)*nosew,.0003*nosew))
 side=1 if x>=0 else -1;dx=abs(x)-.0265
 eye=gauss(dx,0,.013)*gauss(z,1.337,.010)*front
 lids=Vector((side*dx*.18*eye,0,(.0010*(dx/.011)-.0006)*eye))
 mouth=gauss(x,0,.025)*gauss(z,1.279,.009)*max(0,min(1,(-y-.100)/.017))
 lip=Vector((x*.055*mouth,-.0009*mouth,.00065*(abs(x)/.022)**2*mouth))
 return [jaw,nose,lids,lip]

h.shape_key_add(name='Basis - R4 proportions')
names=['01 - Softer jaw and chin','02 - Slimmer nasal shape','03 - Longer eyelids and outer corners','04 - Lip volume and corners']
for n,i in zip(names,range(4)):
 key=h.shape_key_add(name=n)
 for v,k in zip(h.data.vertices,key.data):k.co=v.co+edits(v.co)[i]
 key.value=1
for o in bpy.data.objects:
 if o.type=='CURVE':
  for spline in o.data.splines:
   for p in spline.points:
    co=Vector(p.co[:3]);co+=sum(edits(co),Vector());p.co=(*co,p.co.w)

# Store the supplied sheet in a visible image editor beside the editable head.
ref=bpy.data.images.load(str(root/'assets/characters/aria-custom/r6-candidate/reference-three-views.png'),check_existing=True)
ref.name='ARIA supplied front - three-quarter - profile';ref.pack()
for o in list(bpy.data.objects):
 if o.type=='EMPTY':bpy.data.objects.remove(o,do_unlink=True)
refobj=bpy.data.objects.new('Reference sheet - toggle in Outliner',None);bpy.context.scene.collection.objects.link(refobj)
refobj.empty_display_type='IMAGE';refobj.data=ref;refobj.empty_display_size=.65;refobj.location=(.40,.15,1.32);refobj.rotation_euler=(math.pi/2,0,0);refobj.hide_render=True
refobj.hide_set(True)
scene=bpy.context.scene;scene['status']='R7 face-only study, unapproved likeness. No hair or expression rig. R6 rejected by owner.'
scene['adjustments']='Four reversible shape layers: jaw/chin, nose, eyelids, lips. Toggle each 0-1 for comparison.'
scene.cycles.samples=32
target=Vector((0,-.075,1.326));camera=scene.camera;camera.data.ortho_scale=.31
def aim(offset):
 camera.location=target+Vector(offset);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
aim((0,-1.2,0))
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   space=area.spaces.active;space.region_3d.view_location=target;space.region_3d.view_distance=.40
   space.region_3d.view_rotation=Quaternion((1,0,0),math.pi/2);space.region_3d.view_perspective='ORTHO'
   space.shading.type='MATERIAL';space.overlay.show_floor=False;space.overlay.show_axis_x=False;space.overlay.show_axis_y=False
  elif area.type in ['DOPESHEET_EDITOR','TIMELINE']:
   area.type='IMAGE_EDITOR'
   if hasattr(area.spaces.active,'image'):area.spaces.active.image=ref
  elif area.type=='PROPERTIES':area.spaces.active.context='DATA'
bpy.context.view_layer.objects.active=h;h.select_set(True)
bpy.ops.file.pack_all();bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r7.blend'))
for name,offset in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
 aim(offset);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
(out/'report.json').write_text(json.dumps({'status':scene['status'],'base':'aria-head-r4.blend','head_vertices':len(h.data.vertices),'quads':sum(len(p.vertices)==4 for p in h.data.polygons),'adjustment_keys':names,'reference':'packed original user three-view sheet','verification':'Blender save and three static renders; no exact likeness or animation claim'},indent=2),encoding='utf-8')
print('R7_HEAD_STUDY_SAVED')
