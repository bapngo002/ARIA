import bpy,json,sys,struct
from pathlib import Path
root=Path(__file__).resolve().parents[2]/'assets/characters/aria-custom/r6-candidate'
report={}
expected=set(json.loads((root/'build-report.json').read_text())['morphs'])
for ext in ['glb','fbx']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 if ext=='glb':bpy.ops.import_scene.gltf(filepath=str(root/('aria-face-r6.'+ext)))
 else:bpy.ops.import_scene.fbx(filepath=str(root/('aria-face-r6.'+ext)))
 heads=[o for o in bpy.data.objects if o.type=='MESH' and o.data.shape_keys and expected.issubset(set(o.data.shape_keys.key_blocks.keys()))]
 assert heads,f'{ext}: missing head or shape keys'
 h=heads[0];ks=h.data.shape_keys.key_blocks;basis=ks[0]
 deltas={n:max((a.co-b.co).length for a,b in zip(ks[n].data,basis.data)) for n in expected}
 rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
 assert 'head' in rig.data.bones
 assert len(bpy.data.actions)>0
 global_deltas=dict(deltas)
 for obj in bpy.data.objects:
  if obj.type!='MESH' or not obj.data.shape_keys:continue
  blocks=obj.data.shape_keys.key_blocks
  for key in list(blocks)[1:]:
   if key.name in expected:global_deltas[key.name]=max(global_deltas[key.name],max((v.co-b.co).length for v,b in zip(key.data,blocks[0].data)))
 assert all(d>1e-7 for d in global_deltas.values()),f'{ext}: inactive morph'
 report[ext]={'head_name':h.name,'vertices':len(h.data.vertices),'morph_count':len(ks)-1,'morph_max_displacement_m':deltas,'zero_displacement_keys':[n for n,d in deltas.items() if d<1e-7],'whole_avatar_morph_displacements_m':global_deltas,'bones':len(rig.data.bones),'actions':[a.name for a in bpy.data.actions],'bytes':(root/('aria-face-r6.'+ext)).stat().st_size}
 if ext=='glb':
  # Verify the actual animation changes evaluated head geometry after import.
  samples=[]
  for frame in [1,24,45,80]:
   bpy.context.scene.frame_set(frame);bpy.context.view_layer.update()
   ev=h.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh()
   samples.append(sum(v.co.length for v in m.vertices));ev.to_mesh_clear()
  assert max(samples)-min(samples)>1e-5
  report[ext]['evaluated_frame_checksums']=samples
(root/'export-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('VALIDATION_OK',json.dumps({k:{p:v[p] for p in ['morph_count','bones','zero_displacement_keys','bytes']} for k,v in report.items()}))
