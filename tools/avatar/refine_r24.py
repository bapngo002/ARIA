from pathlib import Path
import bpy,math
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r24-projection';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r23-skin-blend/aria-head-r23.blend'))
hair=bpy.data.objects['ARIA R22 - hair'];hair.name='ARIA R24 - hair';d=hair.data
for lp in d.loops:
 x,y,z=d.vertices[lp.vertex_index].co;py=150+(1.336-z)*1200;d.uv_layers['Front'].data[lp.index].uv=((135+x*1200)/773,1-py/396);d.uv_layers['Side'].data[lp.index].uv=((600-y*1200)/773,1-py/396)
for i in range(len(d.vertices)):
 w=max(0,min(1,(-math.sin(math.tau*(i%192)/192)+.1)/.65));d.color_attributes['ProjectionMix'].data[i].color=(w,w,w,1)
m=bpy.data.materials.new('Pixel-normalized dual hair projection');m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.72;p.inputs['Specular IOR Level'].default_value=.04;p.inputs['Emission Strength'].default_value=.6
source=bpy.data.images['ARIA supplied front - three-quarter - profile'];mask=bpy.data.images['Hair validity at texture pixels'];color=[];masks=[]
for uv in ['Side','Front']:
 u=n.new('ShaderNodeUVMap');u.uv_map=uv
 t=n.new('ShaderNodeTexImage');t.image=source;l.new(u.outputs[0],t.inputs[0]);color.append(t.outputs['Color'])
 t=n.new('ShaderNodeTexImage');t.image=mask;l.new(u.outputs[0],t.inputs[0]);masks.append(t.outputs['Color'])
def mathnode(op,a,b):
 o=n.new('ShaderNodeMath');o.operation=op
 for i,v in enumerate([a,b]):
  if isinstance(v,(float,int)):o.inputs[i].default_value=v
  else:l.new(v,o.inputs[i])
 return o.outputs[0]
attr=n.new('ShaderNodeVertexColor');attr.layer_name='ProjectionMix';w=attr.outputs['Color'];wf=mathnode('MULTIPLY',w,masks[1]);ws=mathnode('MULTIPLY',mathnode('SUBTRACT',1.,w),masks[0]);total=mathnode('ADD',wf,ws);norm=mathnode('DIVIDE',wf,mathnode('MAXIMUM',total,.0001))
mix=n.new('ShaderNodeMixRGB');l.new(norm,mix.inputs[0]);l.new(color[0],mix.inputs[1]);l.new(color[1],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color']);l.new(mix.outputs[0],p.inputs['Emission Color']);l.new(total,p.inputs['Alpha']);d.materials.clear();d.materials.append(m)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R24 continuous photo-projected 3D appearance study, awaiting likeness review; rig incomplete.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r24.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R24_SAVED')
