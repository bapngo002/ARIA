"""R2: fitted static eyes and restrained eyelid/nose targets, preserving R1."""
from pathlib import Path
import bpy, importlib, json, math
from mathutils import Vector
root=Path(__file__).resolve().parents[2]
out=root/'assets/characters/aria-custom'
bpy.ops.wm.open_mainfile(filepath=str(out/'aria-head-blockout-r1.blend'))
human=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
human.name='ARIA head R2 - eyes and profile study'
service=importlib.import_module('bl_ext.aria_local.mpfb.services.targetservice').TargetService
targets=Path('D:/UserData/ARIA/tools/mpfb2-source/src/mpfb/data/targets')
adjustments={'eyes/l-eye-height2-incr':.12,'eyes/r-eye-height2-incr':.12,
 'nose/nose-point-up':.06,'nose/nose-point-width-incr':.08,
 'mouth/mouth-upperlip-height-incr':.08}
for path,value in adjustments.items():service.load_target(human,str(targets/(path+'.target.gz')),weight=value)
# Temporary R1 eyes are replaced only in the new R2 scene.
for o in list(bpy.data.objects):
    if 'temporary fitting sphere' in o.name:bpy.data.objects.remove(o,do_unlink=True)
mask=human.modifiers.get('Hide helpers');sub=human.modifiers.get('Sculpt preview smoothing')
mask.show_viewport=False;sub.show_viewport=False;bpy.context.view_layer.update()
evaluated=human.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
assert len(mesh.vertices)==19158
centers={}
for name in ('joint-l-eye','joint-r-eye'):
    index=human.vertex_groups[name].index
    points=[mesh.vertices[v.index].co.copy() for v in human.data.vertices if any(g.group==index for g in v.groups)]
    centers[name]=sum(points,Vector())/len(points)+Vector((0,-.0003,0))
evaluated.to_mesh_clear();mask.show_viewport=True;sub.show_viewport=True

def material(name,color,roughness,coat=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=roughness;p.inputs['Coat Weight'].default_value=coat
    p.inputs['Coat Roughness'].default_value=.14
    return m
sclera=material('Warm ivory sclera',(.72,.68,.63),.24,.12)
pupil=material('Pupil',(.0015,.001,.0008),.18,.15)
limbus=material('Dark limbal ring',(.024,.010,.005),.26,.15)
iris=[]
for i in range(12):
    f=i/11
    iris.append(material('Brown iris fiber '+str(i),(.065+.12*f,.025+.060*f,.009+.019*f),.28,.16))
radius=.0112
for name,center in centers.items():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=40,radius=radius,location=center)
    eye=bpy.context.object;eye.name=name+' - sclera';eye.data.materials.append(sclera)
    for p in eye.data.polygons:p.use_smooth=True
    # A concentric curved cap follows the sphere and provides a real iris silhouette.
    vertices=[];faces=[];segments=120
    rings=[0,.0018,.0023,.0031,.0040,.0047,.00505]
    for rho in rings:
        y=-math.sqrt(radius*radius-rho*rho)-.000025
        for j in range(segments):
            a=math.tau*j/segments
            vertices.append((rho*math.cos(a),y,rho*math.sin(a)))
    for k in range(len(rings)-1):
        for j in range(segments):faces.append((k*segments+j,k*segments+(j+1)%segments,(k+1)*segments+(j+1)%segments,(k+1)*segments+j))
    data=bpy.data.meshes.new(name+' iris geometry');data.from_pydata(vertices,[],faces);data.update()
    obj=bpy.data.objects.new(name+' - iris and pupil',data);bpy.context.scene.collection.objects.link(obj);obj.location=center
    for m in [pupil,limbus,*iris]:data.materials.append(m)
    for p in data.polygons:
        ring=p.index//segments;sector=p.index%segments
        p.material_index=0 if ring==0 else 1 if ring==len(rings)-2 else 2+(sector*7+ring*3)%12
        p.use_smooth=True
    eye['status']='Static fit only; gaze/blink not rigged.'

scene=bpy.context.scene;camera=scene.camera
target=(centers['joint-l-eye']+centers['joint-r-eye'])/2+Vector((0,.025,-.018))
def aim():camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
camera.location=target+Vector((0,-1.2,0));aim()
scene['status']='R2 static eyes/lids/profile study; likeness unapproved, hair/skin/rig pending.'
scene['remaining']='Match portrait likeness; eyebrows, eyelashes, tearline, hair, skin, clothing, eye/face rig.'
bpy.ops.object.select_all(action='DESELECT');human.select_set(True);bpy.context.view_layer.objects.active=human
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r2.blend'))
for name,offset in [('front',(0,-1.2,0)),('three-quarter',(.65,-1,0)),('profile',(1.2,0,0))]:
    camera.location=target+Vector(offset);aim()
    scene.render.filepath=str(out/('head-r2-'+name+'.png'));bpy.ops.render.render(write_still=True)
(out/'head-r2-report.json').write_text(json.dumps({'targets':adjustments,'eye_centers':{k:list(v) for k,v in centers.items()},'eye_radius':radius,'iris_radius':.00505,'status':'static fit and profile study only'},indent=2),encoding='utf-8')
print('ARIA_R2_COMPLETE')
