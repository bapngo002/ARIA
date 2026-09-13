"""R3 adds surface-fitted brows and static lid detail without changing R2 proportions."""
from pathlib import Path
import bpy, math, json, random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom'
bpy.ops.wm.open_mainfile(filepath=str(out/'aria-head-r2.blend'))
human=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
human.name='ARIA head R3 - preserved R2 proportions'
bpy.context.view_layer.update()
bvh=BVHTree.FromObject(human,bpy.context.evaluated_depsgraph_get())
collection=bpy.data.collections.new('R3 brows and lid details');bpy.context.scene.collection.children.link(collection)
def mat(name,color,rough):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
brow=mat('Soft brown brow strands',(.048,.024,.015),.7)
lash=mat('Brown lashes',(.024,.012,.008),.5)
rim=mat('Subtle warm lid margin',(.28,.18,.16),.48)
def curve(name,points,radius,material,taper=False):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=2;d.bevel_depth=radius;d.bevel_resolution=2
 s=d.splines.new('POLY');s.points.add(len(points)-1)
 for i,(p,co) in enumerate(zip(s.points,points)):
  p.co=(*co,1);p.radius=max(.05,1-i/(len(points)-1)) if taper else .6+.4*math.sin(math.pi*i/(len(points)-1))
 o=bpy.data.objects.new(name,d);collection.objects.link(o);d.materials.append(material)
def surface(x,z):
 p,n,idx,dist=bvh.ray_cast(Vector((x,-.4,z)),Vector((0,1,0)))
 return p+Vector((0,-.00012,0)) if p is not None else None
rng=random.Random(73);counts={'brow_hairs':0,'lashes':0,'lid_curves':0}
for side in (-1,1):
 # Individually tapered strands follow the actual R2 forehead surface.
 for i in range(135):
  t=i/134;x=.011+.036*t;z=1.3515+.008*math.sin(math.pi*t*.88)-.0015*t
  width=.0024*(1-t)**.6+.00015;z+=rng.uniform(-.5,.5)*width
  pts=[]
  for j in range(6):
   u=j/5;p=surface(side*(x+.0013*u),z+.0018*math.sin(u*math.pi/2)*(1-.65*t))
   if p is not None:pts.append(p)
  if len(pts)>1:curve('Brow strand',pts,.000075,brow,True);counts['brow_hairs']+=1
 center=Vector((side*.0264916047,-.0999172628,1.3366111517));radius=.0112
 # Detect the upper/lower aperture against the eye sphere in frontal projection.
 upper=[];lower=[]
 for i in range(65):
  x=center.x-.0105+.021*i/64;dx=x-center.x
  candidates=[]
  for j in range(121):
   z=center.z-.009+.018*j/120;disc=radius**2-dx*dx-(z-center.z)**2
   if disc<=0:continue
   eye_y=center.y-math.sqrt(disc);p=surface(x,z)
   if p is not None and p.y>eye_y+.00015:candidates.append(z)
  if not candidates:continue
  for dest,z,direction in ((upper,max(candidates),1),(lower,min(candidates),-1)):
   p=surface(x,z+direction*.00020)
   if p is not None:dest.append(p)
 for label,pts in [('upper',upper),('lower',lower)]:
  if len(pts)>5:
   curve(label+' lid margin',pts,.00010,rim);counts['lid_curves']+=1
 if len(upper)>10:
  for idx in range(3,len(upper)-3,3):
   p=upper[idx];pts=[]
   for j in range(7):
    u=j/6;pts.append(p+Vector((side*.0006*u,-.0020*u,.0014*u*u)))
   curve('Upper eyelash',pts,.000065,lash,True);counts['lashes']+=1
scene=bpy.context.scene;camera=scene.camera;target=Vector((0,-.0749172628,1.3186111517))
def aim():camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
scene['status']='R3 static brow/lid detail; R2 proportions accepted as direction and unchanged.'
scene['remaining']='Hair, skin, clothing, expression rig and final likeness review.'
camera.location=target+Vector((0,-1.2,0));aim();bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r3.blend'))
for name,offset in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
 camera.location=target+Vector(offset);aim();scene.render.filepath=str(out/('head-r3-'+name+'.png'));bpy.ops.render.render(write_still=True)
(out/'head-r3-report.json').write_text(json.dumps({'counts':counts,'base':'aria-head-r2.blend','proportions_changed':False,'status':'static surface fitting; no expression rig'},indent=2),encoding='utf-8')
print('ARIA_R3_COMPLETE',counts)
