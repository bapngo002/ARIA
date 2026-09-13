"""Tighten hair to both observed silhouettes; refine profile chin/lips and ear scale."""
from pathlib import Path
import bpy,math
import numpy as np
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r14-likeness';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r13-appearance/aria-head-r13.blend'))
h=bpy.data.objects['ARIA R13 - reference face'];h.name='ARIA R14 - face'
import importlib
TS=importlib.import_module('bl_ext.aria_local.mpfb.services.targetservice').TargetService;TS.bake_targets(h)
h.shape_key_add(name='Basis - R13');key=h.shape_key_add(name='Chin lip and ear profile correction')
for b,v in zip(h.data.vertices,key.data):
 x,y,z=b.co;fw=max(0,min(1,(-y-.055)/.035))
 v.co.y+=fw*(.012*math.exp(-((z-1.256)/.017)**2-(x/.06)**2)+.0025*math.exp(-((z-1.281)/.008)**2-(x/.03)**2))
 ear=max(0,min(1,(abs(x)-.053)/.012))*max(0,min(1,(y+.040)/.020))*math.exp(-((z-1.320)/.030)**6)
 v.co.z+=(1.321-z)*.23*ear;v.co.x+=((.067 if x>0 else -.067)-x)*.16*ear
key.value=1
front=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0];side=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
def sample(mask,x,y):return float(mask[max(0,min(395,int(y))),max(0,min(mask.shape[1]-1,int(x)))])
hair=bpy.data.objects['ARIA R13 - textured hair volume'];hair.name='ARIA R14 - reference hair volume';d=hair.data;attrs=d.color_attributes['ProjectionMix']
for i,v in enumerate(d.vertices):
 x,y,z=v.co;py=150+(1.336-z)*1200;pxF=135+x*1200;pxS=600-y*1200
 af=sample(front,pxF,py);ass=sample(side,pxS-516,py)
 a=math.tau*(i%192)/192
 confidence=min(af,ass) if math.sin(a)<.05 else ass
 alpha=max(0,min(1,(confidence-.28)/.50))
 old=attrs.data[i].color;attrs.data[i].color=(old[0],old[1],old[2],alpha)
 # The lower side locks pass behind the ear rather than cutting through the cheek.
 w=math.exp(-((z-1.287)/.023)**2)*max(0,min(1,(abs(x)-.040)/.022))*max(0,min(1,(.015-y)/.055))
 v.co.y+=.014*w
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R14 appearance refinement: multiview hair silhouette and profile correction; photo projection, not strand hair.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r14.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,0,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R14_SAVED')
