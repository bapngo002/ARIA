"""R4 adds surface-fitted brows and static lid detail without changing R2 proportions."""
from pathlib import Path
import bpy, math, json, random
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom'
bpy.ops.wm.open_mainfile(filepath=str(out/'aria-head-r3.blend'))
human=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
human.name='ARIA head R4 - preserved R2 proportions'
bpy.context.view_layer.update()
bvh=BVHTree.FromObject(human,bpy.context.evaluated_depsgraph_get())
collection=bpy.data.collections.new('R4 brows and lid details');bpy.context.scene.collection.children.link(collection)
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

for o in list(bpy.data.objects):
 if o.name.startswith('Brow strand'):bpy.data.objects.remove(o,do_unlink=True)
rng=random.Random(73);counts={'brow_hairs':0}
for side in (-1,1):
 for i in range(700):
  t=i/699;x=.011+.036*t;z=1.3515+.007*math.sin(math.pi*t*.88)-.0015*t
  width=.0052*(1-t)**.55+.00012
  z+=rng.uniform(-.5,.5)*width
  pts=[]
  for j in range(7):
   u=j/6
   p=surface(side*(x+.0018*u),z+.0018*math.sin(u*math.pi/2)*(1-.65*t))
   if p is not None:pts.append(p)
  if len(pts)>1:curve('Brow strand R4',pts,.00012,brow,True);counts['brow_hairs']+=1
scene=bpy.context.scene;camera=scene.camera;target=Vector((0,-.0749172628,1.3186111517))
def aim():camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
scene['status']='R4 fuller brows; existing lid details retained; R2 proportions accepted as direction and unchanged.'
scene['remaining']='Hair, skin, clothing, expression rig and final likeness review.'
camera.location=target+Vector((0,-1.2,0));aim();bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r4.blend'))
for name,offset in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
 camera.location=target+Vector(offset);aim();scene.render.filepath=str(out/('head-r4-'+name+'.png'));bpy.ops.render.render(write_still=True)
(out/'head-r4-report.json').write_text(json.dumps({'counts':counts,'base':'aria-head-r3.blend','proportions_changed':False,'status':'static surface fitting; no expression rig'},indent=2),encoding='utf-8')
print('ARIA_R4_COMPLETE',counts)
