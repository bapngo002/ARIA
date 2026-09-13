"""Install the pinned official MPFB source into the isolated ARIA Blender profile."""
from pathlib import Path
import bpy, shutil, importlib, json
root=Path(__file__).resolve().parents[2]
tools=Path('D:/UserData/ARIA/tools')
source=tools/'mpfb2-source/src/mpfb'
archive=tools/'mpfb-2.0.17'
shutil.make_archive(str(archive),'zip',source)
repo_dir=tools/'blender-profile/extensions/aria_local'
repo_dir.mkdir(parents=True,exist_ok=True)
bpy.ops.preferences.extension_repo_add(name='ARIA local',type='LOCAL',use_custom_directory=True,custom_directory=str(repo_dir))
repo=next(r for r in bpy.context.preferences.extensions.repos if Path(r.directory)==repo_dir)
bpy.ops.extensions.package_install_files(filepath=str(archive)+'.zip',repo=repo.module,enable_on_install=True)
module='bl_ext.'+repo.module+'.mpfb'
mpfb=importlib.import_module(module)
bpy.ops.wm.save_userpref()
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/characters/aria-custom/aria-custom-sculpt.blend'))
human_service=importlib.import_module(module+'.services.humanservice').HumanService
target_service=importlib.import_module(module+'.services.targetservice').TargetService
macro=target_service.get_default_macro_info_dict()
macro['gender']=0.0
macro['age']=.35
human=human_service.create_human(macro_detail_dict=macro)
human.name='ARIA adult female base - NOT likeness sculpt'
for collection in list(human.users_collection):collection.objects.unlink(human)
bpy.data.collections['Custom sculpt - awaiting geometry'].objects.link(human)
human['status']='Unsculpted MPFB base. No likeness or animation acceptance.'
scene=bpy.context.scene
scene['status']='MPFB base created; custom likeness sculpt and eyes/hair/rig pending.'
bpy.context.preferences.filepaths.save_version=0
output=root/'assets/characters/aria-custom/aria-human-base.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(output))
report={'blender':bpy.app.version_string,'mpfb':list(mpfb.VERSION),'source_commit':'80919fa4682335c41847f761a4d79dcad4124732','vertices_including_helpers':len(human.data.vertices),'macro':macro,'status':'base only; no custom likeness','module':module}
(output.parent/'mpfb-setup.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ARIA_MPFB_SETUP_OK',json.dumps(report))
