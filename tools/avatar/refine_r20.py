from pathlib import Path
import bpy,numpy as np,math
from mathutils import Vector
root=Path(__file__).resolve().parents[2];out=root/'assets/characters/aria-custom/r20-continuous-hair';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/r19-hairline/aria-head-r19.blend'))
hair=bpy.data.objects['ARIA R19 - hair'];old=hair.data;mat=old.materials[0];verts=[tuple(v.co) for v in old.vertices];M=192;N=len(verts)//M
faces=[(j*M+i,j*M+(i+1)%M,(j+1)*M+(i+1)%M,(j+1)*M+i) for j in range(N-1) for i in range(M)]
d=bpy.data.meshes.new('Continuous hair surface');d.from_pydata(verts,[],faces);d.update();hair.data=d;hair.name='ARIA R20 - continuous hair';d.materials.append(mat)
f=np.load('D:/UserData/ARIA/tools/avatar-fit-data/front-segmentation.npy')[1,:,:,0];s=np.load('D:/UserData/ARIA/tools/avatar-fit-data/profile-segmentation.npy')[1,:,:,0]
uf=d.uv_layers.new(name='Front');us=d.uv_layers.new(name='Side');mix=d.color_attributes.new(name='ProjectionMix',type='FLOAT_COLOR',domain='POINT');coverage=d.color_attributes.new(name='ScalpCoverage',type='FLOAT_COLOR',domain='POINT')
uvf=[];uvs=[]
def info(mask,px,py,offset):
 iy=max(0,min(395,round(py)));ix=max(0,min(mask.shape[1]-1,round(px)));conf=float(mask[iy,ix]);found=np.where(mask[iy]>.78)[0]
 if conf<.78 and len(found):ix=int(found[np.argmin(abs(found-ix))])
 return conf,((ix+offset+.5)/773,1-(iy+.5)/396)
for i,(x,y,z) in enumerate(verts):
 py=150+(1.336-z)*1200;af,uv=info(f,135+x*1200,py,0);ass,sv=info(s,84-y*1200,py,516);uvf.append(uv);uvs.append(sv)
 a=math.tau*(i%M)/M;w=max(0,min(1,(-math.sin(a)+.10)/.65));conf=w*af+(1-w)*ass;weight=w*af/(conf+1e-8);alpha=max(0,min(1,(conf-.30)/.40))
 if y>0 and z>1.31:alpha=1
 if z>1.40:alpha=1
 mix.data[i].color=(weight,weight,weight,alpha);coverage.data[i].color=(1,alpha,0,1)
for lp in d.loops:uf.data[lp.index].uv=uvf[lp.vertex_index];us.data[lp.index].uv=uvs[lp.vertex_index]
for p in d.polygons:p.use_smooth=True
scene=bpy.context.scene;scene.cycles.samples=48;scene['status']='R20 continuous hair surface study. Likeness review pending; no animation-ready claim.'
target=Vector((0,-.065,1.324));cam=scene.camera
def camera(off):cam.location=target+Vector(off);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((0,-1.2,0));bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'aria-head-r20.blend'))
for name,off in [('front',(0,-1.2,0)),('three-quarter',(-.65,-1,0)),('profile',(-1.2,-.22,0))]:
 camera(off);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('R20_SAVED')
