"""R8 material and swept-hair refinement. Preserves all earlier candidates."""
from pathlib import Path
import bpy,math,random,json
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r9-refinement';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r8-reference-fit/aria-head-r8.blend'))
h=bpy.data.objects['ARIA R8 - reference-fitted face'];h.name='ARIA R9 - reference face'
skin=h.data.materials[0];p=skin.node_tree.nodes.get('Principled BSDF');p.inputs['Specular IOR Level'].default_value=.05;p.inputs['Emission Strength'].default_value=.40
for o in bpy.data.objects:
 if o.type=='LIGHT':o.data.energy*=.52
hair=bpy.data.objects['ARIA R8 - long hair foundation'];hair.name='ARIA R9 - long dark hair foundation'
for v in hair.data.vertices:
 x,y,z=v.co;w=math.exp(-((z-1.322)/.034)**2)*max(0,min(1,(.03-y)/.06))*max(0,min(1,(abs(x)-.035)/.025))
 v.co.y+=.045*w;v.co.x+= (.003 if x>0 else -.003)*w
for m in hair.data.materials:
 if not m or not m.use_nodes:continue
 nodes=m.node_tree.nodes;links=m.node_tree.links
 for n in list(nodes):
  if n.type=='BSDF_PRINCIPLED':
   n.inputs['Roughness'].default_value=.70;n.inputs['Specular IOR Level'].default_value=.12
   if n.inputs['Base Color'].links:
    source=n.inputs['Base Color'].links[0].from_socket
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.19,.14,.12,1)
    links.new(source,mix.inputs[1]);links.new(mix.outputs[0],n.inputs['Base Color'])
# Darken and soften the existing iris materials to match the reference.
for m in bpy.data.materials:
 if m.name.startswith('Brown iris fiber'):
  shader=m.node_tree.nodes.get('Principled BSDF');col=shader.inputs['Base Color'].default_value
  shader.inputs['Base Color'].default_value=(col[0]*.38,col[1]*.48,col[2]*.65,1);shader.inputs['Roughness'].default_value=.35

mat=bpy.data.materials.new('Individual dark brown strands');mat.use_nodes=True
nodes=mat.node_tree.nodes;nodes.clear();output=nodes.new('ShaderNodeOutputMaterial');shader=nodes.new('ShaderNodeBsdfHairPrincipled');shader.parametrization='COLOR';shader.inputs['Color'].default_value=(.015,.009,.006,1);shader.inputs['Roughness'].default_value=.40;mat.node_tree.links.new(shader.outputs[0],output.inputs['Surface'])
curve=bpy.data.curves.new('Swept side-part individual strands','CURVE');curve.dimensions='3D';curve.bevel_depth=.000060;curve.bevel_resolution=0;curve.resolution_u=1
obj=bpy.data.objects.new('ARIA R9 - swept front strands',curve);bpy.context.scene.collection.objects.link(obj);curve.materials.append(mat)
rng=random.Random(987)
def bez(p0,p1,p2,p3,t):return (1-t)**3*p0+3*(1-t)**2*t*p1+3*(1-t)*t*t*p2+t**3*p3
for side in [-1,1]:
 for i in range(3400):
  s=rng.random();offset=Vector((rng.uniform(-.0017,.0017),rng.uniform(-.002,.002),rng.uniform(-.0013,.0013)))
  p0=Vector((.014+side*.01*s,-.073+.085*s,1.444-.005*s))+offset
  p1=Vector((side*(.048+.018*s),-.12+.075*s,1.449-.012*s))+offset
  p2=Vector((side*(.090+.012*s),-.104+.080*s,1.364-.019*s))+offset
  p3=Vector((side*(.079+.011*s),-.004+.049*s,1.298-.025*s))+offset
  spline=curve.splines.new('POLY');spline.points.add(31)
  for j,pt in enumerate(spline.points):
   t=j/31;co=bez(p0,p1,p2,p3,t);co.x+=.0005*math.sin(t*17+s*80)
   pt.co=(*co,1);pt.radius=(.50+.45*rng.random())*(1-t**6)*min(1,.15+t*12)
scene=bpy.context.scene;scene.view_settings.exposure=0;scene.cycles.samples=40;scene.cycles.transparent_max_bounces=16
target=Vector((0,-.075,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));scene['status']='R9 visual refinement under comparison; not approved or deployed.'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r9.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R9_SAVED')
