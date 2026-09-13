"""Non-destructive first proportion pass; neutral clay renders, no likeness claim."""
from pathlib import Path
import bpy, importlib, json
from mathutils import Vector
root=Path(__file__).resolve().parents[2]
out=root/'assets/characters/aria-custom'
bpy.ops.wm.open_mainfile(filepath=str(out/'aria-human-base.blend'))
human=next(o for o in bpy.data.objects if o.type=='MESH')
human.name='ARIA head proportions R1 - review required'
targets=Path('D:/UserData/ARIA/tools/mpfb2-source/src/mpfb/data/targets')
service=importlib.import_module('bl_ext.aria_local.mpfb.services.targetservice').TargetService
adjustments={'head/head-oval':.22,'head/head-scale-horiz-decr':.10,
 'chin/chin-height-decr':.12,'chin/chin-width-incr':.12,'chin/chin-bones-decr':.15,
 'nose/nose-width1-decr':.16,'nose/nose-width3-decr':.12,
 'mouth/mouth-upperlip-volume-incr':.18,'mouth/mouth-lowerlip-volume-incr':.16,
 'mouth/mouth-cupidsbow-incr':.10,'mouth/mouth-angles-up':.07,
 'eyes/l-eye-scale-incr':.18,'eyes/r-eye-scale-incr':.18}
loaded=[]
for path,value in adjustments.items():
    key=service.load_target(human,str(targets/(path+'.target.gz')),weight=value)
    loaded.append((key,value))

# Obtain eye centers from authored landmarks, with helpers temporarily visible.
mask=human.modifiers.get('Hide helpers');mask.show_viewport=False
bpy.context.view_layer.update()
mesh=human.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
assert len(mesh.vertices)==len(human.data.vertices)
landmarks={}
for name in ('joint-l-eye','joint-r-eye'):
    idx=human.vertex_groups[name].index
    points=[mesh.vertices[v.index].co.copy() for v in human.data.vertices if any(g.group==idx for g in v.groups)]
    landmarks[name]=sum(points,Vector())/len(points)
human.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh_clear()
mask.show_viewport=True
sub=human.modifiers.new('Sculpt preview smoothing','SUBSURF');sub.levels=1;sub.render_levels=2
clay=bpy.data.materials.new('Neutral sculpt clay');clay.diffuse_color=(.42,.39,.37,1);clay.use_nodes=True
shader=clay.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.42,.39,.37,1);shader.inputs['Roughness'].default_value=.7
human.data.materials.clear();human.data.materials.append(clay)
for face in human.data.polygons:face.material_index=0;face.use_smooth=True
for name,center in landmarks.items():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,radius=.010,location=center)
    eye=bpy.context.object;eye.name=name+' - temporary fitting sphere';eye.data.materials.append(clay)
    for face in eye.data.polygons:face.use_smooth=True

scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=640;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Sculpt studio');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.15,.15,.15,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.35
eye_mid=(landmarks['joint-l-eye']+landmarks['joint-r-eye'])/2
target=eye_mid+Vector((0,.025,-.018))
def aim(o):o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
for name,offset,power,size in [('Key',(-.6,-.8,.7),35,1.0),('Fill',(.7,-.3,.2),12,.8),('Rim',(.3,.6,.5),22,.7)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=target+Vector(offset);aim(obj)
data=bpy.data.cameras.new('Head review');camera=bpy.data.objects.new('Head review',data);scene.collection.objects.link(camera);scene.camera=camera
data.type='ORTHO';data.ortho_scale=.34
camera.location=target+Vector((0,-1.2,0));aim(camera)
scene['status']='First MPFB proportion blockout only; not approved likeness. Eye spheres are placeholders.'
scene['remaining']='Detailed likeness sculpt, fitted eyes, hair, clothing, textures, rig and animation.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='DESELECT');human.select_set(True);bpy.context.view_layer.objects.active=human
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_location=target
            area.spaces.active.region_3d.view_distance=.55
bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-blockout-r1.blend'))
for key,value in loaded:key.value=0
bpy.context.view_layer.update()
scene.render.filepath=str(out/'head-before-front.png');bpy.ops.render.render(write_still=True)
for key,value in loaded:key.value=value
bpy.context.view_layer.update()
for name,offset in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
    camera.location=target+Vector(offset);aim(camera)
    scene.render.filepath=str(out/('head-r1-'+name+'.png'));bpy.ops.render.render(write_still=True)
(out/'head-r1-report.json').write_text(json.dumps({'targets':adjustments,'eye_landmarks':{k:list(v) for k,v in landmarks.items()},'status':'proportion study, not accepted likeness'},indent=2),encoding='utf-8')
print('ARIA_HEAD_R1_COMPLETE')
