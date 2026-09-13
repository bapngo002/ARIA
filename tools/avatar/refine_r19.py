from pathlib import Path
import bpy,numpy as np,math
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r19-hairline';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r18-side-cleanup/aria-head-r18.blend'))
hair=bpy.data.objects['ARIA R17 - clean hair projection'];hair.name='ARIA R19 - hair';d=hair.data
f=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0];s=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
def sample(m,x,y):return float(m[max(0,min(395,round(y))),max(0,min(m.shape[1]-1,round(x)))])
for i,v in enumerate(d.vertices):
 x,y,z=v.co;py=150+(1.336-z)*1200;af=sample(f,135+x*1200,py);ass=sample(s,84-y*1200,py)
 a=math.tau*(i%192)/192
 w=max(0,min(1,(-math.sin(a)+.10)/.65))
 alpha=(af*w+ass*(1-w));alpha=max(0,min(1,(alpha-.3)/.4))
 if y>0 and z>1.31:alpha=1
 if z>1.40:alpha=1
 d.color_attributes['ProjectionMix'].data[i].color=(w,w,w,alpha)
 d.color_attributes['ScalpCoverage'].data[i].color=(1,alpha,0,1)
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R19 experimental hairline correction. Unapproved and incomplete animation.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r19.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R19_SAVED')
