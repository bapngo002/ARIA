"""Build an editable, rigged approximation of concept 01; not image reconstruction.
Run with Blender 5.2: blender --background --factory-startup --python this_file.
Source VRM and original concept PNG are never overwritten.
"""
from pathlib import Path
import bpy
import math
import json
import struct
from mathutils import Vector, Quaternion

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assets/characters/aria-concept-01'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT / 'software/pi/app_ui/models/aria-sample.vrm'))
scene = bpy.context.scene
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 180
rig = next(o for o in scene.objects if o.type == 'ARMATURE')
face = bpy.data.objects['Face']
hair = bpy.data.objects['Hair']
body = bpy.data.objects['Body']
for obj in list(scene.objects):
    if obj.type == 'MESH' and obj not in (face, hair, body):
        bpy.data.objects.remove(obj, do_unlink=True)

def deform_face(v):
    x, y, z = v
    front = max(0, min(1, (-y-.025)/.035))
    # Adult proportions: reduce enlarged anime eye openings and their surrounding mesh.
    eye = math.exp(-((abs(x)-.040)/.033)**4-((z-1.444)/.035)**4)*front
    z -= (z-1.444)*.16*eye
    x -= (x-math.copysign(.040,x))*.05*eye
    chin = math.exp(-(x/.033)**2-((z-1.352)/.015)**2)
    z += .006*chin
    nose = math.exp(-(x/.012)**2-((z-1.409)/.013)**2)*max(0,min(1,(-y-.075)/.014))
    y += .004*nose
    # Broad, low-amplitude cheek volume, without pointed protrusions.
    cheek = math.exp(-((abs(x)-.052)/.03)**2-((z-1.411)/.026)**2)*front
    y -= .0018*cheek
    return Vector((x,y,z))

for key in face.data.shape_keys.key_blocks:
    for point in key.data:
        point.co = deform_face(point.co)
for vertex, point in zip(face.data.vertices,face.data.shape_keys.key_blocks[0].data):
    vertex.co = point.co

# Dark flowing hair with a subtle asymmetric wave below the jaw.
for vertex in hair.data.vertices:
    x,y,z = vertex.co
    fade=max(0,min(1,(1.44-z)/.25))
    vertex.co.x += .011*math.sin((z-1.05)*24 + (0 if x<0 else 1.1))*fade
    vertex.co.y += .004*math.sin(z*31+x*7)*fade

# Native mesh color detail. These are vertex colors, not projected portrait pixels.
colors=face.data.color_attributes.new(name='ARIA_Complexion',type='FLOAT_COLOR',domain='POINT')
skin_vertices=set()
for poly in face.data.polygons:
    if face.data.materials[poly.material_index].name == 'Face_00_SKIN':
        skin_vertices.update(poly.vertices)
for vertex in face.data.vertices:
    x,y,z=vertex.co
    r,g,b=1.,1.,1.
    if vertex.index in skin_vertices:
        front=max(0,min(1,(-y-.04)/.025))
        blush=.11*math.exp(-((abs(x)-.049)/.025)**2-((z-1.414)/.021)**2)*front
        lips=.40*math.exp(-(x/.021)**4-((z-1.387)/.0058)**2)*front
        g-=blush+lips; b-=blush*.7+lips*.62
    colors.data[vertex.index].color=(r,g,b,1)

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    nodes=mat.node_tree.nodes
    # The VRM source is unlit. Rebuild true PBR nodes instead of retaining emission.
    source_image=next((n.image for n in nodes if n.type=='TEX_IMAGE' and n.image),None)
    nodes.clear()
    shader=nodes.new('ShaderNodeBsdfPrincipled')
    output=nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(shader.outputs['BSDF'],output.inputs['Surface'])
    if source_image:
        texture=nodes.new('ShaderNodeTexImage');texture.image=source_image
        mat.node_tree.links.new(texture.outputs['Color'],shader.inputs['Base Color'])
        # All source surfaces are OPAQUE; connecting alpha changes glTF sorting.
    shader.inputs['Metallic'].default_value=0
    shader.inputs['Roughness'].default_value=.65
    if 'HAIR' in mat.name:
        # Retain authored strand texture and alpha; tint it deep brown/black.
        base=shader.inputs['Base Color']
        if base.is_linked:
            source=base.links[0].from_socket
            mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY'
            mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.12,.095,.10,1)
            mat.node_tree.links.new(source,mix.inputs[1]);mat.node_tree.links.new(mix.outputs[0],base)
        shader.inputs['Roughness'].default_value=.62
        shader.inputs['Specular IOR Level'].default_value=.22
    elif mat.name.startswith('Tops_'):
        base=shader.inputs['Base Color']
        for link in list(base.links):mat.node_tree.links.remove(link)
        base.default_value=(.029,.036,.090,1)
        shader.inputs['Roughness'].default_value=.8
    elif mat.name in ('Face_00_SKIN','Body_00_SKIN'):
        shader.inputs['Roughness'].default_value=.78
        shader.inputs['Subsurface Weight'].default_value=.075
        shader.inputs['Subsurface Radius'].default_value=(1.,.45,.25)
        shader.inputs['Subsurface Scale'].default_value=.008
        if mat.name=='Face_00_SKIN':
            base=shader.inputs['Base Color']
            color=nodes.new('ShaderNodeVertexColor');color.layer_name=colors.name
            mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
            if base.is_linked:mat.node_tree.links.new(base.links[0].from_socket,mix.inputs[1])
            else:mix.inputs[1].default_value=base.default_value
            mat.node_tree.links.new(color.outputs['Color'],mix.inputs[2]);mat.node_tree.links.new(mix.outputs[0],base)
    elif mat.name in ('EyeIris_00_EYE','EyeWhite_00_EYE'):
        shader.inputs['Roughness'].default_value=.32
        shader.inputs['Specular IOR Level'].default_value=.22
        shader.inputs['Coat Weight'].default_value=.12
        shader.inputs['Coat Roughness'].default_value=.25

for obj in (body,face,hair):
    for poly in obj.data.polygons:poly.use_smooth=True

# An original indigo stand collar with a thin metallic rim, weighted to the neck.
def collar_mesh(name,radius,depth,z,height,material):
    vertices=[];faces=[];steps=64
    for level in (0,1):
        for i in range(steps):
            a=i*math.tau/steps
            vertices.append((radius*math.cos(a),depth*math.sin(a),z+level*height))
    for i in range(steps):faces.append((i,(i+1)%steps,(i+1)%steps+steps,i+steps))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(name,mesh);scene.collection.objects.link(obj);obj.parent=rig;mesh.materials.append(material)
    group=obj.vertex_groups.new(name='J_Bip_C_Neck');group.add(list(range(len(vertices))),1,'REPLACE')
    modifier=obj.modifiers.new('Neck skin','ARMATURE');modifier.object=rig
    for p in mesh.polygons:p.use_smooth=True
    return obj
cloth=bpy.data.materials['Tops_01_CLOTH']
collar_mesh('ARIA indigo collar',.056,.047,1.258,.075,cloth)
silver=bpy.data.materials.new('ARIA silver trim');silver.use_nodes=True
shader=silver.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.35,.38,.44,1)
shader.inputs['Metallic'].default_value=.7;shader.inputs['Roughness'].default_value=.3
collar_mesh('ARIA collar trim',.0564,.0474,1.331,.0018,silver)

# Demonstration animation: head turns, two blinks and a restrained smile.
# Keep the authored T pose: secondary sleeve constraints are not imported from VRM.
head=rig.pose.bones['J_Bip_C_Head'];head.rotation_mode='QUATERNION'
head_rest=head.bone.matrix_local.to_quaternion()
for frame,angle in [(1,0),(45,.075),(90,0),(135,-.075),(180,0)]:
    head.rotation_quaternion=head_rest.inverted() @ Quaternion((0,0,1),angle) @ head_rest
    head.keyframe_insert(data_path='rotation_quaternion',frame=frame)
keys=face.data.shape_keys.key_blocks
for suffix in ('Fcl_EYE_Close','Fcl_MTH_Fun'):
    key=next(k for k in keys if k.name.endswith(suffix))
    poses=[(1,0),(40,0),(43,1),(46,0),(125,0),(128,1),(131,0),(180,0)] if 'EYE' in suffix else [(1,.08),(65,.25),(110,.08),(180,.08)]
    for frame,value in poses:key.value=value;key.keyframe_insert(data_path='value',frame=frame)

scene.frame_set(1)
character_objects=[o for o in scene.objects if o.type in ('MESH','ARMATURE')]
for obj in scene.objects:obj.select_set(obj in character_objects)
bpy.context.view_layer.objects.active=rig
properties=bpy.ops.export_scene.gltf.get_rna_type().properties
options=dict(filepath=str(OUT/'aria-concept-01-draft.glb'),export_format='GLB',use_selection=True,
             export_animations=True,export_animation_mode='SCENE',export_frame_range=True,
             export_skins=True,export_morph=True,export_extras=True)
options={k:v for k,v in options.items() if k in properties}
bpy.ops.export_scene.gltf(**options)

# Preserve explicit material factors and provenance in the interchange file.
glb_path=OUT/'aria-concept-01-draft.glb'
binary=glb_path.read_bytes();json_length=struct.unpack_from('<I',binary,12)[0]
document=json.loads(binary[20:20+json_length])
document['asset']['copyright']='Derived from (c) 2022 pixiv Inc.; VRM Public License 1.0 with source settings; see README.md.'
document['asset']['extras']={'ARIA_status':'DRAFT approximation, not approved likeness','sourceLicense':'https://vrm.dev/licenses/1.0/','sourceModel':'VRM1_Constraint_Twist_Sample v1.0.1','modifications':'Face proportions/morphs, hair wave/color, complexion, collar, PBR materials, demonstration animation'}
for material in document.get('materials',[]):
    material['alphaMode']='OPAQUE'
    if 'HAIR' in material.get('name',''):
        material['pbrMetallicRoughness']['baseColorFactor']=[.12,.095,.10,1]
encoded=json.dumps(document,separators=(',',':')).encode('utf-8');encoded+=b' '*((-len(encoded))%4)
tail=binary[20+json_length:]
glb_path.write_bytes(struct.pack('<4sII',b'glTF',2,20+len(encoded)+len(tail))+struct.pack('<I4s',len(encoded),b'JSON')+encoded+tail)

# Studio portrait cameras are only in the editable Blender scene, not the runtime GLB.
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=800;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('ARIA portrait studio')
scene.world.color=(.10,.075,.13)
world=scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.13,.22,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.3
def point_at(obj,point):obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()
def light(name,location,power,size,color):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=location;point_at(obj,(0,0,1.45))
light('Warm softbox',(-.8,-1.2,2.3),30,1.2,(1,.85,.75))
light('Soft fill',(.9,-.7,1.6),15,1.0,(.82,.86,1))
light('Hair rim',(.5,.6,2.0),15,.8,(.85,.75,1))
camera_data=bpy.data.cameras.new('Portrait camera');camera=bpy.data.objects.new('Portrait camera',camera_data);scene.collection.objects.link(camera)
scene.camera=camera;camera_data.type='ORTHO';camera_data.ortho_scale=.38
camera.location=(0,-1.5,1.455);point_at(camera,(0,0,1.455))
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.render.filepath=str(OUT/'front.png')
scene['ARIA_status']='DRAFT: adapted licensed pixiv base, not exact concept-image reconstruction. Pi performance not verified.'
scene['ARIA_reference']='docs/design/aria-face-concepts/01-long-hair.png'
bpy.ops.file.pack_all()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'aria-concept-01-draft.blend'))
bpy.ops.render.render(write_still=True)
camera.location=(.85,-1.25,1.455);point_at(camera,(0,0,1.455))
scene.render.filepath=str(OUT/'three-quarter.png');bpy.ops.render.render(write_still=True)
report={'blender':bpy.app.version_string,'vertices':sum(len(o.data.vertices) for o in character_objects if o.type=='MESH'),
        'bones':len(rig.data.bones),'facial_shape_keys':len(keys)-1,'animation_frames':180,
        'source':'pixiv VRM1_Constraint_Twist_Sample v1.0.1','status':'draft approximation; not image reconstruction'}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('ARIA_BUILD_COMPLETE',json.dumps(report))
